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


@api_view(['GET'])
def test_api(request):
    return Response({"message": "Hurray IT is working"})


def home(request):
    return render(request, 'index.html')


def extract_text(file):
    try:
        if file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()

        elif file.name.endswith('.docx'):
            doc = docx.Document(file)
            return "\n".join([p.text for p in doc.paragraphs]).strip()

        return None
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

    if not text:
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

    if not resume_text:
        return Response({"error": "No resume text provided"}, status=400)

    user_data = {
        "age": float(request.data.get("age", 0)),
        "education_level": float(request.data.get("education_level", 0)),
        "cgpa": float(request.data.get("cgpa", 0)),
        "internships": float(request.data.get("internships", 0)),
        "projects": float(request.data.get("projects", 0)),
        "programming_languages": float(request.data.get("programming_languages", 0)),
        "certifications": float(request.data.get("certifications", 0)),
        "experience_years": float(request.data.get("experience_years", 0)),
        "hackathons": float(request.data.get("hackathons", 0)),
        "research_papers": float(request.data.get("research_papers", 0)),
        "soft_skills_score": float(request.data.get("soft_skills_score", 0)),
        "university_tier_2": float(request.data.get("university_tier_2", 0)),
        "university_tier_3": float(request.data.get("university_tier_3", 0)),
        "company_type_mid": float(request.data.get("company_type_mid", 0)),
        "company_type_startup": float(request.data.get("company_type_startup", 0)),
    }

    result = predict_resume(resume_text, user_data)

    return Response(result)