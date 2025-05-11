from sentence_transformers import SentenceTransformer, util

# Load the trained SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(resume_text, job_text):
    # Generate embeddings for both resume and job description
    embeddings = model.encode([resume_text, job_text])
    
    # Calculate cosine similarity
    score = util.cos_sim(embeddings[0], embeddings[1])
    
    # Return the similarity score as a float
    return float(score)
