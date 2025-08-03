import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

def genereaza_deviz_AI(tip_dulap, prompt_descriere, cale_csv):
    prompt = f"""
Ești un configurator AI specializat în mobilier. Primești detalii despre un corp de mobilier și returnezi un deviz estimativ în format JSON care include:
1. materiale folosite (denumire, cantitate, preț unitar)
2. accesorii necesare (denumire, cantitate, preț unitar)
3. servicii implicate (tip, cantitate, preț unitar)
4. valoare_totală (suma totală estimată)

Returnează **doar** structura JSON de mai jos:
{
  "materiale": [
    {"nume": "", "cantitate": , "pret_unitar": },
    ...
  ],
  "accesorii": [
    {"nume": "", "cantitate": , "pret_unitar": },
    ...
  ],
  "servicii": [
    {"tip": "", "cantitate": , "pret_unitar": },
    ...
  ],
  "valoare_total": 
}

Tip dulap: {tip_dulap}
Detalii suplimentare: {prompt_descriere}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        content = response.choices[0].message['content']
        return json.loads(content)
    except Exception as e:
        return {"eroare": str(e), "materiale": [], "accesorii": [], "servicii": [], "valoare_total": 0.0}
