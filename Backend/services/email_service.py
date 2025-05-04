import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import json
import logging

# Load environment variables
load_dotenv()

# Ensure environment variables are set
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL or not EMAIL_PASSWORD:
    raise ValueError("EMAIL or EMAIL_PASSWORD not set in .env file.")

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_feedback_email(to_email: str, similarity_score: float, feedback: dict, summarized_sections: dict) -> bool:
    try:
        subject = "Resume Analyzer Results"

        # Format the body of the email
        body = f"""
        Hi {to_email},\n
        Here is your resume analysis report:\n\n
        🔎 Similarity Score: {round(similarity_score, 2)}\n\n
        📝 Feedback:\n{json.dumps(feedback, indent=4)}\n\n
        📚 Summarized Sections:\n-------------------------\n
        Experience:\n{summarized_sections.get("Experience", "Not Available")}\n\n
        Education:\n{summarized_sections.get("Education", "Not Available")}\n\n
        Skills:\n{summarized_sections.get("Skills", "Not Available")}\n\n
        This analysis helps you understand how well your resume matches the job description.\n\n
        Thank you for using Resume Analyzer!\n\n
        Regards,\nResume Analyzer Bot
        """

        # Create email message
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email

        # Attach body to email
        msg.attach(MIMEText(body, "plain"))

        # Send email via SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, EMAIL_PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())

        logger.info(f"[INFO] Email sent successfully to {to_email}")
        return True

    except Exception as e:
        logger.error(f"[ERROR] Failed to send email to {to_email}: {e}")
        return False
