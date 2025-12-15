from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import html

def generate_workout_pdf(filename, data):
    """
    Generates a workout PDF from free-text input.
    Expected keys in `data`:
    - prompt
    - plan
    """

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("AI Workout Plan", styles["Title"]))
    story.append(Spacer(1, 0.3 * inch))

    # User Prompt
    story.append(Paragraph("<b>User Request</b>", styles["Heading2"]))
    story.append(Spacer(1, 0.1 * inch))
    user_prompt = html.escape(data.get("prompt", ""))
    story.append(Paragraph(user_prompt.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Generated Plan
    story.append(Paragraph("<b>Generated Workout Plan</b>", styles["Heading2"]))
    story.append(Spacer(1, 0.1 * inch))
    plan_text = html.escape(data.get("plan", ""))
    story.append(Paragraph(plan_text.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(story)
