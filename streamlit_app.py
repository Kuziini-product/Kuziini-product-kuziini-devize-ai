import streamlit as st
from pathlib import Path
import json
from datetime import datetime
import re
import fitz  # PyMuPDF
from PIL import Image
import io
import pandas as pd

from utils.openai_utils import genereaza_deviz_AI
from utils.pdf_exporter import export_pdf, export_pdf_detaliat
from utils.excel_exporter import export_excel
from utils.github_uploader import incarca_in_github
from utils.ocr_online import extrage_dimensiuni_ocr_space
from utils.gpt_dimension_extractor import extrage_dimensiuni_cu_gpt
from components.header import afiseaza_header
from components.history_slider import afiseaza_istoric

st.set_page_config(page_title="Kuziini | Generator Devize AI", layout="wide")
afiseaza_header()

df_accesorii = pd.read_csv("Accesorii.csv")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
numar_oferte = len(list(output_dir.glob("OF-*.json")))
st.markdown(f"📊 Devize generate: **{numar_oferte}**")

# ========================
# 📤 Upload fișier (PDF sau imagine)
# ========================
uploaded_file = st.file_uploader("📤 Încarcă o schiță (PDF, JPG, PNG)", type=None)
inaltime = latime = adancime = 100
dims = {"înălțime": None, "lățime": None, "adâncime": None}

if uploaded_file:
    file_type = uploaded_file.type
    text = ""

    with st.spinner("🔍 Se procesează fișierul și extrage textul..."):
        if "pdf" in file_type:
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            pix = doc[0].get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_bytes))
            dims, text = extrage_dimensiuni_ocr_space(io.BytesIO(img_bytes))

        elif "image" in file_type:
            dims, text = extrage_dimensiuni_ocr_space(uploaded_file)

        # 🧠 Dacă OCR nu a returnat nimic, cerem GPT să înțeleagă textul
        if not any(dims.values()) and text:
            dims = extrage_dimensiuni_cu_gpt(text)

        st.success("✅ Dimensiuni extrase inteligent:")
        st.write(dims)

        if dims["înălțime"]: inaltime = dims["înălțime"]
        if dims["lățime"]: latime = dims["lățime"]
        if dims["adâncime"]: adancime = dims["adâncime"]

# ========================
# 🧾 Formular completare
# ========================
col1, col2 = st.columns(2)
with col1:
    nume_client = st.text_input("Nume client")
with col2:
    telefon_client = st.text_input("Telefon client")

col1, col2, col3 = st.columns(3)
with col1:
    inaltime = st.number_input("Înălțime (mm)", min_value=100, value=inaltime)
with col2:
    latime = st.number_input("Lățime (mm)", min_value=100, value=latime)
with col3:
    adancime = st.number_input("Adâncime (mm)", min_value=100, value=adancime)

tip_dulap = st.selectbox("Tip dulap", [
    "dulap de dressing", "dulap bucătărie bază", "dulap bucătărie suspendat",
    "dulap colț bază", "dulap colț suspendat", "poliță", "consolă"
])

prompt_descriere = st.text_area("Descriere scurtă (ex: culoare PAL, preferințe)")

# ========================
# 🔧 Generează deviz
# ========================
if st.button("🔧 Generează ofertă"):
    with st.spinner("Se generează devizul..."):
        dimensiuni = {"înălțime": inaltime, "lățime": latime, "adâncime": adancime}
        json_data = genereaza_deviz_AI(tip_dulap, dimensiuni, prompt_descriere, nume_client, telefon_client)
        numar_oferta = f"OF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        json_data["numar"] = numar_oferta
        total = json_data.get("valoare_total", 0.0)

        with open(f"history/{numar_oferta}_{nume_client}.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        logo_path = "Logo_Kuziini.png"
        export_pdf(json_data, logo_path)
        export_pdf_detaliat(json_data, logo_path)
        export_excel(json_data)

        incarca_in_github(json_data)

        st.success(f"✅ Deviz generat: {numar_oferta} | 💰 {total:.2f} RON")

# ========================
# 📂 Istoric
# ========================
afiseaza_istoric()
