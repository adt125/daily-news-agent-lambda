from agent import generate_email_content
from email_service import send_email
import traceback


def lambda_handler(event, context):
    try:
        llm_email_response = generate_email_content()
        send_email(llm_email_response)
        return {"statusCode": 200, "body": "Email sent successfully!"}
    except Exception as exc:
        traceback.print_exc()
        return {"statusCode": 500, "error": str(exc)}
