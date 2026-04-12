import re

SKILLS = [
    "python", "java", "c++", "ruby", "javascript",
    "django", "flask", "react", "node", "express",
    "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch", "sklearn",
    "sql", "mongodb", "mysql",
    "data analysis", "pandas", "numpy","c#",
]

SYNONYMS = {
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "machine learning",
    "np": "numpy",
    "pd": "pandas"
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s+]', ' ', text)
    return text


def normalize_text(text):
    words = text.split()
    normalized_words = []

    for word in words:
        if word in SYNONYMS:
            normalized_words.append(SYNONYMS[word])
        else:
            normalized_words.append(word)

    return " ".join(normalized_words)


def extract_skills(text):
    text = clean_text(text)
    text = normalize_text(text)

    found_skills = []

    for skill in SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))


def skills_to_vector(found_skills):
    return [1 if skill in found_skills else 0 for skill in SKILLS]


def process_resume(text):
    skills = extract_skills(text)
    vector = skills_to_vector(skills)

    return {
        "skills": skills,
        "vector": vector
    }