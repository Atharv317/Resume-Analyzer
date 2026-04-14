import re
from collections import Counter

KEYWORDS = ["education", "experience", "skills", "projects"]
COMMON_SKILLS = ["python", "java", "ml", "machine learning", "django"]

STOPWORDS = set([
    "the","and","of","to","in","a","is","for","on","with",
    "as","by","an","at","from","or","that","this"
])


def validate_resume(text):

    raw_clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'[^a-zA-Z]', '', raw_clean)

    if len(clean) < 5:
        return {
            "is_resume": False,
            "confidence": 0,
            "details": {
                "word_count": 0,
                "unique_ratio": 0,
                "max_repeat": 0,
                "repeat_ratio": 0,
                "keywords_found": 0,
                "skills_found": 0,
                "spam_detected": False,
                "reason": "Empty input"
            }
        }

    text = re.sub(r'<[^>]+>', ' ', text)
    text_lower = text.lower()

    words = re.findall(r'\b[a-zA-Z]+\b', text_lower)
    filtered_words = [w for w in words if w not in STOPWORDS]

    word_count = len(filtered_words)

    word_freq = Counter(filtered_words)
    unique_words = len(word_freq)

    keyword_score = sum(1 for kw in KEYWORDS if re.search(rf'\b{kw}\b', text_lower))

    skill_hits = 0
    seen = set()
    for skill in COMMON_SKILLS:
        if re.search(rf'\b{re.escape(skill)}\b', text_lower):
            if skill == "ml" and "machine learning" in text_lower:
                continue
            if skill not in seen:
                skill_hits += 1
                seen.add(skill)

    has_email = bool(re.search(r'\S+@\S+', text))
    has_phone = bool(re.search(r'\b\d{10}\b', text))

    unique_ratio = unique_words / (word_count + 1)
    max_repeat = max(word_freq.values()) if word_freq else 0
    repeat_ratio = max_repeat / (word_count + 1)

    sentence_like = bool(re.search(r'\b(i|worked|developed|built|designed)\b', text_lower))
    bullet_points = len(re.findall(r'•|-|\*', text))

    score = 0

    if word_count > 80 or (word_count > 20 and keyword_score >= 3):
        score += 1

    if keyword_score >= 2:
        score += 1

    if has_email or has_phone:
        score += 1

    if skill_hits >= 2:
        score += 1

    if sentence_like or bullet_points >= 2:
        score += 1

    spam_flag = False

    if repeat_ratio > 0.3 and word_count > 10:
        spam_flag = True

    if unique_ratio < 0.25 and word_count > 15:
        spam_flag = True

    if word_count < 15:
        return {
            "is_resume": False,
            "confidence": round(score / 5, 2),
            "details": {
                "word_count": word_count,
                "unique_ratio": round(unique_ratio, 2),
                "max_repeat": max_repeat,
                "repeat_ratio": round(repeat_ratio, 2),
                "keywords_found": keyword_score,
                "skills_found": skill_hits,
                "spam_detected": False,
                "reason": "Too short / insufficient content"
            }
        }

    is_resume = (score >= 3) and not spam_flag

    return {
        "is_resume": is_resume,
        "confidence": round(score / 5, 2),
        "details": {
            "word_count": word_count,
            "unique_ratio": round(unique_ratio, 2),
            "max_repeat": max_repeat,
            "repeat_ratio": round(repeat_ratio, 2),
            "keywords_found": keyword_score,
            "skills_found": skill_hits,
            "spam_detected": spam_flag
        }
    }