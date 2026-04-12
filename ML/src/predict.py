import os
import joblib
import json
import numpy as np
from src.skills import process_resume

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "../models")

model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

with open(os.path.join(MODEL_DIR, "columns.json")) as f:
    columns = json.load(f)

with open(os.path.join(MODEL_DIR, "threshold.txt")) as f:
    threshold = float(f.read())


def build_features(resume_text, user_data):

    result = process_resume(resume_text)
    skills_vector = result["vector"]

    structured = [
        user_data.get("age", 0),
        user_data.get("education_level", 0),
        user_data.get("cgpa", 0),
        user_data.get("internships", 0),
        user_data.get("projects", 0),
        user_data.get("programming_languages", 0),
        user_data.get("certifications", 0),
        user_data.get("experience_years", 0),
        user_data.get("hackathons", 0),
        user_data.get("research_papers", 0),
        user_data.get("skills_score", 0),
        user_data.get("soft_skills_score", 0),
        user_data.get("resume_length_words", 0),
        user_data.get("university_tier_2", 0),
        user_data.get("university_tier_3", 0),
        user_data.get("company_type_mid", 0),
        user_data.get("company_type_startup", 0),
    ]

    final_features = structured + skills_vector

    return final_features, result["skills"]


def predict_resume(resume_text, user_data):

    features, skills = build_features(resume_text, user_data)

    feature_dict = dict(zip(columns, features))
    ordered_features = [feature_dict[col] for col in columns]

    arr = np.array([ordered_features])
    arr = scaler.transform(arr)

    prob = model.predict_proba(arr)[0][1]

    return {
        "score": float(round(prob * 100, 2)),
        "selected": bool(prob > threshold),
        "skills": skills
    }