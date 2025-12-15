from dotenv import load_dotenv
import os

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

# ---------- SHARED LLM ----------
from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key=GROQ_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.5
)

# ---------- TOOLS ----------
from langchain.tools import tool

@tool
def goal_analysis(goal: str) -> str:
    """Analyze the user's fitness goal and provide training focus."""
    return llm.invoke(f"Explain training focus for: {goal}").content


@tool
def workout_split(days: str) -> str:
    """Generate a weekly workout split based on the number of workout days."""
    return llm.invoke(f"Create a {days}-day workout split").content


@tool
def exercise_selector(day_and_equipment: str) -> str:
    """Suggest exercises for a workout day based on equipment."""
    day, equipment = day_and_equipment.split("|")
    return llm.invoke(
        f"Suggest exercises for {day.strip()} with {equipment.strip()}"
    ).content


@tool
def sets_reps(goal_and_level: str) -> str:
    """Suggest sets and rep
