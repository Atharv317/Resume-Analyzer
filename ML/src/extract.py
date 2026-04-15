import re
from datetime import datetime
from src.section_parser import split_sections


def extract_projects(text):
    sections = split_sections(text)
    proj_text = sections.get("projects", "")

    if not proj_text:
        return 0

    lines = [l.strip() for l in proj_text.split("\n") if l.strip()]

    count = 0
    for line in lines:
        if len(line.split()) > 3 and ("—" in line or " - " in line):
            count += 1

    return min(count, 6)


def extract_internships(text):
    sections = split_sections(text)
    exp_text = sections.get("experience", "").lower()

    matches = re.findall(r'\b(internship|intern|trainee|summer intern)\b', exp_text)

    return len(set(matches))


def extract_experience(text):
    sections = split_sections(text)
    exp_text = sections.get("experience", "").lower()

    date_ranges = re.findall(
        r'([A-Za-z]{3,9}\s*\d{4})\s*[-–]\s*([A-Za-z]{3,9}\s*\d{4}|present)',
        exp_text
    )

    total_years = 0.0

    for start, end in date_ranges:
        try:
            start_dt = datetime.strptime(start, "%b %Y")
        except:
            try:
                start_dt = datetime.strptime(start, "%B %Y")
            except:
                continue

        if "present" in end:
            end_dt = datetime.now()
        else:
            try:
                end_dt = datetime.strptime(end, "%b %Y")
            except:
                try:
                    end_dt = datetime.strptime(end, "%B %Y")
                except:
                    continue

        total_years += (end_dt - start_dt).days / 365

    return round(total_years, 2)


def extract_cgpa(text):
    text = text.lower()
    match = re.search(r'(cgpa|gpa)[^0-9]*([0-9]\.?[0-9]{0,2})', text)
    if match:
        value = float(match.group(2))
        if value <= 4:
            return round((value / 4) * 10, 2)
        return value
    return 0


def extract_education_level(text):
    text = text.lower()

    if "phd" in text:
        return 4
    elif "master" in text or "m.tech" in text or "msc" in text:
        return 3
    elif "b.tech" in text or "bachelor" in text or "b.e" in text:
        return 2
    elif "diploma" in text:
        return 1

    return 0


def extract_certifications(text):
    keywords = [
        "certified", "certificate", "aws", "google cloud",
        "coursera", "udemy", "azure"
    ]

    text = text.lower()
    count = 0

    for k in keywords:
        if k in text:
            count += 1

    return min(count, 5)


def extract_soft_skills(text):
    skills = [
        "communication", "teamwork", "leadership",
        "problem solving", "adaptability", "collaboration"
    ]

    text = text.lower()
    score = 0

    for s in skills:
        if s in text:
            score += 1

    return score


def extract_all(text):
    return {
        "projects": extract_projects(text),
        "internships": extract_internships(text),
        "experience_years": extract_experience(text),
        "cgpa": extract_cgpa(text),
        "education_level": extract_education_level(text),
        "certifications": extract_certifications(text),
        "soft_skills_score": extract_soft_skills(text)
    }