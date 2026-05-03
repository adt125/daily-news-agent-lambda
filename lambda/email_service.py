import boto3
from config import SES_SENDER, SES_RECEIVER


def send_email(content):
    ses = boto3.client("ses", region_name="ap-south-1")

    ses.send_email(
        Source=SES_SENDER,
        Destination={"ToAddresses": [SES_RECEIVER]},
        Message={
            "Subject": {"Data": "Daily News Digest"},
            "Body": {"Html": {"Data": content}},
        },
    )
