import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_skills(path="skills.csv"):
    return pd.read_csv(path)["skill"].str.lower().tolist()


def find_skills(text, skills):
    found = []
    for s in skills:
        pattern = r"(?<![a-z0-9+#])" + re.escape(s) + r"(?![a-z0-9+#])"
        if re.search(pattern, text):
            found.append(s)
    return found


def similarity_score(resume_text, jd_text):
    vec = TfidfVectorizer(stop_words="english")
    matrix = vec.fit_transform([resume_text, jd_text])
    score = cosine_similarity(matrix[0], matrix[1])[0][0]
    return round(float(score) * 100, 2)


def analyze(resume_text, jd_text, skills):
    resume_skills = find_skills(resume_text, skills)
    jd_skills = find_skills(jd_text, skills)
    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched": sorted(set(resume_skills) & set(jd_skills)),
        "missing": sorted(set(jd_skills) - set(resume_skills)),
        "similarity": similarity_score(resume_text, jd_text),
    }