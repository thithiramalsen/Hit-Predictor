# backend/src/ocr_extract.py
import re
from PIL import Image
import pytesseract
import easyocr
import numpy as np
import os
from utils import enhance_image_for_ocr

USE_EASYOCR = True

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
    text = text.lower()
    out = {}
    # Extract key string (e.g., "key: e minor")
    key_match = re.search(r"key[:\s]*([a-g][#b]?[\s]?(major|minor)?)", text)
    if key_match:
        out["key_str"] = key_match.group(1).strip()
    # Extract explicit string (e.g., "explicit: yes")
    explicit_match = re.search(r"explicit[:\s]*(yes|no)", text)
    if explicit_match:
        out["explicit_str"] = explicit_match.group(1).strip()
    # Extract happiness/valence
    happiness_match = re.search(r"happiness[:\s]*([0-9]+)", text)
    if happiness_match:
        out["happiness"] = float(happiness_match.group(1))
    # Existing float extraction logic...
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
        elif "duration" in key:
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

if __name__ == "__main__":
    import sys
    fp = sys.argv[1]
    print(extract_from_image(fp))
