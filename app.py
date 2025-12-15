import streamlit as st
from workout_agents import generate_plan
from pdf_utils import generate_workout_pdf

st.set_page_config(
    page_title="AI Workout Split Generator",
    page_icon="🏋️",
    layout="centered"
)

st.title("🏋️ AI Workout Split Generator")
st.write("Describe your workout requirements in your own words")

user_prompt = st.text_area(
    "💬 Your workout request",
    placeholder=(
        "Example:\n"
        "I want a 5 day muscle gain workout using full gym equipment. "
        "I am intermediate and want 60 minute sessions."
    ),
    height=160
)

if st.button("Generate Workout 💪"):
    if not user_prompt.strip():
        st.warning("Please enter your workout details.")
    else:
        with st.spinner("AI tools are building your workout..."):
            plan = generate_plan(user_prompt)

        st.success("Workout Plan Generated!")
        st.markdown("## 📋 Your Personalized Plan")
        st.markdown(plan)

        pdf_filename = "workout_plan.pdf"
        generate_workout_pdf(pdf_filename, {
            "prompt": user_prompt,
            "plan": plan
        })

        with open(pdf_filename, "rb") as f:
            st.download_button(
                "📄 Download Workout Plan (PDF)",
                f,
                file_name="AI_Workout_Plan.pdf",
                mime="application/pdf"
            )
