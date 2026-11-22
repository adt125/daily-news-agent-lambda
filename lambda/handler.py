from agent import generate_email_content
from email_service import send_email
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    logger.info("Lambda started")

    try:
        llm_email_response = generate_email_content()
        message_id = send_email(llm_email_response)
        logger.info("Lambda completed. SES message id: %s", message_id)
        return {"statusCode": 200, "body": "Email sent successfully!"}
    except Exception as exc:
        logger.exception("Lambda failed: %s", exc)
        return {"statusCode": 500, "error": str(exc)}
