from google import genai
from google.genai.types import HttpOptions
from dotenv import load_dotenv, find_dotenv
from news_service import get_news
from html_formatter import generate_html_email
import os
import json

load_dotenv(find_dotenv())


def generate_email_content():
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"), http_options=HttpOptions(api_version="v1")
    )

    ai_news, market_news = get_news()

    prompt = f"""
Return ONLY valid JSON. No explanation.

Format:
{{
  "ai": [
    {{
      "title": "",
      "summary": "",
      "link": ""
    }}
  ],
  "market": [
    {{
      "title": "",
      "summary": "",
      "link": ""
    }}
  ]
}}

Rules:
- 5 AI items, 3 market items
- Summary must be 2-3 lines
- Use EXACT links from input
- Do NOT modify links
- No markdown, no extra text

INPUT:

AI News:
{ai_news}

Market News:
{market_news}
"""

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    # Parse JSON safely
    try:
        data = json.loads(response.text)
    except Exception:
        print("Invalid JSON from model:\n", response.text)
        raise

    return data


if __name__ == "__main__":
    structured_data = generate_email_content()
    html_email = generate_html_email(structured_data)

    print(html_email)  # or pass to SES
