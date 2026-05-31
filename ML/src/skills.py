import re

SKILLS = [

    # Languages
    "python", "java", "c++", "c#", "javascript",
    "typescript", "sql",

    # Backend
    "django", "flask", "fastapi",
    "node", "express",
    "spring", "spring boot",

    # Frontend
    "react", "nextjs",
    "html", "css",

    # Databases
    "mysql", "postgresql",
    "mongodb", "sqlite",

    # ML / AI
    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",
    "feature engineering",
    "data analysis",

    # Libraries
    "numpy",
    "pandas",
    "scikit-learn",
    "tensorflow",
    "pytorch",

    # DevOps / Tools
    "docker",
    "git",
    "github",
    "linux",
    "aws",

    # APIs
    "rest api",
    "restful api"
]

SYNONYMS = {

    "ml": "machine learning",
    "ai": "machine learning",
    "dl": "deep learning",

    "np": "numpy",
    "pd": "pandas",

    "js": "javascript",
    "ts": "typescript",

    "nodejs": "node",
    "reactjs": "react",

    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",

    "postgres": "postgresql",

    "restapi": "rest api",
    "restful api": "rest api"
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s+#]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def normalize_text(text):
    words = text.split()
    normalized = []

    for word in words:
        normalized.append(SYNONYMS.get(word, word))

    return " ".join(normalized)


def extract_skills(text):
    text = clean_text(text)
    text = normalize_text(text)

    found = set()

    for skill in SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.add(skill)

    return sorted(found)


def skills_to_vector(found_skills):
    skill_set = set(found_skills)
    return [1 if skill in skill_set else 0 for skill in SKILLS]


def process_resume(text):
    skills = extract_skills(text)

    return {
        "skills": skills,
        "vector": skills_to_vector(skills),
        "count": len(skills)
    }