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
        director: str
):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFillColorRGB(0.95, 0.90, 0.80)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    bg_path = "bg.png"
    c.drawImage(bg_path, 0, 0, width=width, height=height, mask='auto')

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 18)

    c.drawImage(logo, width/2 - 20*mm, height - 55*mm, width=40*mm, height=40*mm, preserveAspectRatio=True, mask="auto")

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 70*mm, "Iqtidor Academy")

    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width/2, height - 80*mm, "UMUMTA'LIM FANINI BILISH DARAJASI TO'G'RISIDA SERTIFIKAT")

    y = height - 100*mm
    c.setFont("Helvetica", 11)
    c.drawString(30*mm, y, f"Sertifikat raqami: {id}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Talabaning shaxsiy kodi: {phone}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Familiyasi: {first_name}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Ismi: {last_name}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Otasining ismi: {middle_name}")

    c.drawImage(photo, width - 50*mm, height - 120*mm, width=25*mm, height=30*mm, preserveAspectRatio=True, mask="auto")

    y -= 50*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30*mm, y, f"Umumta'lim fani: {subject}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Umumiy to'plagan ball: {points}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Umumiy ballga nisbatan foiz ko'rsatkichi: {percentage} %")
    y -= 8*mm
    c.drawString(30*mm, y, f"Sertifikat darajasi: {degree}")

    y -= 60*mm
    c.drawString(30*mm, y, f"Berilgan sanasi: {date}")

    c.setFont("Helvetica", 10)
    c.drawString(width - 60*mm, y, f"Direktor: {director}")

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

