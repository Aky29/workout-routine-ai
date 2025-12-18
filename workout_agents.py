from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

from langchain.tools import tool

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment variables")
llm = ChatGroq(
    api_key=GROQ_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.5
)

@tool
def analyze_goal(text: str) -> str:
    """
    Tool 1:
    Analyzes the user's fitness goal and explains
    the appropriate training focus.
    """
    return llm.invoke(
        f"Analyze the fitness goal and training focus:\n{text}"
    ).content


@tool
def decide_split(text: str) -> str:
    """
    Tool 2:
    Determines the best weekly workout split
    (e.g., Push/Pull/Legs, Upper/Lower).
    """
    return llm.invoke(
        f"Create a weekly workout split based on:\n{text}"
    ).content


@tool
def suggest_exercises(text: str) -> str:
    """
    Tool 3:
    Suggests exercises based on available equipment
    and workout style.
    """
    return llm.invoke(
        f"Suggest exercises based on:\n{text}"
    ).content


@tool
def sets_and_reps(text: str) -> str:
    """
    Tool 4:
    Recommends sets, reps, and rest times based
    on goal and experience level.
    """
    return llm.invoke(
        f"Recommend sets, reps, and rest times for:\n{text}"
    ).content


TOOLS = {
    "analyze_goal": analyze_goal,
    "decide_split": decide_split,
    "suggest_exercises": suggest_exercises,
    "sets_and_reps": sets_and_reps,
}

def generate_plan(user_prompt: str) -> str:
    """
    Orchestrates all tools to generate a complete
    workout plan from a single user text prompt.
    """

    goal_analysis = TOOLS["analyze_goal"].run(user_prompt)

    split_plan = TOOLS["decide_split"].run(user_prompt)

    exercise_plan = TOOLS["suggest_exercises"].run(user_prompt)

    volume_plan = TOOLS["sets_and_reps"].run(user_prompt)

    final_prompt = f"""
You are a professional fitness coach.

User request:
{user_prompt}

Training focus:
{goal_analysis}

Weekly split:
{split_plan}

Exercise selection:
{exercise_plan}

Sets, reps, and rest:
{volume_plan}

Now combine all of the above into a single,
well-structured, easy-to-follow workout plan.
"""

    return llm.invoke(final_prompt).content
