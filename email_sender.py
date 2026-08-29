"""SMTP üzerinden HTML e-posta gönderir."""

import os
import smtplib
from email.message import EmailMessage


def send_email(subject: str, html_body: str) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = os.environ["EMAIL_FROM"]
    message["To"] = os.environ["EMAIL_TO"]
    message.set_content("Bu e-posta HTML destekleyen bir istemciyle açılmalıdır.")
    message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", "587"))) as smtp:
        smtp.starttls()
        smtp.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(message)

