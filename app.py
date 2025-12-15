import streamlit as st
from workout_agents import generate_plan
from pdf_utils import generate_workout_pdf

st.set_page_config(
    page_title="AI Workout Split Generator",
    page_icon="🏋️",
    layout="centered"
)

st.title("🏋️ AI Workout Split Generator")
st.write("Describe your fitness goal in your own words")

# ---------------- TEXT INPUT ---------------- #
user_prompt = st.text_area(
    "💬 Tell me about your workout needs",
    placeholder=(
        "Example:\n"
        "I want a 4 day muscle gain workout using dumbbells. "
        "I am an intermediate lifter and want 60 minute sessions."
    ),
    height=160
)

generate = st.button("Generate Workout 💪")

# ---------------- GENERATION ---------------- #
if generate:
    if not user_prompt.strip():
        st.warning("Please describe your workout requirements.")
    else:
        with st.spinner("AI agents are building your workout..."):
            plan = generate_plan(
                goal="auto",
                days="auto",
                equipment="auto",
                level="auto"
            )

        st.success("Workout Plan Generated!")
        st.markdown("## 📋 Your Personalized Plan")
        st.markdown(plan)

        # ---------------- PDF EXPORT ---------------- #
        pdf_data = {
            "user_prompt": user_prompt,
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
