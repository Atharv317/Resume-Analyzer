# 🚀 AI Resume Analyzer (Hybrid ML + NLP)

An end-to-end AI-powered resume analysis system that evaluates candidate profiles using a hybrid approach combining structured features, NLP-based skill extraction, and machine learning-powered resume scoring.

---

## 🧠 Overview

AI Resume Analyzer automates resume screening by extracting text from uploaded resumes, identifying relevant skills using NLP techniques, engineering meaningful candidate features, and generating a score using a trained machine learning model.

The project integrates Django REST APIs, NLP preprocessing, feature engineering, and ML inference into a complete full-stack application with an interactive frontend.

---

## ✨ Features

* 📄 Resume Upload (PDF / DOCX)
* 🧹 Resume Text Extraction (PyPDF2, python-docx)
* 🧠 NLP-based Skill Extraction
* 🔄 Synonym-based Skill Normalization
* 📊 Machine Learning Resume Scoring
* 🎯 Candidate Evaluation & Classification
* ⚖️ Threshold Optimization using F1-Score
* ✅ Resume Validation & Spam Detection
* 📁 File Validation (Format & Size Checks)
* 📈 Experience Extraction from Date Ranges
* 📝 Structured Backend Logging
* ⚡ REST API using Django REST Framework
* 🌐 Interactive Frontend with Score Visualization
* 🏷️ Skill Tag Rendering
* 📊 Structured Resume Insights

---

## 🏗️ System Architecture

```text
Resume Upload
      │
      ▼
File Validation
      │
      ▼
Text Extraction
      │
      ▼
Resume Validation
      │
      ▼
Skill Extraction (NLP)
      │
      ▼
Feature Engineering
      │
      ▼
Machine Learning Model
      │
      ▼
Score + Candidate Evaluation
      │
      ▼
Frontend Visualization
```

---

## 📂 Project Structure

```text
Resume-Analyzer/
│
├── backend/
│   │
│   ├── backend/
│   │
│   ├── api/
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── templates/
│
├── ML/
│   │
│   ├── dataset/
│   │
│   ├── models/
│   │
│   └── src/
│       ├── extract.py
│       ├── predict.py
│       ├── skills.py
│       ├── validation.py
│       └── section_parser.py
│
└── README.md
```

---

## 🧪 Tech Stack

### 🔹 Backend

* Django
* Django REST Framework

### 🔹 Machine Learning

* Scikit-learn
* Logistic Regression

### 🔹 NLP

* Regex-based Skill Extraction
* Synonym Mapping
* Resume Section Parsing

### 🔹 Data Processing

* Pandas
* NumPy

### 🔹 File Handling

* PyPDF2
* python-docx

### 🔹 Frontend

* HTML
* CSS
* JavaScript

---

## 📊 Model Details

### Model

* Logistic Regression
* Binary Classification (interpreted as score-based candidate evaluation)

### Features Used

#### Academic Features

* CGPA
* Education Level

#### Experience Features

* Internships
* Projects
* Work Experience

#### NLP Features

* Skill Count
* Programming Language Count

#### Resume Features

* Resume Length
* Skill Density

---

## ⚙️ Feature Engineering

The model uses several engineered features to improve prediction quality.

### Derived Features

* Skill Density
* High CGPA Flag
* Low CGPA Flag
* High Experience Flag
* Fresher Flag

### Interaction Features

* CGPA × Skills
* Experience × Projects
* Experience × Internships
* Skills × Soft Skills

These features help the model capture relationships between candidate qualifications instead of evaluating each feature independently.

---

## ⚖️ Threshold Optimization

Instead of using the default classification threshold (0.50), the system uses:

```text
Threshold = 0.45
```

selected through F1-score optimization.

Benefits:

* Better balance between precision and recall
* More stable candidate evaluation
* Improved classification consistency

---

## 📈 Key Insights

* Default threshold (0.50) produced imbalanced predictions
* Threshold tuning improved prediction stability
* Feature engineering significantly improved model consistency
* Skill extraction quality directly impacts prediction quality
* Synthetic training data limits overall model performance
* System is designed as a resume scoring platform rather than a strict hiring classifier

