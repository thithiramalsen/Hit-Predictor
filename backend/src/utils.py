# backend/src/utils.py
import cv2
import numpy as np
from PIL import Image

KEY_MAP = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5,
    "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
}

def enhance_image_for_ocr(pil_img: Image.Image) -> Image.Image:
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # resize to improve OCR reading if small
    h, w = gray.shape
    if max(h, w) < 1000:
        scale = 1000 / max(h, w)
        gray = cv2.resize(gray, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_CUBIC)
    # adaptive threshold
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((1,1), np.uint8)
    dilated = cv2.dilate(th, kernel, iterations=1)
    return Image.fromarray(cv2.cvtColor(dilated, cv2.COLOR_BGR2RGB))

def parse_key(key_str):
    # Example: "E Minor", "C#/Db Minor", "G Major"
    for note in KEY_MAP:
        if note in key_str:
            return KEY_MAP[note]
    return None

def parse_mode(key_str):
    if "major" in key_str.lower():
        return 1
    elif "minor" in key_str.lower():
        return 0
    return None

def parse_explicit(explicit_str):
    if explicit_str.strip().lower() in ["yes", "1", "true"]:
        return 1
    return 0

def parse_valence(happiness):
    # Chosic: 0-100, Spotify: 0-1
    return float(happiness) / 100.0
