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
    """Suggest sets and reps based on goal and experience level."""
    goal, level = goal_and_level.split("|")
    return llm.invoke(
        f"Suggest sets and reps for {goal.strip()}, level {level.strip()}"
    ).content


tools = [goal_analysis, workout_split, exercise_selector, sets_reps]

# ---------- AGENT (AUTO-COMPATIBLE) ----------
def _build_agent():
    try:
        # 🔹 NEW LangChain (>=0.2)
        from langchain.agents import AgentExecutor, create_react_agent
        from langchain.prompts import ChatPromptTemplate

        prompt = ChatPromptTemplate.from_template("""
        You are a professional fitness coach.

        Use the tools to create a complete workout plan.

        User request:
        {input}
        """)

        agent = create_react_agent(
            llm=llm,
            tools=tools,
            prompt=prompt
        )

        return AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=False
        )

    except ImportError:
        # 🔹 OLD LangChain (<0.2)
        from langchain.agents import initialize_agent, AgentType

        return initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )


agent = _build_agent()

# ---------- ENTRY FUNCTION ----------
def generate_plan(user_prompt: str):
    prompt = f"""
    The user described their workout needs as follows:

    {user_prompt}

    Extract:
    - Fitness goal
    - Days per week
    - Equipment
    - Experience level

    Then create a complete workout plan including:
    - Weekly split
    - Exercises
    - Sets and reps
    - Rest times
    """

    try:
        result = agent.invoke({"input": prompt})
        return result["output"]
    except AttributeError:
        return agent.run(prompt)
