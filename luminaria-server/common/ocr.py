import io

import pytesseract
import requests
from PIL import Image

from constants import IS_DEV_ENV

if IS_DEV_ENV:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_img_from_url(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return image


def ocr(image):
    text = pytesseract.image_to_string(image)
    return text


def image_to_text(url):
    image = get_img_from_url(url)
    text = ocr(image)
    return text
