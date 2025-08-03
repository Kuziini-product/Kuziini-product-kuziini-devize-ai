from fpdf import FPDF
import os

def export_pdf(json_data, logo_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 12)

    if logo_path and os.path.exists(logo_path):
        pdf.image(logo_path, 10, 8, 40)
        pdf.ln(20)

    pdf.set_font("Helvetica", "", 14)
    pdf.cell(200, 10, txt="Oferta estimativa mobilier", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(200, 10, txt=f"Client: {json_data['client']}", ln=True)
    pdf.cell(200, 10, txt=f"Telefon: {json_data['telefon']}", ln=True)
    pdf.cell(200, 10, txt=f"Oferta nr: {json_data['numar']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(60, 10, "Produs", border=1)
    pdf.cell(30, 10, "Cantitate", border=1)
    pdf.cell(30, 10, "Pret", border=1)
    pdf.cell(30, 10, "Total", border=1)
    pdf.ln()

    total_general = 0
    for item in json_data.get("items", []):
        produs = item.get("produs", "")
        cant = item.get("cantitate", 0)
        pret = item.get("pret", 0)
        total = cant * pret
        total_general += total

        pdf.cell(60, 10, str(produs), border=1)
        pdf.cell(30, 10, str(cant), border=1)
        pdf.cell(30, 10, f"{pret:.2f}", border=1)
        pdf.cell(30, 10, f"{total:.2f}", border=1)
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(200, 10, txt=f"Total estimat: {total_general:.2f} RON", ln=True)

    os.makedirs("exports", exist_ok=True)
    output_path = os.path.join("exports", f"{json_data['numar']}_{json_data['client']}.pdf")
    pdf.output(output_path)

def export_pdf_detaliat(json_data, logo_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 12)

    if logo_path and os.path.exists(logo_path):
        pdf.image(logo_path, 10, 8, 40)
        pdf.ln(20)

    pdf.set_font("Helvetica", "", 14)
    pdf.cell(200, 10, txt="Detaliere completa materiale", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(60, 10, "Produs", border=1)
    pdf.cell(30, 10, "Cantitate", border=1)
    pdf.cell(30, 10, "Pret unitar", border=1)
    pdf.cell(30, 10, "Total", border=1)
    pdf.ln()

    total_general = 0
    for item in json_data.get("items", []):
        produs = item.get("produs", "")
        cant = item.get("cantitate", 0)
        pret = item.get("pret", 0)
        total = cant * pret
        total_general += total

        pdf.cell(60, 10, str(produs), border=1)
        pdf.cell(30, 10, str(cant), border=1)
        pdf.cell(30, 10, f"{pret:.2f}", border=1)
        pdf.cell(30, 10, f"{total:.2f}", border=1)
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(200, 10, txt=f"Total estimat: {total_general:.2f} RON", ln=True)

    os.makedirs("exports", exist_ok=True)
    output_path = os.path.join("exports", f"{json_data['numar']}_{json_data['client']}_detaliat.pdf")
    pdf.output(output_path)