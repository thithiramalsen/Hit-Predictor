# backend/src/ocr_extract.py
import re
from PIL import Image
import pytesseract
import easyocr
import numpy as np
import os
from .utils import enhance_image_for_ocr

# Use Tesseract in production (Vercel) as it's lighter than EasyOCR.
# The VERCEL environment variable is set by Vercel.
# Locally, you can set USE_EASYOCR=True in your environment to use EasyOCR.
USE_EASYOCR = os.getenv("USE_EASYOCR", "False").lower() in ("true", "1") and not os.getenv("VERCEL")

def ocr_with_tesseract(pil_image: Image.Image):
    # optional enhancement to help tesseract
    img = pil_image.convert("RGB")
    text = pytesseract.image_to_string(img, lang="eng", config='--psm 6')
    return text

def ocr_with_easyocr(image_path):
    reader = easyocr.Reader(["en"], gpu=False)
    res = reader.readtext(image_path, detail=0)
    text = "\n".join(res)
    return text

def extract_features_from_text(text: str) -> dict:
    print("RAW OCR TEXT:\n", text)  # Debug print
    text = text.lower()
    out = {}
    # Improved key extraction: match "F# Major", "Gb Major", "F#IGb Major", etc.
    key_match = re.search(r"\b([a-g][#b]?)\w*\s*(major|minor)\b", text)
    if key_match:
        note = key_match.group(1).strip().upper()
        scale = key_match.group(2).lower()
        out["key_str"] = f"{note} {scale}".strip()
    # Explicit, happiness, loudness (unchanged)
    explicit_match = re.search(r"explicit[:;\s]*(yes|no)", text)
    if explicit_match:
        out["explicit_str"] = explicit_match.group(1).strip()
    happiness_match = re.search(r"happiness[:;\s]*([0-9]+)", text)
    if happiness_match:
        out["happiness"] = float(happiness_match.group(1))
    loudness_match = re.search(r"loudness[:;\s]*([-+]?\d+\.?\d*)\s*d?b?", text)
    if loudness_match:
        out["loudness"] = float(loudness_match.group(1))
    # --- Duration/Length handling ---
    # 1. mm:ss (colon)
    length_match_colon = re.search(r"(length|duration)[:;\s]*([0-9]+):([0-9]+)", text)
    if length_match_colon:
        mm, ss = length_match_colon.group(2), length_match_colon.group(3)
        out["duration_min"] = float(mm) + float(ss)/60.0
    else:
        # 2. m.ss (dot, where .ss is seconds, NOT decimal)
        length_match_dot = re.search(r"(length|duration)[:;\s]*([0-9]+)\.([0-9]{1,2})", text)
        if length_match_dot:
            mm, ss = length_match_dot.group(2), length_match_dot.group(3)
            # treat .ss as seconds, not decimal
            out["duration_min"] = float(mm) + float(ss)/60.0

    # Remove any fallback that treats a single float as decimal minutes for duration/length!
    # --- Rest of your float extraction logic (unchanged) ---
    float_pattern = r"([a-zA-Z %]+?)[:\s]*([-+]?\d*\.\d+|\d+[:\d]*)"
    matches = re.findall(float_pattern, text)
    for k, v in matches:
        key = k.strip()
        val = v.strip()
        try:
            if ":" in val:  # duration mm:ss matched as "mm:ss"
                mm, ss = val.split(":")
                val_num = float(mm) + float(ss)/60.0
                out["duration_min"] = val_num
                continue
            # Only treat as decimal if not length/duration
            if ("duration" in key or "length" in key):
                # If it matches m.ss, already handled above, so skip
                continue
            val_num = float(val)
        except:
            continue
        if "dance" in key:
            out["danceability"] = val_num
        elif "energy" in key:
            out["energy"] = val_num
        elif key.strip() == "key":
            out["key"] = int(val_num)
        elif "loud" in key:
            out["loudness"] = val_num
        elif "speech" in key:
            out["speechiness"] = val_num
        elif "acoustic" in key:
            out["acousticness"] = val_num
        elif "instrument" in key:
            out["instrumentalness"] = val_num
        elif "liveness" in key:
            out["liveness"] = val_num
        elif "valence" in key:
            out["valence"] = val_num
        elif "tempo" in key:
            out["tempo"] = val_num
        elif "duration" in key or "length" in key:
            # Only treat as decimal if not already handled above
            if val_num > 1000:
                out["duration_min"] = val_num / 60000.0
            elif val_num > 120:
                out["duration_min"] = val_num / 60.0
            else:
                out["duration_min"] = val_num
    return out

def extract_from_image(image_path_or_pil):
    # Accept PIL Image or path
    tmp_path = None
    if isinstance(image_path_or_pil, str):
        path = image_path_or_pil
        if USE_EASYOCR:
            text = ocr_with_easyocr(path)
        else:
            img = Image.open(path)
            text = ocr_with_tesseract(img)
    else:
        # PIL Image
        pil_img = image_path_or_pil
        pil_img = enhance_image_for_ocr(pil_img)
        tmp_path = "tmp_ocr.png"
        pil_img.save(tmp_path)
        if USE_EASYOCR:
            text = ocr_with_easyocr(tmp_path)
        else:
            text = ocr_with_tesseract(pil_img)
    if tmp_path and os.path.exists(tmp_path):
        try:
            os.remove(tmp_path)
        except:
            pass
    features = extract_features_from_text(text)
    return features

def extract_features_from_image(image_path):
    """
    Wrapper for API to extract features from an image file path.
    """
    return extract_from_image(image_path)

if __name__ == "__main__":
    import sys
    fp = sys.argv[1]
    print(extract_from_image(fp))
