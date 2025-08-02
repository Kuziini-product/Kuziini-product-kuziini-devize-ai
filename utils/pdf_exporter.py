from fpdf import FPDF

def export_pdf(json_data, logo_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'utils/fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.image(logo_path, 10, 8, 40)
    pdf.ln(20)
    pdf.cell(200, 10, txt=f"Deviz estimativ - {json_data['numar']}", ln=True)
    pdf.cell(200, 10, txt=f"Client: {json_data['client']}", ln=True)
    pdf.cell(200, 10, txt=f"Telefon: {json_data['telefon']}", ln=True)
    pdf.cell(200, 10, txt=f"Dimensiuni: {json_data['dimensiuni']}", ln=True)
    pdf.ln(10)

    for item in json_data["items"]:
        pdf.cell(200, 10, txt=f"{item['produs']} x {item['cantitate']} = {item['subtotal']} RON", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total: {json_data['valoare']:.2f} RON", ln=True)

    pdf.output(f"exports/{json_data['numar']}_{json_data['client']}.pdf")


def export_pdf_detaliat(json_data, logo_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'utils/fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.image(logo_path, 10, 8, 40)
    pdf.ln(20)
    pdf.cell(200, 10, txt=f"Deviz detaliat - {json_data['numar']}", ln=True)
    pdf.cell(200, 10, txt=f"Client: {json_data['client']}", ln=True)
    pdf.cell(200, 10, txt=f"Telefon: {json_data['telefon']}", ln=True)
    pdf.cell(200, 10, txt=f"Tip: {json_data['tip']}", ln=True)
    pdf.cell(200, 10, txt=f"Dimensiuni: {json_data['dimensiuni']}", ln=True)
    pdf.ln(10)

    for item in json_data["items"]:
        pdf.cell(200, 10, txt=f"{item['produs']} | Cod: {item['cod']} | x{item['cantitate']} @ {item['pret_unitar']} RON = {item['subtotal']} RON", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total general: {json_data['valoare']:.2f} RON", ln=True)

    pdf.add_page()
    pdf.set_font("DejaVu", size=14)
    pdf.cell(200, 10, txt="Anexa: Tabel debitare PAL (simulat)", ln=True)
    pdf.set_font("DejaVu", size=12)
    pdf.ln(5)

    debitare = [
        ("PAL alb 18mm", "600 x 400", 2, "laterale"),
        ("PAL alb 18mm", "800 x 400", 1, "poliță"),
        ("PAL alb 18mm", "600 x 800", 1, "spate")
    ]

    for placa, dim, cant, obs in debitare:
        pdf.cell(200, 10, txt=f"{placa} | {dim} mm | x{cant} | {obs}", ln=True)

    pdf.output(f"exports/{json_data['numar']}_{json_data['client']}_detaliat.pdf")
