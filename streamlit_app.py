import streamlit as st
from pathlib import Path
import json
from datetime import datetime
import fitz
from PIL import Image
import io

from utils.openai_utils import genereaza_deviz_AI
from utils.pdf_exporter import export_pdf, export_pdf_detaliat
from utils.excel_exporter import export_excel
from utils.github_uploader import incarca_in_github
from utils.ocr_online import extrage_dimensiuni_ocr_space
from utils.gpt_dimension_extractor import extrage_dimensiuni_cu_gpt
from components.header import afiseaza_header
from components.history_slider import afiseaza_istoric

# ========= CONFIGURARE =========
st.set_page_config(page_title="Kuziini | Generator Devize AI", layout="wide")
afiseaza_header()

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
numar_oferte = len(list(output_dir.glob("OF-*.json")))
st.markdown(f"📊 Devize generate: **{numar_oferte}**")

# ========== UPLOAD ==========
uploaded_file = st.file_uploader("📤 Încarcă o schiță (PDF, JPG, PNG)", type=None)
inaltime = latime = adancime = 100
dims = {"înălțime": None, "lățime": None, "adâncime": None}
text = ""

if uploaded_file:
    file_type = uploaded_file.type
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

        st.text_area("📋 Text extras din imagine/PDF (OCR brut)", text, height=200)

        if text == "Eroare OCR" or not any(dims.values()):
            st.warning("⚠️ OCR a eșuat. Încercăm extragere AI cu GPT...")
            dims = extrage_dimensiuni_cu_gpt(text if text != "Eroare OCR" else "")

        st.success("✅ Dimensiuni extrase inteligent:")
        st.write(dims)

        if dims["înălțime"]: inaltime = dims["înălțime"]
        if dims["lățime"]: latime = dims["lățime"]
        if dims["adâncime"]: adancime = dims["adâncime"]

# ========== FORMULAR ==========
col1, col2 = st.columns(2)
with col1:
    nume_client = st.text_input("Nume client", value=st.session_state.get("nume_client", ""))
with col2:
    telefon_client = st.text_input("Telefon client", value=st.session_state.get("telefon_client", ""))

col1, col2, col3 = st.columns(3)
with col1:
    inaltime = st.number_input("Înălțime (mm)", min_value=100, value=st.session_state.get("înălțime", inaltime))
with col2:
    latime = st.number_input("Lățime (mm)", min_value=100, value=st.session_state.get("lățime", latime))
with col3:
    adancime = st.number_input("Adâncime (mm)", min_value=100, value=st.session_state.get("adâncime", adancime))

tipuri_dulap = [
    "dulap de dressing", "dulap bucătărie bază", "dulap bucătărie suspendat",
    "dulap colț bază", "dulap colț suspendat", "poliță", "consolă"
]
tip_dulap = st.selectbox(
    "Tip dulap",
    tipuri_dulap,
    index=tipuri_dulap.index(st.session_state["tip_dulap"]) if "tip_dulap" in st.session_state else 0
)

prompt_descriere = st.text_area("Descriere scurtă (ex: culoare PAL, preferințe)", value=st.session_state.get("prompt_descriere", ""))

# ========== GENERARE ==========
if st.button("🔧 Generează ofertă"):
    with st.spinner("Se generează devizul..."):
        dimensiuni = {"înălțime": inaltime, "lățime": latime, "adâncime": adancime}
        json_data = genereaza_deviz_AI(
            tip_dulap, dimensiuni, prompt_descriere, nume_client, telefon_client
        )

        numar_oferta = f"OF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        json_data["numar"] = numar_oferta
        json_data["client"] = nume_client
        json_data["telefon"] = telefon_client
        json_data["dimensiuni"] = dimensiuni
        json_data["tip_dulap"] = tip_dulap
        json_data["descriere"] = prompt_descriere

        total = 0.0
        for item in json_data.get("items", []):
            pret = item.get("preț") or item.get("pret") or 100
            cant = item.get("cantitate") or 1
            try:
                total += float(pret) * float(cant)
            except:
                total += 100
        json_data["valoare_total"] = round(total, 2)

        history_path = Path("history")
        history_path.mkdir(exist_ok=True)
        with open(history_path / f"{numar_oferta}_{nume_client}.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        logo_path = "Logo_Kuziini.png"
        export_pdf(json_data, logo_path)
        export_pdf_detaliat(json_data, logo_path)
        export_excel(json_data)
        incarca_in_github(json_data)

        pdf_detaliat_path = f"exports/{numar_oferta}_{nume_client}_detaliat.pdf"
        with open(pdf_detaliat_path, "rb") as f:
            st.download_button(
                label="📥 Descarcă deviz detaliat PDF",
                data=f,
                file_name=f"{numar_oferta}_{nume_client}_detaliat.pdf",
                mime="application/pdf"
            )

        st.success(f"✅ Deviz generat: {numar_oferta} | 💰 {total:.2f} RON")

# ========== ISTORIC OFERTE ==========
afiseaza_istoric()
