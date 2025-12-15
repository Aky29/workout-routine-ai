from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime


def generate_workout_pdf(filename: str, data: dict):
    """
    Generates a PDF workout plan.

    data keys expected:
    - goal
    - days
    - equipment
    - level
    - plan
    """

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=A4)

    story = []

    # ---------- Title ----------
    story.append(Paragraph("<b>AI Generated Workout Plan</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    # ---------- Meta Info ----------
    story.append(
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"]
        )
    )
    story.append(Spacer(1, 10))

    story.append(Paragraph(f"<b>Goal:</b> {data['goal']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Days per Week:</b> {data['days']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Equipment:</b> {data['equipment']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Experience Level:</b> {data['level']}", styles["Normal"]))

    story.append(Spacer(1, 16))

    # ---------- Workout Plan ----------
    story.append(Paragraph("<b>Workout Plan</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    for line in data["plan"].split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 6))

    # ---------- Build PDF ----------
    doc.build(story)
