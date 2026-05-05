import boto3
from config import SES_SENDER, SES_RECEIVER
from html_formatter import generate_html_email

ses = boto3.client("ses", region_name="ap-south-1")


def send_email(content):

    html_email_content = generate_html_email(content)

    ses.send_email(
        Source=SES_SENDER,
        Destination={"ToAddresses": [SES_RECEIVER]},
        Message={
            "Subject": {"Data": "Daily News Digest"},
            "Body": {"Html": {"Data": html_email_content}},
        },
    )
