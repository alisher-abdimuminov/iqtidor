import io
import math
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.core.files.base import ContentFile


def draw_hex_grid(c, width, height, size=15):
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.setLineWidth(1)
    dx = size * math.sqrt(3)
    dy = size * 1.5
    rows = int(height / dy) + 2
    cols = int(width / dx) + 2
    for row in range(rows):
        for col in range(cols):
            x = col * dx + (row % 2) * (dx / 2)
            y = row * dy
            draw_hexagon(c, x, y, size)


def draw_hexagon(c, x, y, size):
    points = []
    for i in range(6):
        angle = math.pi / 3 * i
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.append((px, py))
    path = c.beginPath()
    path.moveTo(*points[0])
    for p in points[1:]:
        path.lineTo(*p)
    path.close()
    c.drawPath(path, stroke=1, fill=0)


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

    draw_hex_grid(c, width, height, size=20)

    c.setLineWidth(2)
    c.setStrokeColor(colors.black)
    margin = 10
    c.rect(margin, margin, width - 2*margin, height - 2*margin, stroke=1, fill=0)


    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 18)

    c.drawImage(logo, width/2 - 20*mm, height - 45*mm, width=40*mm, height=40*mm, preserveAspectRatio=True, mask="auto")

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 50*mm, "Iqtidor Academy")

    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width/2, height - 60*mm, "UMUMTA'LIM FANINI BILISH DARAJASI TO'G'RISIDA SERTIFIKAT")

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

