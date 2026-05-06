from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from dotenv import load_dotenv, find_dotenv
from news_service import get_news
from models import EmailDigest
import logging
import os
import json

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)


def generate_email_content():
    logger.info("Generating email content")

    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options=HttpOptions(api_version="v1beta"),
    )

    ai_news, market_news = get_news()

    prompt = f"""
Create a daily news email digest from the input.

Rules:
- 5 AI items, 5 market items
- Summary must be 2-3 lines
- Use EXACT links from input
- Do NOT modify links

INPUT:

AI News:
{ai_news}

Market News:
{market_news}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=EmailDigest,
                temperature=0.2,
            ),
        )
    except Exception:
        logger.exception("Gemini request failed")
        raise

    logger.info("Gemini response received")

    try:
        if response.parsed:
            data = response.parsed.model_dump()
        else:
            data = EmailDigest.model_validate(json.loads(response.text)).model_dump()
    except Exception:
        logger.exception("Gemini returned invalid JSON: %s", response.text)
        raise

    logger.info(
        "Gemini JSON parsed. AI items=%s Market items=%s",
        len(data.get("ai", [])),
        len(data.get("market", [])),
    )
    return data


if __name__ == "__main__":
    structured_data = generate_email_content()
    print(json.dumps(structured_data, indent=2))
