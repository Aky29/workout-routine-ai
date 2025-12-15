from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def generate_workout_pdf(filename, data):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI Workout Plan</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    # User prompt
    story.append(Paragraph("<b>User Request:</b>", styles["Heading2"]))
    story.append(Paragraph(data["prompt"], styles["Normal"]))
    story.append(Spacer(1, 12))

    # Generated plan
    story.append(Paragraph("<b>Workout Plan:</b>", styles["Heading2"]))
    story.append(Paragraph(data["plan"].replace("\n", "<br/>"), styles["Normal"]))

    doc.build(story)
