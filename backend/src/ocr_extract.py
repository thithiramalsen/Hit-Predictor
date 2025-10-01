# src/ocr_extract.py
import re
from PIL import Image
import pytesseract
import easyocr
import numpy as np

# Preferred: EasyOCR (often handles numbers better). If Tesseract is used, tune config (--psm)
USE_EASYOCR = True

# Example mapping: keys in training pipeline
EXPECTED_FEATURES = [
    "danceability", "energy", "key", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration"
    # adjust names to match Chosic labels exactly
]

def ocr_with_tesseract(image: Image.Image):
    text = pytesseract.image_to_string(image, lang="eng", config='--psm 6')
    return text

def ocr_with_easyocr(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    res = reader.readtext(image_path, detail=0)
    # join lines
    text = "\n".join(res)
    return text

def extract_features_from_text(text: str) -> dict:
    """
    Parse common patterns like:
      Danceability: 0.658
      Tempo: 120 BPM
      Loudness: -5.32 dB
    Returns a dict of numeric features mapped to expected pipeline columns.
    """
    text = text.lower()
    out = {}
    # floats
    float_pattern = r"([a-z ]+?)[:\s]*([-+]?\d*\.\d+|\d+)"
    matches = re.findall(float_pattern, text)
    # Create a lookup map by checking for keywords
    for k, v in matches:
        key = k.strip()
        try:
            val = float(v)
        except:
            continue
        # key heuristic
        if "dance" in key:
            out["danceability"] = val
        elif "energy" in key:
            out["energy"] = val
        elif key == "key":
            # sometimes key is like "Key: 5" -> treat as int
            out["key"] = int(val)
        elif "loud" in key:
            out["loudness"] = val
        elif "speech" in key:
            out["speechiness"] = val
        elif "acoustic" in key:
            out["acousticness"] = val
        elif "instrument" in key:
            out["instrumentalness"] = val
        elif "liveness" in key:
            out["liveness"] = val
        elif "valence" in key:
            out["valence"] = val
        elif "tempo" in key:
            out["tempo"] = val
        elif "duration" in key:
            # duration might be mm:ss or seconds or ms; try parse '3:42' or 222
            if ":" in v:
                mm, ss = v.split(":")
                out["duration_min"] = float(mm) + float(ss)/60.0
            else:
                # assume seconds
                if val > 1000:  # if ms
                    out["duration_min"] = val / 60000.0
                else:
                    out["duration_min"] = val/60.0
    return out

def extract_from_image(image_path_or_pil):
    # accept both file paths and PIL.Image
    if isinstance(image_path_or_pil, str):
        if USE_EASYOCR:
            text = ocr_with_easyocr(image_path_or_pil)
        else:
            img = Image.open(image_path_or_pil)
            text = ocr_with_tesseract(img)
    else:
        # assume PIL Image
        if USE_EASYOCR:
            # save temp
            tmp = "tmp_ocr.png"
            image_path_or_pil.save(tmp)
            text = ocr_with_easyocr(tmp)
        else:
            text = ocr_with_tesseract(image_path_or_pil)

    features = extract_features_from_text(text)
    return features

if __name__ == "__main__":
    import sys
    fp = sys.argv[1]
    print(extract_from_image(fp))
