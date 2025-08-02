
import requests
import re

def extrage_dimensiuni_ocr_space(image_file):
    url_api = 'https://api.ocr.space/parse/image'
    payload = {
        'isOverlayRequired': False,
        'apikey': 'helloworld',  # demo key
        'language': 'ron'
    }
    r = requests.post(url_api, files={'filename': image_file}, data=payload)
    result = r.json()

    if not result['IsErroredOnProcessing']:
        full_text = result['ParsedResults'][0]['ParsedText'].lower()

        dimensiuni = {"înălțime": None, "lățime": None, "adâncime": None}
        full_text = full_text.replace("î", "i").replace("ă", "a").replace("â", "a").replace("ș", "s").replace("ț", "t")

        patterns = {
            "înălțime": r"(inaltime|h)[^\d]*(\d{3,4})",
            "lățime": r"(latime|l)[^\d]*(\d{3,4})",
            "adâncime": r"(adancime|a|d)[^\d]*(\d{3,4})"
        }

        for cheie, pattern in patterns.items():
            match = re.search(pattern, full_text)
            if match:
                dimensiuni[cheie] = int(match.group(2))

        return dimensiuni, full_text
    else:
        return {"înălțime": None, "lățime": None, "adâncime": None}, "Eroare OCR"
