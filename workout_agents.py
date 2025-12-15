from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.tools import tool

# ---------------- ENV ----------------
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY not found")

# ---------------- LLM ----------------
llm = ChatGroq(
    api_key=GROQ_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.5
)

# ---------------- TOOLS ----------------

@tool
def analyze_goal(text: str) -> str:
    """Analyze the user's fitness goal and explain training focus."""
    return llm.invoke(
        f"Analyze the fitness goal and training focus:\n{text}"
    ).content


@tool
def decide_split(text: str) -> str:
    """Decide an appropriate weekly workout split."""
    return llm.invoke(
        f"Create a weekly workout split based on:\n{text}"
    ).content


@tool
def suggest_exercises(text: str) -> str:
    """Suggest exercises based on equipment and workout type."""
    return llm.invoke(
        f"Suggest exercises based on:\n{text}"
    ).content


@tool
def sets_and_reps(text: str) -> str:
    """Recommend sets, reps, and rest times."""
    return llm.invoke(
        f"Recommend sets, reps, and rest times for:\n{text}"
    ).content


TOOLS = {
    "analyze_goal": analyze_goal,
    "decide_split": decide_split,
    "suggest_exercises": suggest_exercises,
    "sets_and_reps": sets_and_reps,
}

# ---------------- MAIN FUNCTION ----------------

def generate_plan(user_prompt: str) -> str:
    """
    Generate a workout plan using tools WITHOUT LangChain agents.
    """

    goal = TOOLS["analyze_goal"].run(user_prompt)
    split = TOOLS["decide_split"].run(user_prompt)
    exercises = TOOLS["suggest_exercises"].run(user_prompt)
    volume = TOOLS["sets_and_reps"].run(user_prompt)

    final_prompt = f"""
You are a professional fitness coach.

User request:
{user_prompt}

Training focus:
{goal}

Weekly split:
{split}

Exercises:
{exercises}

Sets and reps:
{volume}

Now combine everything into ONE clean, structured workout plan.
"""

    return llm.invoke(final_prompt).content
