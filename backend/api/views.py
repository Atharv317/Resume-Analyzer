from django.shortcuts import render

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser
)

import logging
import PyPDF2
import docx

import os
import sys

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

from ML.src.predict import predict_resume
from ML.src.validation import validate_resume
from ML.src.extract import extract_all
from ML.src.skills import process_resume


logger = logging.getLogger(__name__)


def count_languages(skills):

    langs = {
        "python",
        "java",
        "c++",
        "javascript"
    }

    return len([
        s for s in skills
        if s in langs
    ])


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

    logger.info("Health check API called")

    return Response({
        "message": "Hurray IT is working"
    })


def home(request):
    return render(request, 'index.html')


def extract_text(file):

    try:

        text = ""

        if file.name.endswith('.pdf'):

            logger.info("Extracting text from PDF")

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        elif file.name.endswith('.docx'):

            logger.info("Extracting text from DOCX")

            doc = docx.Document(file)

            text = "\n".join([
                p.text for p in doc.paragraphs
            ])

        return text.strip()

    except Exception as e:

        logger.error(f"Error extracting text: {e}")

        return None


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_resume(request):

    logger.info("Resume upload request received")

    file = request.FILES.get("file")

    if not file:

        logger.warning("No file received")

        return Response({
            "error": "File not received"
        }, status=400)

    allowed_extensions = [".pdf", ".docx"]

    ext = os.path.splitext(file.name)[1].lower()

    if ext not in allowed_extensions:

        logger.warning(
            f"Invalid file type uploaded: {file.name}"
        )

        return Response({
            "error": "Only PDF and DOCX files are allowed"
        }, status=400)

    max_size_mb = 5

    if file.size>max_size_mb*1024*1024:

        logger.warning(
            f"File too large: {file.name}"
        )

        return Response({
            "error": "File size exceeds 5 MB limit"
        }, status=400)

    text = extract_text(file)

    if text is None:

        logger.error(
            f"Text extraction failed: {file.name}"
        )

        return Response({
            "error": "Failed to read the uploaded file"
        }, status=400)

    if not text.strip():

        logger.warning(
            f"Empty file uploaded: {file.name}"
        )

        return Response({
            "error": "Empty or unreadable file"
        }, status=400)

    logger.info(
        f"Resume uploaded successfully: {file.name}"
    )

    return Response({
        "message": "Uploaded successfully",
        "text_preview": text
    })


@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def analyze_resume(request):

    logger.info("Resume analysis started")

    resume_text = request.data.get("resume_text")

    if resume_text is None:

        logger.warning("Resume text missing")

        return Response({
            "error": "Please upload a valid PDF or DOCX file"
        }, status=400)

    resume_text = str(resume_text).strip()

    if not resume_text:

        logger.warning("Empty resume submitted")

        return Response({
            "error": "Empty resume",
            "type": "empty",
            "confidence": 0,
            "details": {
                "word_count": 0
            }
        })

    validation = validate_resume(resume_text)

    if not validation["is_resume"]:

        logger.warning("Resume validation failed")

        return Response({
            "error": validation["details"].get(
                "reason",
                "Invalid resume"
            ),

            "type": validation.get("error_type"),

            "confidence": validation.get(
                "confidence",
                0
            ),

            "details": validation.get(
                "details",
                {}
            )
        })

    extracted = extract_all(resume_text)

    skill_data = process_resume(resume_text)

    skills = skill_data["skills"]

    user_data = {

        "age": to_float(
            request.data.get("age")
        ),

        "education_level": extracted.get(
            "education_level",
            0
        ),

        "cgpa": get_val(
            request,
            "cgpa",
            extracted["cgpa"]
        ),

        "internships": get_val(
            request,
            "internships",
            extracted["internships"]
        ),

        "projects": get_val(
            request,
            "projects",
            extracted["projects"]
        ),

        "experience_years": get_val(
            request,
            "experience_years",
            extracted["experience_years"]
        ),

        "programming_languages": count_languages(
            skills
        ),

        "certifications": extracted.get(
            "certifications",
            0
        ),

        "hackathons": to_float(
            request.data.get("hackathons")
        ),

        "research_papers": to_float(
            request.data.get("research_papers")
        ),

        "soft_skills_score": extracted.get(
            "soft_skills_score",
            0
        ),

        "university_tier_2": to_float(
            request.data.get("university_tier_2")
        ),

        "university_tier_3": to_float(
            request.data.get("university_tier_3")
        ),

        "company_type_mid": to_float(
            request.data.get("company_type_mid")
        ),

        "company_type_startup": to_float(
            request.data.get("company_type_startup")
        )
    }

    result = predict_resume(
        resume_text,
        user_data,
        extracted
    )

    result["extracted"] = extracted
    result["validation"] = validation

    logger.info(
        f"Resume analyzed successfully. "
        f"Score: {result['score']}"
    )

    return Response(result)