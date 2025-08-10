import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

PAGE_W, PAGE_H = A4


Bg = colors.Color(255/255, 245/255, 242/255)
Border = colors.Color(233/255, 84/255, 62/255)
Ink = colors.Color(28/255, 35/255, 45/255)
Hint = colors.Color(230/255, 150/255, 140/255)
Good = colors.Color(16/255, 158/255, 72/255)
Bad = colors.Color(214/255, 40/255, 40/255)


def parse_csv(s):
    return [p.strip() for p in s.replace("\n", "").split(",") if p.strip() != ""]

def generate_answers_sheet(
    answers: str,
    keys: str,
    student: str,
    score: str,
    date: str,
    groups: tuple
):
    answers = parse_csv(answers)
    keys = parse_csv(keys)
    n = min(len(answers), len(keys))

    MARGIN = 8*mm
    PADDING = 10*mm

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Background
    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    header_h = 18*mm
    c.setFillColor(Border)
    c.rect(0, PAGE_H - header_h, PAGE_W, header_h, stroke=0, fill=1)

    logo_path = "logo.png"
    logo_w = 14*mm
    logo_h = 14*mm
    logo_x = MARGIN
    logo_y = PAGE_H - header_h + (header_h - logo_h)/2

    c.drawImage(logo_path, logo_x, logo_y, width=logo_w, height=logo_h, mask='auto')

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(PAGE_W/2, PAGE_H - header_h/2 - 6, "Iqtidor Academy")


    c.setFillColor(Ink)
    c.setFont("Helvetica-Bold", 12)
    y = PAGE_H - header_h - 10*mm
    c.drawString(MARGIN, y, "Test topshiruvchi: ")
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN + 40*mm, y, student)

    y -= 7*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Umumiy ball: ")
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN + 40*mm, y, f"{score}")

    y -= 7*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Test sanasi: ")
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN + 40*mm, y, date)

    # Answer box
    box_top = y - 6*mm
    box_bottom = 10*mm
    box_left = MARGIN
    box_right = PAGE_W - MARGIN
    radius = 4*mm
    c.setFillColor(Bg)
    c.setStrokeColor(Border)
    c.setLineWidth(1)
    c.roundRect(box_left, box_bottom, box_right - box_left, box_top - box_bottom, radius, stroke=1, fill=1)

    # Title inside box
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(Ink)
    c.drawCentredString((box_left + box_right)/2, box_top - 10*mm, "Javoblar vaqarasi")

    # Layout
    inner_left = box_left + PADDING
    inner_right = box_right - PADDING
    inner_top = box_top - 16*mm
    inner_bottom = box_bottom + PADDING

    col_count = 3
    col_w = (inner_right - inner_left) / col_count
    line_h = 6.5*mm
    heading_gap_above = 3*mm
    heading_gap_below = 2*mm

    def draw_bubbles(cx, cy, selected_letter):
        r = 1.9*mm
        gap = 4.2*mm
        x = cx
        for letter in ["A", "B", "C", "D"]:
            c.setLineWidth(0.4)
            c.setStrokeColor(Hint)
            c.setFillColor(Bg)
            c.circle(x, cy, r, stroke=1, fill=1)
            if letter.upper() == selected_letter.upper():
                c.setFillColor(Ink)
                c.circle(x, cy, r, stroke=0, fill=1)
            x += gap

    def draw_mark_near_answer(x, y, ok_flag):
        c.setFont("Helvetica", 9)
        c.setFillColor(Good if ok_flag else Bad)
        c.drawString(x, y, "✓" if ok_flag else "✗")

    # Cursor state
    col = 0
    y_cursor = inner_top

    def new_column():
        nonlocal col, y_cursor
        col += 1
        y_cursor = inner_top

    def ensure_space(lines_needed=1):
        nonlocal col, y_cursor
        y_needed = lines_needed * line_h
        if y_cursor - y_needed < inner_bottom:
            new_column()

    def draw_heading(title):
        nonlocal y_cursor
        # If near bottom, move to next column before printing heading
        ensure_space(5)
        c.setFillColor(Border)
        c.setFont("Helvetica", 10)
        x = inner_left + col * col_w + 10
        y_cursor -= heading_gap_above
        c.drawString(x, y_cursor, title)
        y_cursor -= heading_gap_below + 4

    def draw_row(idx1):
        nonlocal y_cursor
        x0 = inner_left + col * col_w
        y0 = y_cursor

        # number with extra gap to bubbles
        c.setFillColor(Ink)
        c.setFont("Helvetica", 9)
        c.drawRightString(x0 + 8*mm, y0, str(idx1))

        # bubbles
        draw_bubbles(x0 + 12*mm, y0+1.1*mm, answers[idx1-1])

        # "n."
        c.setFillColor(Ink)
        c.setFont("Helvetica", 9)
        c.drawRightString(x0 + 40*mm, y0, f"{idx1}.")

        # answer letter
        c.setFillColor(Ink)
        c.setFont("Helvetica-Bold", 10)
        ans_x = x0 + 44*mm
        c.drawString(ans_x, y0, answers[idx1-1])

        # mark
        is_ok = answers[idx1-1].upper() == keys[idx1-1].upper()
        mark_x = ans_x + 5*mm
        draw_mark_near_answer(mark_x, y0, is_ok)

        y_cursor -= line_h

    # Render groups
    for title, start, end in groups:
        draw_heading(title)
        for i in range(start, end+1):
            ensure_space(0.5)
            draw_row(i)

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
