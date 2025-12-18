from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY not found")

llm = ChatGroq(
    api_key=GROQ_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.5
)

@tool
def analyze_goal(text: str) -> str:
    """Analyze the user's fitness goal."""
    return f"Primary goal identified: {text}"

@tool
def decide_split(text: str) -> str:
    """Decide weekly workout split."""
    return "Suggested split: Push/Pull/Legs or Upper/Lower depending on days."

@tool
def suggest_exercises(text: str) -> str:
    """Suggest exercises based on equipment."""
    return "Focus on compound lifts with accessory movements."

@tool
def sets_and_reps(text: str) -> str:
    """Recommend sets and reps."""
    return "3–4 sets, 8–12 reps for hypertrophy; 3–5 sets, 3–6 reps for strength."

tools = [
    analyze_goal,
    decide_split,
    suggest_exercises,
    sets_and_reps
]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    max_iterations=3,
    early_stopping_method="generate"
)

def generate_plan(user_prompt: str) -> str:
    """
    Generate a workout plan using a Groq-powered ReAct agent.
    This is called from Streamlit.
    """
    result = agent.invoke(user_prompt)
    return result["output"]
