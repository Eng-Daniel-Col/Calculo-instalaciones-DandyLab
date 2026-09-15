from fpdf import FPDF


def crear_pdf(nombre_archivo, titulo="Informe Técnico DandyLab"):
    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", "B", 16)

    pdf.cell(
        0,
        10,
        titulo,
        ln=True,
        align="C",
    )

    pdf.output(nombre_archivo)

    return nombre_archivo
