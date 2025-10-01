# backend/src/utils.py
import cv2
import numpy as np
from PIL import Image

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
