import re
from datetime import datetime
from src.section_parser import split_sections


def extract_projects(text):

    sections = split_sections(text)
    proj_text = sections.get("projects", "")

    if not proj_text:
        return 0

    lines = [
        l.strip()
        for l in proj_text.split("\n")
        if l.strip()
    ]

    count = 0

    tech_words = [
        "python", "java", "django", "react",
        "pandas", "numpy", "tensorflow",
        "scikit", "html", "css", "javascript",
        "flask", "sql", "mongodb",
        "rest framework", "api"
    ]

    for i in range(len(lines) - 1):

        line = lines[i]

        if line.startswith("•"):
            continue

        words = line.split()

        if len(words) < 1 or len(words) > 12:
            continue

        next_line = lines[i + 1].lower()

        tech_count = sum(
            1 for t in tech_words
            if t in next_line
        )

        title_case_ratio = sum(
            1 for w in words
            if w[:1].isupper()
        ) / len(words)

        has_separator = any(
            c in line
            for c in ["|", "—", "-", "–", ":"]
        )

        if tech_count >= 2 and (
            has_separator or title_case_ratio > 0.5
        ):
            count += 1

    return min(count, 10)


def extract_internships(text):

    sections = split_sections(text)

    exp_text = (
        sections.get("experience", "") +
        sections.get("work experience", "")
    )

    if not exp_text:
        return 0

    lines = [
        l.strip()
        for l in exp_text.split("\n")
        if l.strip()
    ]

    count = 0

    role_words = [
        "intern",
        "internship",
        "trainee",
        "summer intern"
    ]

    company_words = [
        "python",
        "django",
        "react",
        "java",
        "developer",
        "engineer",
        "backend",
        "frontend",
        "software",
        "ml",
        "ai"
    ]

    for i in range(len(lines) - 1):

        line = lines[i]

        if line.startswith("•"):
            continue

        words = line.split()

        if len(words) < 2 or len(words) > 12:
            continue

        lower = line.lower()

        has_role = any(
            r in lower for r in role_words
        )

        next_line = lines[i + 1].lower()

        context_score = sum(
            1 for w in company_words
            if w in next_line
        )

        title_case_ratio = sum(
            1 for w in words
            if w[:1].isupper()
        ) / len(words)

        if (
            has_role and
            (
                context_score >= 1 or
                title_case_ratio > 0.5
            )
        ):
            count += 1

    return min(count, 5)


def extract_experience(text):

    sections = split_sections(text)

    exp_text = (
        sections.get("experience", "") +
        sections.get("work experience", "")
    ).lower()

    exp_text = re.sub(
        r'([A-Za-z]{3,9})(\d{4})',
        r'\1 \2',
        exp_text
    )

    date_ranges = re.findall(
    r'([A-Za-z]{3,9}\s*\d{4})\s*[-–]\s*(present|current|now|[A-Za-z]{3,9}\s*\d{4})',
    exp_text,
    re.IGNORECASE
    )

    total_years = 0.0

    for start, end in date_ranges:

        start_dt = None
        end_dt = None

        for fmt in ["%b %Y", "%B %Y"]:

            try:
                start_dt = datetime.strptime(start, fmt)
                break

            except:
                pass

        if not start_dt:
            continue

        if end.lower() in ["present", "current", "now"]:
            end_dt = datetime.now()

        else:

            for fmt in ["%b %Y", "%B %Y"]:

                try:
                    end_dt = datetime.strptime(end, fmt)
                    break

                except:
                    pass

        if not end_dt:
            continue

        total_years += (
            (end_dt - start_dt).days / 365
        )

    return round(total_years, 2)


def extract_cgpa(text):

    text = text.lower()

    match = re.search(
        r'(cgpa|gpa)[^0-9]*([0-9]\.?[0-9]{0,2})',
        text
    )

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

    elif (
        "master" in text or
        "m.tech" in text or
        "msc" in text or
        "mca" in text
    ):
        return 3

    elif (
        "b.tech" in text or
        "bachelor" in text or
        "b.e" in text or
        "bca" in text or
        "b.sc" in text or
        "bs" in text
    ):
        return 2

    elif "diploma" in text:
        return 1

    return 0


def extract_certifications(text):

    keywords = [
        "certified",
        "certificate",
        "aws",
        "google cloud",
        "coursera",
        "udemy",
        "azure",
        "oracle",
        "ibm"
    ]

    text = text.lower()

    count = 0

    for k in keywords:

        if k in text:
            count += 1

    return min(count, 5)


def extract_soft_skills(text):

    skills = [
        "communication",
        "teamwork",
        "leadership",
        "problem solving",
        "adaptability",
        "collaboration",
        "critical thinking",
        "time management"
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