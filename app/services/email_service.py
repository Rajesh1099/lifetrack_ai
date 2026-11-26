
import smtplib  # Import Python's SMTP email library
from email.message import EmailMessage  # Import the email message builder
from email.utils import formataddr  # Import sender name formatting

from app.core.config import settings  # Import SMTP configuration


def send_email(to_email: str, subject: str, body: str, html_body: str) -> None:  # Send a plain-text and HTML email
    message = EmailMessage()  # Create a new email message

    message["Subject"] = subject  # Set the email subject
    message["From"] = formataddr((settings.SMTP_FROM_NAME, settings.SMTP_FROM_EMAIL))  # Set sender name and address
    message["To"] = to_email  # Set recipient email address

    message.set_content(body)  # Add plain-text fallback for email clients that do not support HTML
    message.add_alternative(html_body, subtype="html")  # Add the professionally styled HTML version

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:  # Connect to Gmail SMTP
        server.ehlo()  # Identify this application to Gmail
        server.starttls()  # Enable encrypted communication
        server.ehlo()  # Identify again after encryption is enabled
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)  # Authenticate with Gmail
        server.send_message(message)  # Send the email
