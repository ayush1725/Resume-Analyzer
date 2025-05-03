def save_resume_analysis(jobs_collection, user_email, resume_text, summary, score, feedback):
    return jobs_collection.insert_one({
        "user_email": user_email,
        "resume_text": resume_text,
        "summary": summary,
        "score": score,
        "feedback": feedback
    })
