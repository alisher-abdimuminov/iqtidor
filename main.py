# # import numpy as np
# # import pandas as pd

# # df = pd.read_json("results.json").T
# # # df.columns = df.columns.astype(int)
# # df = df.reindex(sorted(df.columns), axis=1)

# # question_cols = [c for c in df.columns if isinstance(c, int)]

# # df["correct_answers"] = df[question_cols].sum(axis=1).astype(int)
# # df["ratio_of_total_questions"] = (df["correct_answers"] / 43) * 100
# # df["according_to_the_answers_found"] = (df["correct_answers"] / 42) * 100

# # mean_val = df["correct_answers"].mean()
# # std_val = df["correct_answers"].std(ddof=1)
# # df["deviation"] = 0 if std_val == 0 else (df["correct_answers"] - mean_val) / std_val

# # avg_per_q = df.loc[:, question_cols].mean(axis=0)

# # def difficulty_fn(x):
# #     if x < 0.5:
# #         return 3
# #     elif x <= 0.75:
# #         return 2
# #     else:
# #         return 1

# # difficulty_row = pd.Series(np.nan, index=df.columns)
# # difficulty_row.loc[question_cols] = avg_per_q.apply(difficulty_fn).astype("Int64").values

# # df.loc["difficulty"] = difficulty_row

# # difficulty_vals = df.loc["difficulty", question_cols]

# # df["by_difficulty_level"] = df[question_cols].apply(
# #     lambda row: ((row == 1) * difficulty_vals).sum(), axis=1
# # )

# # df["rash"] = (df["by_difficulty_level"] / 65) * 100

# # def degree_fn(rash):
# #     if rash > 70:
# #         return "A+"
# #     elif rash >= 65:
# #         return "A"
# #     elif rash >= 60:
# #         return "B+"
# #     elif rash >= 55:
# #         return "B"
# #     elif rash >= 50:
# #         return "C+"
# #     elif rash >= 46:
# #         return "C"
# #     else:
# #         return "F"

# # df["degree"] = df["rash"].apply(lambda x: degree_fn(x) if pd.notnull(x) else np.nan)

# # df.loc["difficulty", ["by_difficulty_level", "rash", "degree"]] = np.nan

# # df = df.sort_values(by="correct_answers", ascending=False)

# # df.to_json("final.json", indent=4)
# # df.to_excel("final.xlsx")

# # print(df["correct_answers"].to_dict())


# # # correct_answers = 35
# # # overall = (correct_answers / 43) * 100
# # # findded_answers = (correct_answers / 42) * 100
# # # deviation = (correct_answers - np.avg(all)) / np.std(all)



# # services/certificate_generator.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from django.core.files.base import ContentFile
import math


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


def generate_certificate(data: dict) -> bytes:
    c = canvas.Canvas("answers.pdf", pagesize=A4)
    width, height = A4

    c.setFillColorRGB(0.95, 0.90, 0.80)  # och jigarrang (RGB)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    draw_hex_grid(c, width, height, size=20)

    c.setLineWidth(2)
    c.setStrokeColor(colors.black)
    margin = 10
    c.rect(margin, margin, width - 2*margin, height - 2*margin, stroke=1, fill=0)


    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 18)

    if data.get("emblem_path"):
        c.drawImage(data["emblem_path"], width/2 - 20*mm, height - 45*mm, width=40*mm, height=40*mm, preserveAspectRatio=True, mask="auto")

    # Sarlavha
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 50*mm, "Iqtidor Academy")

    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width/2, height - 60*mm, "UMUMTA'LIM FANINI BILISH DARAJASI TO'G'RISIDA SERTIFIKAT")

    # Asosiy ma'lumotlar
    y = height - 100*mm
    c.setFont("Helvetica", 11)
    c.drawString(30*mm, y, f"Sertifikat raqami: {data['sertifikat_raqam']}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Talabaning shaxsiy kodi: {data['talaba_kodi']}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Familiyasi: {data['familiya']}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Ismi: {data['ismi']}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Otasining ismi: {data['otasining_ismi']}")

    # O'ng tomonda rasm
    if data.get("photo_path"):
        c.drawImage(data["photo_path"], width - 50*mm, height - 120*mm, width=25*mm, height=30*mm, preserveAspectRatio=True, mask="auto")

    # Ball va foiz
    y -= 50*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30*mm, y, f"Umumta'lim fani: {data['fan']}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Umumiy to'plagan ball: {data['ball']}")
    y -= 8*mm
    c.drawString(30*mm, y, f"Umumiy ballga nisbatan foiz ko'rsatkichi: {data['foiz']} %")
    y -= 8*mm
    c.drawString(30*mm, y, f"Sertifikat darajasi: {data['daraja']}")

    # Sana va imzo
    y -= 60*mm
    c.drawString(30*mm, y, f"Berilgan sanasi: {data['sana']}")

    c.setFont("Helvetica", 10)
    c.drawString(width - 60*mm, y, f"Direktor: {data['direktor']}")

    c.showPage()
    c.save()
    # pdf_bytes = buffer.getvalue()
    # buffer.close()
    # return pdf_bytes


data = {
        "sertifikat_raqam": "UZ25 360967",
        "talaba_kodi": "52203096030035",
        "familiya": "MURATOV",
        "ismi": "ASILBEK",
        "otasining_ismi": "ILLYOSOVICH",
        "fan": "Biologiya (O'zbek)",
        "ball": "61.6",
        "foiz": "94.77",
        "daraja": "B+",
        "bolimlar": [
            ("Sitologiya asoslari", 16.367),
            ("Genetika va seleksiya asoslari", 8.184),
            ("Organizmlarning xilma-xilligi", 20.459),
            ("Evolutsiya, ekologiya va biosfera asoslar", 10.23),
            ("Test natijasi", 67.96),
            ("Yozma ish", 55.24),
        ],
        "sana": "30.05.2025",
        "muddat": "29.05.2028",
        "direktor": "S.Sultonov",
        "emblem_path": "bgless.png",
        "photo_path": "bgless.png",
    }


