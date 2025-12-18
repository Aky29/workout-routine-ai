# ---------------- IMPORTS ----------------
import streamlit as st
from langchain.agents import create_react_agent, AgentExecutor,initialize_agent,AgentType


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
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
    """Analyze the user's fitness goal and extract training focus."""
    return f"User fitness goal: {text}"

@tool
def decide_split(text: str) -> str:
    """Decide an appropriate weekly workout split."""
    return "Choose split based on goal, experience level, and availability."

@tool
def suggest_exercises(text: str) -> str:
    """Suggest exercises based on equipment and workout type."""
    return "Include compound lifts and accessories suitable for the split."

@tool
def sets_and_reps(text: str) -> str:
    """Recommend sets, reps, and rest times."""
    return "Strength: 3–5 sets of 3–6 reps, Hypertrophy: 3–4 sets of 8–12 reps."

tools = [
    analyze_goal,
    decide_split,
    suggest_exercises,
    sets_and_reps,
]

# ---------------- REACT PROMPT ----------------
prompt = PromptTemplate.from_template("""
You are a professional fitness coach AI.

You have access to the following tools:
{tools}

Use this format exactly:

Question: the user's request
Thought: your reasoning
Action: one of [{tool_names}]
Action Input: input to the action
Observation: tool result
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: a clean, structured workout plan

Question: {input}
{agent_scratchpad}
""")

# ---------------- CREATE AGENT ----------------
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    max_iterations=3,        
    early_stopping_method="generate" 
)


# ---------------- AGENT EXECUTOR ----------------
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=6,
    handle_parsing_errors=True
)

# ---------------- PUBLIC FUNCTION ----------------
def generate_plan(user_prompt: str) -> str:
    """
    Generate a workout plan using a Groq-powered AgentExecutor.
    """
    result = agent_executor.invoke({
        "input": user_prompt
    })
    return result["output"]









