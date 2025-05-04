# AI Resume Analyzer

An AI-powered web application that analyzes resumes and matches them with job descriptions. The tool uses natural language processing (NLP) to summarize resumes, extract key skills, and provide a compatibility score against job descriptions.

## Features

- **Resume Summarization**: Automatically summarizes resumes using the HuggingFace transformer model.
- **Job Description Matching**: Compares resumes to job descriptions to calculate a compatibility score.
- **User Dashboard**: Allows users to upload resumes, view feedback, and see historical analysis results.
- **Email Notifications**: Notifies users when their resume score falls below a certain threshold.
- **Saved Results**: Lets users save their analysis results and access them later.

## Tech Stack

### Backend:
- **FastAPI**: For building the backend API to handle requests and responses.
- **HuggingFace Transformers**: Used for summarizing resumes (model: `facebook/bart-large-cnn`).
- **Mistral**: Locally hosted for additional summarization and processing.
- **Python**: Backend logic and integration of various services.
- **PyMuPDF**: To extract text from resumes uploaded in PDF format.
- **Sentence Transformers**: For generating semantic embeddings and matching resumes with job descriptions.

### Frontend:
- **React (Vite)**: For building the frontend user interface.
- **Vanilla CSS**: For styling the frontend, including animations and transitions.
- **Bootstrap & Tailwind CSS**: Used for designing and ensuring responsiveness.

### Database:
- **MongoDB**: For storing user data, resumes, feedback scores, and analysis results.

### Additional Tools:
- **GitHub Actions**: For CI/CD pipeline setup to automate deployment and testing.
- **Jenkins**: Integrated for continuous integration workflows.
- **Socket.IO**: For real-time communication between the frontend and backend.

## Working Process

1. **Resume Parsing & Summarization**:
   - When a user uploads a resume, the text is extracted using PyMuPDF.
   - The extracted text is then passed to the HuggingFace transformer model (`facebook/bart-large-cnn`) for summarization.
   - The summarized resume is further processed by Mistral (if used) for additional context and improvements.

2. **Embedding Generation**:
   - Semantic embeddings are generated using `Sentence Transformers`, which enable the comparison between the resume and the job description.

3. **Matching & Scoring Algorithm**:
   - The embeddings of the resume and the job description are compared using cosine similarity.
   - A matching score (0–100%) is calculated to determine how closely the resume matches the job description.

4. **Result Insights & Notifications**:
   - The results are displayed in a user-friendly dashboard, showing a detailed summary, match percentage, and areas for improvement.
   - If the matching score is below a certain threshold, email notifications are sent to users to encourage them to update their resumes.

## Installation

### Prerequisites

- Python 3.x
- Docker
- MongoDB / MySQL (depending on your setup)

### Steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/ai-resume-analyzer.git
   cd ai-resume-analyzer ```
2. **Set up the backend environment**:
   ```bash
   cd Backend
   pip install -r requirements.txt  ```
3. **Start the backend server**:
   ```bash
   uvicorn main:app --reload ```
4. **Set up the frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev ```
5. **Start MongoDB (if using locally) or connect to your cloud instance.**
6. **Deploy the application using Docker(Optional):**
   ```bash
   docker-compose up --build
   ```
### Contributing:
---
Feel free to fork the repository, open issues, or submit pull requests. If you have suggestions for improvements or new features, don’t hesitate to contribute!
### License:
---
This project is licensed under the MIT License - see the LICENSE file for details.
