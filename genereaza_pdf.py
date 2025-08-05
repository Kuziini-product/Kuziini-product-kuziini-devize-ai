from utils.pdf_exporter import export_pdf_detaliat
import json
from pathlib import Path

# Calea către fișierul tău JSON
json_path = Path("data/oferta_actualizata.json")
logo_path = "Logo_Kuziini.png"  # imaginea cu logo-ul (dacă o ai)

# Încarcă datele din JSON
with open(json_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Generează PDF-ul
export_pdf_detaliat(json_data, logo_path)
