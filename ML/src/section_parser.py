import re

SECTION_MAP = {
    "education": ["education", "academic background"],
    "experience": ["experience", "work experience", "professional experience"],
    "projects": ["projects", "personal projects"],
    "skills": ["skills", "technical skills"]
}


def normalize_header(line):
    line = line.strip().lower()
    line = re.sub(r'[^a-z\s]', '', line)

    for key, variants in SECTION_MAP.items():
        for v in variants:
            if line == v:
                return key
    return None


def split_sections(text):
    sections = {k: "" for k in SECTION_MAP}
    sections["other"] = ""

    current_section = "other"

    lines = text.split("\n")

    for line in lines:
        header = normalize_header(line)

        if header:
            current_section = header
            continue

        sections[current_section] += line + "\n"

    return sections