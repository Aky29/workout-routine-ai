from dotenv import load_dotenv
import os

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY not found")

from langchain_groq import ChatGroq
from langchain.tools import tool

# ---------- LLM ----------
llm = ChatGroq(
    api_key=GROQ_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.5
)

# ---------- TOOLS ----------
@tool
def goal_analysis(text: str) -> str:
    return llm.invoke(f"Analyze fitness goal: {text}").content


@tool
def workout_split(text: str) -> str:
    return llm.invoke(f"Create workout split: {text}").content


@tool
def exercise_selector(text: str) -> str:
    return llm.invoke(f"Suggest exercises: {text}").content


@tool
def sets_reps(text: str) -> str:
    return llm.invoke(f"Suggest sets and reps: {text}").content


tools = [goal_analysis, workout_split, exercise_selector, sets_reps]


# ---------- AGENT BUILDER ----------
def _get_agent():
    try:
        # NEW LangChain
        from langchain.agents import AgentExecutor, create_react_agent
        from langchain.prompts import ChatPromptTemplate

        prompt = ChatPromptTemplate.from_template("""
        You are a professional fitness coach.

        User input:
        {input}

        Extract:
        - Goal
        - Days
        - Equipment
        - Experience level

        Then generate a complete workout plan.
        """)

        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

        return AgentExecutor(agent=agent, tools=tools, verbose=False)

    except Exception:
        # OLD LangChain
        from langchain.agents import initialize_agent, AgentType

        return initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )


# ---------- PUBLIC FUNCTION ----------
def generate_plan(user_prompt: str) -> str:
    """
    Accepts free-text user prompt and returns workout plan
    """
    agent = _get_agent()

    final_prompt = f"""
    User workout description:
    {user_prompt}

    Create a detailed workout plan with:
    - Weekly split
    - Exercises
    - Sets & reps
    - Rest times
    """

    try:
        result = agent.invoke({"input": final_prompt})
        return result["output"]
    except AttributeError:
        return agent.run(final_prompt)
