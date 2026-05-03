from agent import get_news_summary
from email_service import send_email
import asyncio


async def async_handler(event, context):
    summary = await get_news_summary()
    if summary:
        send_email(summary)
    else:
        print("ERROR IN AI RESPONSE")
    return {"statusCode": 200, "body": "Email sent successfully"}


def lambda_handler(event, context):
    return asyncio.run(async_handler(event, context))
