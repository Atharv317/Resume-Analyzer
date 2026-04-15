from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

import PyPDF2
import docx
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BASE_DIR, "ML"))

from src.predict import predict_resume
from src.validation import validate_resume
from src.extract import extract_all
from src.skills import process_resume


def count_languages(skills):
    langs = {"python", "java", "c++", "javascript"}
    return len([s for s in skills if s in langs])


def to_float(val, fallback=0):
    try:
        return float(val)
    except:
        return fallback


def get_val(request, key, extracted_val):
    val = request.data.get(key)
    try:
        user_val = float(val)
    except:
        user_val = 0
    return max(user_val, extracted_val)


@api_view(['GET'])
def test_api(request):
    return Response({"message": "Hurray IT is working"})


def home(request):
    return render(request, 'index.html')


def extract_text(file):
    try:
        text = ""

        if file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        elif file.name.endswith('.docx'):
            doc = docx.Document(file)
            text = "\n".join([p.text for p in doc.paragraphs])

        return text.strip()

    except Exception as e:
        print("Error extracting text:", e)
        return None


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_resume(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "File not received"}, status=400)

    text = extract_text(file)

    if text is None:
        return Response({"error": "Invalid file format. Upload PDF or DOCX"}, status=400)

    if not text.strip():
        return Response({"error": "Empty or unreadable file"}, status=400)

    return Response({
        "message": "Uploaded successfully",
        "text_preview": text
    })


@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def analyze_resume(request):
    file = request.FILES.get("file")

    if file:
        resume_text = extract_text(file)
    else:
        resume_text = request.data.get("resume_text")

    if resume_text is None:
        return Response({"error": "Please upload a valid PDF or DOCX file"}, status=400)

    resume_text = str(resume_text).strip()

    if not resume_text:
        return Response({
            "error": "Empty resume",
            "type": "empty",
            "confidence": 0,
            "details": {"word_count": 0}
        })

    validation = validate_resume(resume_text)

    if not validation["is_resume"]:
        return Response({
            "error": validation["details"].get("reason", "Invalid resume"),
            "type": validation.get("error_type"),
            "confidence": validation.get("confidence", 0),
            "details": validation.get("details", {})
        })

    extracted = extract_all(resume_text)

    skill_data = process_resume(resume_text)
    skills = skill_data["skills"]

    user_data = {
        "age": to_float(request.data.get("age")),
        "education_level": extracted.get("education_level", 0),
        "cgpa": get_val(request, "cgpa", extracted["cgpa"]),
        "internships": get_val(request, "internships", extracted["internships"]),
        "projects": get_val(request, "projects", extracted["projects"]),
        "experience_years": get_val(request, "experience_years", extracted["experience_years"]),
        "programming_languages": count_languages(skills),
        "certifications": extracted.get("certifications", 0),
        "hackathons": to_float(request.data.get("hackathons")),
        "research_papers": to_float(request.data.get("research_papers")),
        "soft_skills_score": extracted.get("soft_skills_score", 0),
        "university_tier_2": to_float(request.data.get("university_tier_2")),
        "university_tier_3": to_float(request.data.get("university_tier_3")),
        "company_type_mid": to_float(request.data.get("company_type_mid")),
        "company_type_startup": to_float(request.data.get("company_type_startup")),
    }

    result = predict_resume(resume_text, user_data, extracted)

    result["extracted"] = extracted
    result["validation"] = validation

    return Response(result)