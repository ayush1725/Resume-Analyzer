from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from resume_parser import extract_text_from_pdf
from matcher import calculate_similarity
from transformers import pipeline
import shutil
import os
import re
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from models.user_model import create_user, get_user_by_email, verify_password
from fastapi.security import OAuth2PasswordBearer
import smtplib  # For email functionality
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Path for file uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY")  # Store in .env for security
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Email configuration
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Pydantic model for user login
class User(BaseModel):
    email: str
    password: str

# Pydantic model for the JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Function to get current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email  # This can be used to fetch the user from DB
    except jwt.JWTError:
        raise credentials_exception

# Function to summarize text using the BART model
def summarize_with_model(text: str) -> str:
    max_input_length = 1024
    chunks = [text[i:i + max_input_length] for i in range(0, len(text), max_input_length)]
    
    chunk_summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        chunk_summaries.append(summary[0]['summary_text'])

    final_summary = " ".join(chunk_summaries)
    final_summary = summarizer(final_summary, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    
    return final_summary

# Function to generate feedback based on resume-job similarity
def generate_feedback(similarity_score, resume_text, job_description):
    feedback = {}
    if similarity_score < 0.4:
        feedback['general_advice'] = "Your resume's similarity score to the job description is low. Consider including more relevant keywords to increase the match."
        
        # Extract keywords from job description
        job_keywords = set(re.findall(r'\b[A-Za-z0-9\+\#]+(?:\s[A-Za-z0-9\+]+)?\b', job_description.lower()))
        
        # Extract keywords from resume
        resume_keywords = set(re.findall(r'\b[A-Za-z0-9\+\#]+(?:\s[A-Za-z0-9\+]+)?\b', resume_text.lower()))
        
        missing_keywords = job_keywords - resume_keywords
        if missing_keywords:
            feedback['missing_keywords'] = f"Consider adding these keywords to your resume: {', '.join(missing_keywords)}."
        
        if "experience" in resume_text.lower():
            feedback['experience_advice'] = "Ensure your experience section highlights the job titles, tools, and technologies mentioned in the job description."
        if "skills" in resume_text.lower():
            feedback['skills_advice'] = "Review the job description for specific skills and make sure they are reflected in your resume."
        
    return feedback

# Route to sign up a new user
@app.post("/signup/")  # Signup route
async def signup(user: User):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    create_user(user.email, user.password)
    return {"message": "User created successfully"}

# Route to log in a user
@app.post("/login/", response_model=Token)  # Login route
async def login(user: User):
    stored_user = get_user_by_email(user.email)
    if not stored_user or not verify_password(stored_user['password'], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route to analyze resume
@app.post("/analyze/")  # Resume analysis route
async def analyze_resume(resume: UploadFile = File(...), job_description: str = Form(...), current_user: str = Depends(get_current_user)):
    try:
        # Save uploaded resume file
        file_path = os.path.join(UPLOAD_DIR, resume.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        resume_text = extract_text_from_pdf(file_path)

        # Define section headers (with variations)
        section_keywords = {
            "Experience": ["experience", "work", "internship", "projects"],
            "Education": ["education", "qualification"],
            "Skills": ["skills", "technical skills", "technologies"],
            "Summary": ["summary", "about", "profile", "overview"]
        }

        section_texts = {key: "" for key in section_keywords}

        current_section = None

        for line in resume_text.splitlines():
            line_lower = line.lower().strip()
            matched = False
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    current_section = section
                    matched = True
                    break
            if current_section:  # Skip adding lines to Misc if section is found
                section_texts[current_section] += line.strip() + '\n'

        # Summarize relevant sections
        summarized_sections = {}
        for section, text in section_texts.items():
            if section == "Skills":
                summarized_sections[section] = text.strip()
            elif section != "Summary":  # Skip the "Summary" section
                summarized_sections[section] = summarize_with_model(text.strip()) if text.strip() else ""

        # Combine Experience and Projects section for similarity calculation
        experience_text = section_texts.get("Experience", "")
        similarity_score = calculate_similarity(experience_text, job_description)

        feedback = generate_feedback(similarity_score, resume_text, job_description)

    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

    return {
        "summary": summarized_sections,
        "similarity_score": round(similarity_score, 2),
        "feedback": feedback
    }