---

## 🔌 API Endpoints

| Endpoint        | Method | Description                   |
| --------------- | ------ | ----------------------------- |
| `/api/test/`    | GET    | Health Check                  |
| `/api/upload/`  | POST   | Upload Resume & Extract Text  |
| `/api/analyze/` | POST   | Analyze Resume & Return Score |

---

## 🌐 Frontend Flow

1. Upload Resume or Paste Resume Text
2. Resume Text Auto-Filled
3. Enter Optional Candidate Details
4. Click Analyze
5. Backend Processing Begins
6. Results Displayed

### Output Includes

* 📊 Resume Score
* 🎯 Candidate Evaluation
* 🧠 Extracted Skills
* 📈 Confidence Level
* 📋 Structured Resume Data

---

## 🧠 How It Works

### Step 1

Resume uploaded through frontend.

### Step 2

Backend validates:

* File type
* File size
* Resume format

### Step 3

Text extracted from:

* PDF
* DOCX

### Step 4

Resume validation checks:

* Resume completeness
* Spam content
* Invalid input

### Step 5

NLP module extracts:

* Skills
* Technologies
* Programming languages

using skill dictionaries and synonym mapping.

### Step 6

Feature engineering pipeline creates:

* Raw features
* Derived features
* Interaction features

### Step 7

Features scaled using trained StandardScaler.

### Step 8

Machine learning model predicts candidate probability score.

### Step 9

Threshold applied.

### Step 10

Frontend displays final evaluation.

---

## 📝 Logging & Monitoring

The backend uses structured logging to monitor application activity.

### Logged Events

* Resume Upload Requests
* Resume Analysis Requests
* Validation Failures
* File Upload Errors
* Extraction Failures
* Successful Predictions

Benefits:

* Easier debugging
* Better monitoring
* Improved maintainability

---

## 🛡️ Validation & Security

Implemented validation mechanisms include:

* File Type Validation
* File Size Validation
* Empty Resume Detection
* Resume Format Validation
* Spam / Invalid Resume Detection

These checks improve reliability and prevent malformed inputs from entering the ML pipeline.

---

## ✅ Current Capabilities

* Resume Parsing & Validation
* NLP-based Skill Extraction
* Synonym-aware Skill Matching
* Experience Extraction from Date Ranges
* Resume Scoring using ML
* Feature Engineering Pipeline
* Confidence Score Generation
* Structured Logging
* File Upload Validation
* Interactive Frontend Visualization
* REST API Architecture

---

## 🏆 Highlights

* 🚀 Built a full-stack ML application from scratch
* 💡 Combined NLP and structured ML features
* ⚙️ Designed a complete feature engineering pipeline
* 🧩 Implemented custom interaction features
* 📊 Applied threshold tuning using F1-score optimization
* 🔍 Added file validation and resume validation mechanisms
* 📋 Implemented structured backend logging
* 📈 Fixed ongoing work-experience extraction using date parsing
* 🧠 Improved NLP skill extraction with synonym mapping
* 🔥 Solved multiple preprocessing and parsing edge cases
* 🎯 Built an interactive frontend with meaningful score interpretation

---

## 🔮 Future Improvements

### 🤖 AI & NLP Enhancements

* Advanced NLP using spaCy
* Transformer-based Skill Extraction
* Semantic Skill Matching
* Job Description Matching
* Resume Ranking Against JD
* AI Resume Feedback Assistant

### 🚀 Product Enhancements

* User Authentication
* User Profiles
* Resume Analysis History
* Job Recommendation System
* Premium Resume Insights
* Advanced Dashboard

### ☁️ Deployment & Scaling

* Docker Containerization
* AWS Deployment
* GCP / Azure Support
* Production-grade Logging
* Scalable API Infrastructure

---

## 👨‍💻 Author

### Atharv Shukla

* 💼 LinkedIn: https://www.linkedin.com/in/atharv-shukla315/
* 🧠 LeetCode: https://leetcode.com/AtharvShukla31
* 💻 GitHub: https://github.com/Atharv317

---

⭐ If you found this project useful, consider giving it a star.
