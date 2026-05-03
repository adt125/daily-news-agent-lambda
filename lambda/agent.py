from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
import asyncio
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

APP_NAME = "MarketMindAI"
USER_ID = "AWSLambda"
SESSION_ID = "AWSLambdaSession"

root_agent = Agent(
    name="MarketMindAI",
    model="gemini-2.5-flash",
    description="AI & Indian Market News Curator",
    instruction="""
Write a minimalist email body. No Subject. No filler.

1. Greeting: "Hello AI & Market Enthusiast,"
2. AI Section: Top 5 updates. One sentence per item.
3. Market Section: Top 3 NSE/BSE updates. Focus on market impact.
4. Closing: "Stay informed, MarketMind AI"

**CRITICAL LINK RULE:** 
- Every link MUST be the exact, full URL provided by the search tool. 
- DO NOT truncate, shorten, or guess the URL. 
- If a direct link isn't clear, use the main news source homepage.

Format: Use bold for key names. Total under 150 words.
""",
    # google_search is a pre-built tool which allows the agent to perform Google searches.
    tools=[google_search],
)


# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )
    return session, runner


# Agent Interaction
async def get_news_summary():
    query = "Generate the daily briefing email."
    content = types.Content(role="user", parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    )

    final_response = None

    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

    return final_response


if __name__ == "__main__":
    asyncio.run(get_news_summary())
