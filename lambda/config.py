import os

SES_SENDER = os.getenv("SES_SENDER")
SES_RECEIVER = os.getenv("SES_RECEIVER")
SES_RECEIVERS = [
    email.strip()
    for email in os.getenv("SES_RECEIVERS", SES_RECEIVER or "").split(",")
    if email.strip()
]
