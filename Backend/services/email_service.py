
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL or not EMAIL_PASSWORD:
    raise ValueError("EMAIL or EMAIL_PASSWORD not set in .env file.")

def send_feedback_email(to_email: str, subject: str, message: str) -> bool:
    try:
        # Create email message
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email

        # Add plain text content
        msg.attach(MIMEText(message, "plain"))

        # Send via SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, EMAIL_PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())

        print(f"[INFO] Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send email to {to_email}: {e}")
        return False
