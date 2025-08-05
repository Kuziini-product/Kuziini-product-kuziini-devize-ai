from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
        self.set_font('DejaVu', '', 12)

def export_pdf(json_data, logo_path):
    pdf = PDF()
    pdf.add_page()

    if logo_path and os.path.exists(logo_path):
        pdf.image(logo_path, 10, 8, 40)
        pdf.ln(25)

    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, txt="Ofertă estimativă mobilier", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 8, f"Client: {json_data.get('client', '')}", ln=True)
    pdf.cell(0, 8, f"Telefon: {json_data.get('telefon', '')}", ln=True)
    pdf.cell(0, 8, f"Ofertă nr: {json_data.get('numar', '')}", ln=True)
    pdf.ln(6)

    # Tabel
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(80, 10, "Produs", border=1)
    pdf.cell(30, 10, "Cantitate", border=1, align='C')
    pdf.cell(30, 10, "Preț", border=1, align='C')
    pdf.cell(40, 10, "Valoare", border=1, align='C')
    pdf.ln()

    pdf.set_font("DejaVu", "", 11)
    total_general = 0
    for item in json_data.get("items", []):
        produs = str(item.get("produs", ""))
        cant = item.get("cantitate", 0)
        pret = item.get("pret", 0.0)
        valoare = cant * pret
        total_general += valoare

        pdf.cell(80, 8, produs, border=1)
        pdf.cell(30, 8, str(cant), border=1, align='C')
        pdf.cell(30, 8, f"{pret:.2f}", border=1, align='R')
        pdf.cell(40, 8, f"{valoare:.2f}", border=1, align='R')
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(140, 10, "Total estimat:", align='R')
    pdf.cell(40, 10, f"{total_general:.2f} RON", border=1, align='R')

    os.makedirs("exports", exist_ok=True)
    output_path = os.path.join("exports", f"{json_data['numar']}_{json_data['client']}.pdf")
    pdf.output(output_path)


def export_pdf_detaliat(json_data, logo_path):
    pdf = PDF()
    pdf.add_page()

    if logo_path and os.path.exists(logo_path):
        pdf.image(logo_path, 10, 8, 40)
        pdf.ln(25)

    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, txt="Detaliere completă materiale", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 8, f"Client: {json_data.get('client', '')}", ln=True)
    pdf.cell(0, 8, f"Telefon: {json_data.get('telefon', '')}", ln=True)
    pdf.cell(0, 8, f"Ofertă nr: {json_data.get('numar', '')}", ln=True)
    pdf.ln(6)

    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(80, 10, "Produs", border=1)
    pdf.cell(30, 10, "Cantitate", border=1, align='C')
    pdf.cell(30, 10, "Preț unitar", border=1, align='C')
    pdf.cell(40, 10, "Valoare", border=1, align='C')
    pdf.ln()

    pdf.set_font("DejaVu", "", 11)
    total_general = 0
    for item in json_data.get("items", []):
        produs = str(item.get("produs", ""))
        cant = item.get("cantitate", 0)
        pret = item.get("pret", 0.0)
        valoare = cant * pret
        total_general += valoare

        pdf.cell(80, 8, produs, border=1)
        pdf.cell(30, 8, str(cant), border=1, align='C')
        pdf.cell(30, 8, f"{pret:.2f}", border=1, align='R')
        pdf.cell(40, 8, f"{valoare:.2f}", border=1, align='R')
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(140, 10, "Total estimat:", align='R')
    pdf.cell(40, 10, f"{total_general:.2f} RON", border=1, align='R')

    os.makedirs("exports", exist_ok=True)
    output_path = os.path.join("exports", f"{json_data['numar']}_{json_data['client']}_detaliat.pdf")
    pdf.output(output_path)
