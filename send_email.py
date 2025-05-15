import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration – Replace with your actual credentials
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def send_email(recipient_email: str, body: str, subject: str = "No Subject"):
    """
    Sends an email to the given recipient with the provided body text and optional subject.

    Parameters:
        recipient_email (str): The recipient's email address.
        body (str): The plain text content of the email.
        subject (str): The subject of the email (default is 'No Subject').
    """
    try:
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
            print(f"Email successfully sent to {recipient_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")
