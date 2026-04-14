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

    except:
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

    def to_float(val):
        try:
            return float(val)
        except:
            return 0.0

    user_data = {
        "age": to_float(request.data.get("age")),
        "education_level": to_float(request.data.get("education_level")),
        "cgpa": to_float(request.data.get("cgpa")),
        "internships": to_float(request.data.get("internships")),
        "projects": to_float(request.data.get("projects")),
        "programming_languages": to_float(request.data.get("programming_languages")),
        "certifications": to_float(request.data.get("certifications")),
        "experience_years": to_float(request.data.get("experience_years")),
        "hackathons": to_float(request.data.get("hackathons")),
        "research_papers": to_float(request.data.get("research_papers")),
        "soft_skills_score": to_float(request.data.get("soft_skills_score")),
        "university_tier_2": to_float(request.data.get("university_tier_2")),
        "university_tier_3": to_float(request.data.get("university_tier_3")),
        "company_type_mid": to_float(request.data.get("company_type_mid")),
        "company_type_startup": to_float(request.data.get("company_type_startup")),
    }

    result = predict_resume(resume_text, user_data)

    return Response(result)