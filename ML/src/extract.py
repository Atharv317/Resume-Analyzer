import re

def extract_projects(text):
    matches = re.findall(r'project', text.lower())
    return len(matches)


def extract_internships(text):
    matches = re.findall(r'intern', text.lower())
    return len(matches)


def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s*(years|yrs)', text.lower())
    if matches:
        return float(matches[0][0])
    return 0


def extract_cgpa(text):
    match = re.search(r'cgpa[^0-9]*([0-9]\.?[0-9]?)', text.lower())
    if match:
        return float(match.group(1))
    return 0


def extract_skills(text):
    skills = [
        "python","java","django","machine learning",
        "ml","sql","pandas","numpy","javascript"
    ]

    found = []
    text_lower = text.lower()

    for skill in skills:
        if skill in text_lower:
            found.append(skill)

    return list(set(found))


def extract_all(text):
    return {
        "projects": extract_projects(text),
        "internships": extract_internships(text),
        "experience_years": extract_experience(text),
        "cgpa": extract_cgpa(text),
        "skills": extract_skills(text)
    }

