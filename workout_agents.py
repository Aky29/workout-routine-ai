from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

# Initialize LLM
llm = ChatGroq(api_key=GROQ_KEY, model="llama-3.1-8b-instant", temperature=0.5)

# ---------------- TOOLS ---------------- #

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
    """
    Suggest exercises for a workout day based on available equipment.
    Input format: 'Day Type | Equipment'
    """
    day, equipment = day_and_equipment.split("|")
    return llm.invoke(f"Suggest exercises for {day.strip()} with {equipment.strip()}").content


@tool
def sets_reps(goal_and_level: str) -> str:
    """
    Suggest sets and reps for each exercise based on fitness goal and experience level.
    Input format: 'Goal | Level'
    """
    goal, level = goal_and_level.split("|")
    return llm.invoke(f"Suggest sets and reps for {goal.strip()}, level {level.strip()}").content


# ---------------- AGENT ---------------- #

tools = [goal_analysis, workout_split, exercise_selector, sets_reps]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)


# ---------------- ENTRY FUNCTION ---------------- #

def generate_plan(goal, days, equipment, level):
    """
    Generate a full workout plan using Groq LLM agent.
    Includes weekly split, exercises per day, and sets/reps guidance.
    """
    prompt = f"""
    Create a complete workout plan.
    Goal: {goal}
    Days: {days}
    Equipment: {equipment}
    Experience Level: {level}
    """
    return agent.run(prompt)
