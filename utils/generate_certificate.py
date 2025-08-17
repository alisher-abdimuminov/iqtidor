import io
import math
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.core.files.base import ContentFile


def generate_certificate(
    logo: str,
    first_name: str,
    last_name: str,
    middle_name: str,
    phone: str,
    photo: str,
    id: str,
    subject: str,
    points: str,
    percentage: str,
    degree: str,
    date: str,
    director: str,
):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    bg_path = "new_bg.jpg"
    c.drawImage(bg_path, 0, 0, width=width, height=height, mask="auto")

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 18)

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 83 * mm, "Iqtidor Academy")

    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(
        width / 2,
        height - 93 * mm,
        "UMUMTA'LIM FANINI BILISH DARAJASI TO'G'RISIDA SERTIFIKAT",
    )

    y = height - 130 * mm
    c.setFont("Helvetica", 15)
    c.drawString(30 * mm, y, f"Sertifikat raqami: {id}")
    y -= 8 * mm
    c.drawString(30 * mm, y, f"Talabaning shaxsiy kodi: {phone}")
    y -= 8 * mm
    c.drawString(30 * mm, y, f"Familiyasi: {first_name}")
    y -= 8 * mm
    c.drawString(30 * mm, y, f"Ismi: {last_name}")
    y -= 8 * mm
    c.drawString(30 * mm, y, f"Otasining ismi: {middle_name}")

    # c.drawImage(
    #     photo,
    #     width - 50 * mm,
    #     height - 120 * mm,
    #     width=25 * mm,
    #     height=30 * mm,
    #     preserveAspectRatio=True,
    #     mask="auto",
    # )

    y -= 30 * mm
    c.setFont("Helvetica-Bold", 15)
    c.drawString(30 * mm, y, f"Umumta'lim fani: {subject}")
    y -= 8 * mm
    c.drawString(30 * mm, y, f"Umumiy to'plagan ball: {points}")
    y -= 8 * mm
    c.drawString(
        30 * mm, y, f"Umumiy ballga nisbatan foiz ko'rsatkichi: {percentage} %"
    )
    y -= 8 * mm
    c.drawString(30 * mm, y, f"Sertifikat darajasi: {degree}")

    c.setFont("Helvetica", 12)
    y -= 60 * mm
    c.drawString(30 * mm, y, f"Berilgan sanasi: {date}")

    c.setFont("Helvetica", 12)
    c.drawString(width - 60 * mm, y, f"Direktor: {director}")

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
