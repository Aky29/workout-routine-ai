from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate

# ---------------- ENV ---------------- #
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY not found")

# ---------------- LLM ---------------- #
llm = ChatGroq(
    api_key=GROQ_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.5
)

# ---------------- TOOLS ---------------- #

@tool
def analyze_goal(text: str) -> str:
    """
    Analyze the user's fitness goal and explain the training focus.
    """
    return llm.invoke(f"Analyze this fitness goal and give training focus:\n{text}").content


@tool
def decide_split(text: str) -> str:
    """
    Decide an appropriate weekly workout split based on the user's request.
    """
    return llm.invoke(f"Create a weekly workout split based on:\n{text}").content


@tool
def suggest_exercises(text: str) -> str:
    """
    Suggest exercises based on available equipment and workout type.
    """
    return llm.invoke(f"Suggest suitable exercises based on:\n{text}").content


@tool
def sets_and_reps(text: str) -> str:
    """
    Recommend sets, reps, and rest times based on goal and experience level.
    """
    return llm.invoke(f"Suggest sets, reps, and rest times for:\n{text}").content


tools = [
    analyze_goal,
    decide_split,
    suggest_exercises,
    sets_and_reps
]

# ---------------- AGENT ---------------- #

prompt = ChatPromptTemplate.from_template("""
You are a professional fitness coach.

The user will describe their workout needs in natural language.
Use the available tools when helpful.

User input:
{input}

Your final answer must be a complete, well-structured workout plan with:
- Clear weekly split
- Exercises per day
- Sets, reps, and rest times
- Short tips
""")

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False
)

# ---------------- PUBLIC FUNCTION ---------------- #

def generate_plan(user_prompt: str) -> str:
    """
    Generate a workout plan from a free-text user prompt.
    """
    result = agent_executor.invoke({"input": user_prompt})
    return result["output"]
