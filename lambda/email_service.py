import boto3
import logging
from botocore.exceptions import ClientError
from config import SES_SENDER, SES_RECEIVER
from html_formatter import generate_html_email

logger = logging.getLogger(__name__)
ses = boto3.client("ses", region_name="ap-south-1")


def send_email(content):
    html_email_content = generate_html_email(content)
    logger.info("Sending email through SES")

    try:
        response = ses.send_email(
            Source=SES_SENDER,
            Destination={"ToAddresses": [SES_RECEIVER]},
            Message={
                "Subject": {"Data": "Daily News Digest"},
                "Body": {"Html": {"Data": html_email_content}},
            },
        )
    except ClientError as exc:
        error = exc.response.get("Error", {})
        metadata = exc.response.get("ResponseMetadata", {})
        logger.exception(
            "SES failed. Code=%s Message=%s RequestId=%s Status=%s",
            error.get("Code"),
            error.get("Message"),
            metadata.get("RequestId"),
            metadata.get("HTTPStatusCode"),
        )
        raise

    message_id = response.get("MessageId")
    logger.info("SES email sent. MessageId=%s", message_id)
    return message_id
