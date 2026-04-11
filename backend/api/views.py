from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import extract_skills
from .models import Resume
from .serializers import ResumeSerializer
import PyPDF2
import docx

@api_view(['GET'])
def test_api(request):
    return Response({"message": "Hurray IT is working"})

def extract_text(file):
    if file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text =""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    return "Invalid File! Please Provide either PDF or Docx File"

@api_view(['POST'])
def upload_resume(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "File not received"})

    text = extract_text(file)

    skills = extract_skills(text)

    return Response({
        "message": "Uploaded",
        "text_preview": text[:500],
        "skills":skills,
    })