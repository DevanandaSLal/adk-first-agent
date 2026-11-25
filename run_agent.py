"""Method 3: Running an ADK agent programmatically with Python."""
import asyncio
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Load GOOGLE_API_KEY from the agent's .env file (keeps the key out of code)
load_dotenv("my_first_agent/.env")

agent = Agent(
    model="gemini-3.5-flash",
    name="math_tutor",
    instruction="""You are a patient math tutor.
    Guide students through problems step-by-step.
    Don't just give answers - help them discover solutions.""",
)

APP_NAME = "math_tutor_app"
USER_ID = "student_1"
SESSION_ID = "session_001"

session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)


async def run_agent():
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(f"Session created: {SESSION_ID}\n")

    question = "How do I solve 2x + 5 = 13?"
    user_message = Content(role="user", parts=[Part(text=question)])
    print(f"User: {question}\n")
    print("Agent: ", end="")

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=user_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(run_agent())
