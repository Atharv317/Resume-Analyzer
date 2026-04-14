import re
from collections import Counter

KEYWORDS = ["education", "experience", "skills", "projects"]
COMMON_SKILLS = ["python", "java", "ml", "machine learning", "django"]

STOPWORDS = set([
    "the","and","of","to","in","a","is","for","on","with",
    "as","by","an","at","from","or","that","this"
])


def validate_resume(text):
    try:
        raw_clean = re.sub(r'<[^>]+>', '', text)
        raw_clean = raw_clean.strip()

        words_raw = re.findall(r'[a-zA-Z]+', raw_clean)
        unique_raw_words = set(words_raw)

        if not raw_clean or len(words_raw) == 0:
            return {
                "is_resume": False,
                "error_type": "empty",
                "confidence": 0,
                "details": {
                    "word_count": 0,
                    "reason": "Empty input"
                }
            }

        if len(unique_raw_words) <= 1:
            return {
                "is_resume": False,
                "error_type": "empty",
                "confidence": 0,
                "details": {
                    "word_count": len(words_raw),
                    "reason": "No meaningful content"
                }
            }

        text = re.sub(r'<[^>]+>', ' ', text)
        text_lower = text.lower()

        words = re.findall(r'\b[a-zA-Z]+\b', text_lower)
        filtered_words = [w for w in words if w not in STOPWORDS]

        word_count = len(filtered_words)

        if word_count == 0:
            return {
                "is_resume": False,
                "error_type": "empty",
                "confidence": 0,
                "details": {
                    "word_count": 0,
                    "reason": "No meaningful content"
                }
            }

        word_freq = Counter(filtered_words)
        unique_words = len(word_freq)

        unique_ratio = unique_words / (word_count + 1)
        max_repeat = max(word_freq.values()) if word_freq else 0
        repeat_ratio = max_repeat / (word_count + 1)

        keyword_score = sum(
            1 for kw in KEYWORDS if re.search(rf'\b{kw}\b', text_lower)
        )

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
        has_phone = bool(re.search(r'(\+?\d{1,3}[-\s]?)?\d{10}', text))

        sentence_like = bool(
            re.search(r'\b(i|worked|developed|built|designed)\b', text_lower)
        )

        bullet_points = len(re.findall(r'•|-|\*', text))

        has_structure = keyword_score >= 1 or skill_hits >= 1 or sentence_like

        if not has_structure:
            return {
                "is_resume": False,
                "error_type": "invalid_format",
                "confidence": 0,
                "details": {
                    "word_count": word_count,
                    "reason": "Not a resume"
                }
            }

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

        if word_count < 10:
            return {
                "is_resume": False,
                "error_type": "too_short",
                "confidence": round(score / 5, 2),
                "details": {
                    "word_count": word_count,
                    "reason": "Too short"
                }
            }

        spam_flag = False

        if repeat_ratio > 0.3:
            spam_flag = True

        if unique_ratio < 0.25:
            spam_flag = True

        if spam_flag:
            return {
                "is_resume": False,
                "error_type": "spam",
                "confidence": round(score / 5, 2),
                "details": {
                    "word_count": word_count,
                    "spam_detected": True,
                    "reason": "Spam detected"
                }
            }

        if word_count < 30:
            return {
                "is_resume": False,
                "error_type": "insufficient_content",
                "confidence": round(score / 5, 2),
                "details": {
                    "word_count": word_count,
                    "reason": "Insufficient content"
                }
            }

        is_resume = (score >= 3)

        return {
            "is_resume": is_resume,
            "error_type": None if is_resume else "invalid_format",
            "confidence": round(score / 5, 2),
            "details": {
                "word_count": word_count,
                "unique_ratio": round(unique_ratio, 2),
                "max_repeat": max_repeat,
                "repeat_ratio": round(repeat_ratio, 2),
                "keywords_found": keyword_score,
                "skills_found": skill_hits,
                "spam_detected": False
            }
        }

    except Exception as e:
        return {
            "is_resume": False,
            "error_type": "processing_error",
            "confidence": 0,
            "details": {
                "reason": str(e)
            }
        }