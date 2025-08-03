import openai
import os
from dotenv import load_dotenv

# Încarcă variabilele din fișierul .env
load_dotenv()

def extrage_dimensiuni_cu_gpt(text_ocr):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY nu este setat.")
    openai.api_key = api_key

    prompt = f'''
Analizează următorul text extras dintr-o schiță tehnică de mobilier și extrage dimensiunile dacă sunt prezente.

Verifică dacă în text sunt valori ce corespund unor dimensiuni reale (în milimetri) și clasifică-le în:
- înălțime
- lățime
- adâncime

Dacă o valoare lipsește, returnează NULL pentru ea.

Textul este:
\"\"\"
{text_ocr}
\"\"\"

Returnează în format JSON exact așa:
{{
  "înălțime": ...,
  "lățime": ...,
  "adâncime": ...
}}
    '''

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = response['choices'][0]['message']['content']
        return eval(content)
    except Exception as e:
        print("❌ Eroare GPT:", e)
        return {"înălțime": None, "lățime": None, "adâncime": None}
