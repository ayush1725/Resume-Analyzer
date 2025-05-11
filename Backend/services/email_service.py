import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL or not EMAIL_PASSWORD:
    raise ValueError("EMAIL or EMAIL_PASSWORD not set in .env file.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_feedback_email(to_email: str, similarity_score: float, feedback: dict, summarized_sections: dict) -> bool:
    try:
        subject = "Resume Analyzer Results"

        # ✅ HTML body
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
            <p>Hi <a href="mailto:{to_email}">{to_email}</a>,</p>
            <p>Thank you for using <strong>Resume Analyzer</strong>! 🎯</p>

            <h3 style="color: #2c3e50;">📊 Resume Analysis Report</h3>
            <p><strong>🔗 Match Score:</strong> {round(similarity_score * 100, 2)}%</p>

            <h4 style="margin-top: 30px;">🧠 Key Insights:</h4>
            <ul>
                <li><strong>general_advice:</strong> {feedback.get("general_advice", "No advice available.")}</li>
            </ul>

            <h4 style="margin-top: 30px;">📄 Summary Breakdown</h4>

            <p><strong>🟡 Experience:</strong><br>{summarized_sections.get("Experience", "Not Available")}</p>
            <p><strong>🎓 Education:</strong><br>{summarized_sections.get("Education", "Not Available")}</p>
            <p><strong>💼 Skills:</strong><br>{summarized_sections.get("Skills", "Not Available")}</p>

            <hr style="margin: 40px 0;">

            <p>This analysis helps you understand how well your resume matches the job description. 
               If your score is low, consider optimizing your resume using the suggestions above.</p>

            <p>Let us know if you'd like help fine-tuning your resume.</p>
            <p style="margin-top: 30px;">Cheers,<br><strong>Resume Analyzer Bot 🤖</strong></p>
        </body>
        </html>
        """

        # Create the email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email

        # Attach HTML body
        msg.attach(MIMEText(html_body, "html"))

        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, EMAIL_PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())

        logger.info(f"[INFO] Email sent successfully to {to_email}")
        return True

    except Exception as e:
        logger.error(f"[ERROR] Failed to send email to {to_email}: {e}")
        return False
