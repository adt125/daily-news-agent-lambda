from agent import generate_email_content
from email_service import send_email


def lambda_handler(event, context):
    try:
        llm_email_response = generate_email_content()
        send_email(llm_email_response)
        return {"statusCode": 200, "body": "Email sent succesfully!"}
    except Exception:
        return {"statusCode": 500, "error": Exception}
