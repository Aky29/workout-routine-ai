import streamlit as st
from workout_agents import generate_plan
from pdf_utils import generate_workout_pdf

st.set_page_config(
    page_title="AI Workout Split Generator",
    page_icon="🏋️",
    layout="centered"
)

st.title("🏋️ AI Workout Split Generator")
st.write("Personalized workouts powered by AI agents")

# ---------------- FORM ---------------- #
with st.form("workout_form"):
    goal = st.selectbox(
        "🎯 Fitness Goal",
        ["Muscle Gain", "Fat Loss", "Strength", "General Fitness"]
    )

    days = st.selectbox(
        "📅 Days Per Week",
        ["3", "4", "5", "6"]
    )

    equipment = st.selectbox(
        "🏋️ Equipment Available",
        ["Bodyweight", "Dumbbells", "Barbell", "Full Gym"]
    )

    level = st.selectbox(
        "📈 Experience Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    submit = st.form_submit_button("Generate Workout 💪")

# ---------------- GENERATION ---------------- #
if submit:
    with st.spinner("AI agents are building your workout..."):
        plan = generate_plan(goal, days, equipment, level)

    st.success("Workout Plan Generated!")
    st.markdown("## 📋 Your Personalized Plan")
    st.markdown(plan)

    # ---------------- PDF EXPORT ---------------- #
    pdf_data = {
        "goal": goal,
        "days": days,
        "equipment": equipment,
        "level": level,
        "plan": plan
    }

    pdf_filename = "workout_plan.pdf"
    generate_workout_pdf(pdf_filename, pdf_data)

    with open(pdf_filename, "rb") as f:
        st.download_button(
            label="📄 Download Workout Plan (PDF)",
            data=f,
            file_name="AI_Workout_Plan.pdf",
            mime="application/pdf"
        )
