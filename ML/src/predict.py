import os
import joblib
import json
import numpy as np
from src.skills import process_resume
from src.validation import validate_resume

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
    skills = result["skills"]

    age = user_data.get("age", 0)
    education_level = user_data.get("education_level", 0)
    cgpa = user_data.get("cgpa", 0)
    internships = user_data.get("internships", 0)
    projects = user_data.get("projects", 0)
    programming_languages = user_data.get("programming_languages", 0)
    certifications = user_data.get("certifications", 0)
    experience_years = user_data.get("experience_years", 0)
    soft_skills_score = user_data.get("soft_skills_score", 0)

    resume_length_words = len(resume_text.split())

    university_tier_2 = user_data.get("university_tier_2", 0)
    university_tier_3 = user_data.get("university_tier_3", 0)
    company_type_mid = user_data.get("company_type_mid", 0)
    company_type_startup = user_data.get("company_type_startup", 0)

    skills_score = len(skills)

    cgpa_high = int(cgpa >= 8)
    cgpa_low = int(cgpa < 6.5)

    exp_high = int(experience_years > 2)
    exp_fresher = int(experience_years < 1)

    skill_density = skills_score / (resume_length_words + 1)

    cgpa_x_skills = cgpa * skills_score
    exp_x_projects = experience_years * projects
    exp_x_internships = experience_years * internships
    skills_x_soft = skills_score * soft_skills_score

    structured = [
        age,
        education_level,
        cgpa,
        internships,
        projects,
        programming_languages,
        certifications,
        experience_years,
        skills_score,
        soft_skills_score,
        resume_length_words,
        university_tier_2,
        university_tier_3,
        company_type_mid,
        company_type_startup,
        cgpa_high,
        cgpa_low,
        exp_high,
        exp_fresher,
        skill_density,
        cgpa_x_skills,
        exp_x_projects,
        exp_x_internships,
        skills_x_soft
    ]

    return structured, skills


def predict_resume(resume_text, user_data):
    validation = validate_resume(resume_text)

    if not validation["is_resume"]:
        return {
            "error": "Invalid resume format",
            "validation": validation
        }

    features, skills = build_features(resume_text, user_data)

    if len(features) != len(columns):
        raise ValueError(f"Feature mismatch: expected {len(columns)}, got {len(features)}")

    feature_dict = dict(zip(columns, features))
    ordered_features = [feature_dict[col] for col in columns]

    arr = np.array([ordered_features])
    arr = scaler.transform(arr)

    prob = model.predict_proba(arr)[0][1]

    return {
        "score": float(round(prob * 100, 2)),
        "selected": bool(prob > threshold),
        "skills": skills,
        "validation": validation
    }