generate_certificate(data)


# Grouped layout PDF: adds section headings and prints questions within each group
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

PAGE_W, PAGE_H = A4

# Colors
Bg = colors.Color(255/255, 245/255, 242/255)
Border = colors.Color(233/255, 84/255, 62/255)
Ink = colors.Color(28/255, 35/255, 45/255)
Hint = colors.Color(230/255, 150/255, 140/255)
Good = colors.Color(16/255, 158/255, 72/255)
Bad = colors.Color(214/255, 40/255, 40/255)

answers_csv = """D,D,C,D,A,B,C,B,A,D,C,D,A,B,C,A,C,B,D,A,
C,B,D,B,A,C,D,C,B,A,C,A,B,D,A,C,B,D,A,C,
D,D,C,D,A,B,C,B,A,D,C,D,A,B,C,A,C,B,D,A,
C,B,D,B,A,C,D,C,B,A, C,B,D,B,A,C,D,C,B,A, C,B,D,B,A,C,D,C,B,F"""
keys_csv = """D,D,C,D,A,B,C,B,A,D,C,D,A,B,C,A,C,B,D,A,
C,B,D,B,A,C,D,C,B,A,C,A,B,D,A,C,B,D,A,C,
D,D,C,D,A,B,C,B,A,D,C,D,A,B,C,A,C,B,D,A,
C,B,D,B,A,C,D,C,B,A, C,B,D,B,A,C,D,C,B,F, C,B,D,B,A,C,D,C,B,A"""

def parse_csv(s):
    return [p.strip() for p in s.replace("\n", "").split(",") if p.strip() != ""]

answers = parse_csv(answers_csv)
keys = parse_csv(keys_csv)
n = min(len(answers), len(keys))

student_name = "Alisher Abdimuminov"
total_score = "167.4"
test_date = "12/02/2025"

# Groups: (Title, start, end) inclusive (1-based indices)
groups = [
    ("Ona tili", 1, 10),
    ("Tarix", 11, 20),
    ("Matematika", 21, 30),
    ("Fizika", 31, 60),
    ("Kimyo", 61, 90),
]

MARGIN = 8*mm
PADDING = 10*mm

out_path = "answers_grouped.pdf"
c = canvas.Canvas(out_path, pagesize=A4)

# Background
c.setFillColor(colors.white)
c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

# Header with logo
header_h = 18*mm  # a bit taller to fit logo
c.setFillColor(Border)
c.rect(0, PAGE_H - header_h, PAGE_W, header_h, stroke=0, fill=1)

# Try to draw logo on the left
logo_path = "logo.png"  # <-- place your logo here
logo_w = 14*mm
logo_h = 14*mm
logo_x = MARGIN
logo_y = PAGE_H - header_h + (header_h - logo_h)/2

if os.path.exists(logo_path):
    c.drawImage(logo_path, logo_x, logo_y, width=logo_w, height=logo_h, mask='auto')
else:
    # Placeholder if no logo file
    c.setFillColor(colors.white)
    c.roundRect(logo_x, logo_y, logo_w, logo_h, 3*mm, stroke=0, fill=1)
    c.setFillColor(Bg)
    c.roundRect(logo_x+1, logo_y+1, logo_w-2, logo_h-2, 3*mm, stroke=1, fill=0)
    c.setFillColor(Ink)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(logo_x + logo_w/2, logo_y + logo_h/2 - 3, "LOGO")

# Title centered (accounting for logo space; still using centered draw for simplicity)
c.setFillColor(colors.white)
c.setFont("Helvetica-Bold", 20)
c.drawCentredString(PAGE_W/2, PAGE_H - header_h/2 - 6, "Iqtidor Academy")

# Identity block
c.setFillColor(Ink)
c.setFont("Helvetica-Bold", 12)
y = PAGE_H - header_h - 10*mm
c.drawString(MARGIN, y, "Test topshiruvchi: ")
c.setFont("Helvetica", 12)
c.drawString(MARGIN + 40*mm, y, student_name)

y -= 7*mm
c.setFont("Helvetica-Bold", 12)
c.drawString(MARGIN, y, "Umumiy ball: ")
c.setFont("Helvetica", 12)
c.drawString(MARGIN + 40*mm, y, total_score)

y -= 7*mm
c.setFont("Helvetica-Bold", 12)
c.drawString(MARGIN, y, "Test sanasi: ")
c.setFont("Helvetica", 12)
c.drawString(MARGIN + 40*mm, y, test_date)

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
    global col, y_cursor
    col += 1
    y_cursor = inner_top

def ensure_space(lines_needed=1):
    global col, y_cursor
    y_needed = lines_needed * line_h
    if y_cursor - y_needed < inner_bottom:
        new_column()

def draw_heading(title):
    global y_cursor
    # If near bottom, move to next column before printing heading
    ensure_space(5)
    c.setFillColor(Border)
    c.setFont("Helvetica", 10)
    x = inner_left + col * col_w + 10
    y_cursor -= heading_gap_above
    c.drawString(x, y_cursor, title)
    y_cursor -= heading_gap_below + 4

def draw_row(idx1):
    global y_cursor
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

out_path
