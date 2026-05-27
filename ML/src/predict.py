import os
import joblib
import json
import numpy as np
import pandas as pd

from ML.src.skills import process_resume

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "../models")

model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

with open(os.path.join(MODEL_DIR, "columns.json")) as f:
    columns = json.load(f)

with open(os.path.join(MODEL_DIR, "threshold.txt")) as f:
    threshold = float(f.read())


LANGUAGES = {
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
    "go",
    "rust",
    "c#",
    "php"
}


def safe_clip(value, low=0, high=100):
    return max(low, min(value, high))


def build_features(resume_text, user_data, extracted):

    skills = process_resume(resume_text)["skills"]

    age = safe_clip(user_data.get("age", 0), 0, 100)

    education_level = safe_clip(
        user_data.get("education_level", 0),
        0,
        5
    )

    cgpa = safe_clip(user_data.get("cgpa", 0), 0, 10)

    internships = safe_clip(
        user_data.get("internships", 0),
        0,
        15
    )

    projects = safe_clip(
        user_data.get("projects", 0),
        0,
        20
    )

    certifications = safe_clip(
        user_data.get("certifications", 0),
        0,
        20
    )

    experience_years = safe_clip(
        user_data.get("experience_years", 0),
        0,
        40
    )

    soft_skills_score = safe_clip(
        user_data.get("soft_skills_score", 0),
        0,
        20
    )

    resume_length_words = len(resume_text.split())

    university_tier_2 = user_data.get("university_tier_2", 0)
    university_tier_3 = user_data.get("university_tier_3", 0)

    company_type_mid = user_data.get("company_type_mid", 0)
    company_type_startup = user_data.get("company_type_startup", 0)

    programming_languages = len([
        s for s in skills
        if s.lower() in LANGUAGES
    ])

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

    feature_dict = {
        "age": age,
        "education_level": education_level,
        "cgpa": cgpa,
        "internships": internships,
        "projects": projects,
        "programming_languages": programming_languages,
        "certifications": certifications,
        "experience_years": experience_years,
        "skills_score": skills_score,
        "soft_skills_score": soft_skills_score,
        "resume_length_words": resume_length_words,
        "university_tier_Tier 2": university_tier_2,
        "university_tier_Tier 3": university_tier_3,
        "company_type_Mid-size": company_type_mid,
        "company_type_Startup": company_type_startup,
        "cgpa_high": cgpa_high,
        "cgpa_low": cgpa_low,
        "exp_high": exp_high,
        "exp_fresher": exp_fresher,
        "skill_density": skill_density,
        "cgpa_x_skills": cgpa_x_skills,
        "exp_x_projects": exp_x_projects,
        "exp_x_internships": exp_x_internships,
        "skills_x_soft": skills_x_soft
    }

    ordered_features = [
        feature_dict[col]
        for col in columns
    ]

    return ordered_features, skills


def predict_resume(resume_text, user_data, extracted):

    features, skills = build_features(
        resume_text,
        user_data,
        extracted
    )

    arr = pd.DataFrame(
        [features],
        columns=columns
    )

    arr = scaler.transform(arr)

    prob = model.predict_proba(arr)[0][1]

    selected = prob >= threshold

    if prob >= threshold:
        confidence = "High"

    elif prob >= threshold - 0.1:
        confidence = "Medium"

    else:
        confidence = "Low"

    return {
        "score": float(round(prob * 100, 2)),
        "selected": selected,
        "skills": skills,
        "confidence_level": confidence,
        "probability": float(round(prob, 4))
    }