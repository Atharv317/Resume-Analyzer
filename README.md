# 🚀 AI Resume Analyzer (Hybrid ML + NLP)

An end-to-end AI-powered resume analysis system that evaluates candidate profiles using a hybrid approach combining structured features and NLP-based skill extraction.

---

## 🧠 Overview

This project automates resume screening by extracting text from resumes, identifying relevant skills using NLP, and scoring candidate profiles using a machine learning model.

It integrates backend APIs, feature engineering, and a trained ML model into a complete pipeline with a responsive interactive UI.

---

## ✨ Features

* 📄 Resume Upload (PDF / DOCX)
* 🧹 Text Extraction (PyPDF2, python-docx)
* 🧠 NLP-based Skill Extraction with Synonym Handling
* 📊 ML-based Resume Scoring
* 🎯 Candidate Evaluation (Score-based Classification)
* ⚖️ Threshold Optimization (F1-score based)
* ✅ Resume Validation & Spam Detection
* ⚡ REST API using Django
* 🌐 Interactive Frontend with Score Visualization
* 🏷️ Skill Tag Rendering (clean UI display)

---

## 🏗️ System Architecture

Resume → Text Extraction → Skill Extraction → Feature Engineering → ML Model → Score + Evaluation

---

## 📂 Project Structure

```text
Resume-Analyzer/
│
├── backend/
│   ├── backend/
│   ├── api/
│   └── templates/
│
├── ML/
│   ├── dataset/
│   ├── models/
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

* Scikit-learn (Logistic Regression)

### 🔹 NLP

* Regex-based Skill Extraction with Synonym Mapping

### 🔹 Data Processing

* Pandas, NumPy

### 🔹 File Handling

* PyPDF2, python-docx

### 🔹 Frontend

* HTML, CSS, JavaScript

---

## 📊 Model Details

* **Model:** Logistic Regression
* **Type:** Binary Classification (interpreted as score-based evaluation)

### Features Used

* Academic: CGPA
* Experience: Internships, Projects, Work Experience
* Skills: NLP-based Skill Count
* Resume Features: Resume Length, Skill Density

### Engineered Features

* Skill Density
* CGPA Flags
* Experience Flags
* Interaction Features
  * CGPA × Skills
  * Experience × Projects
  * Experience × Internships
  * Skills × Soft Skills

### Threshold

* Optimized to **0.45** using F1-score

---

## 📈 Key Insights

* Default threshold (0.5) led to imbalanced predictions
* Threshold tuning improved prediction stability
* Feature engineering improved decision consistency
* Model performance was influenced by limitations of synthetic training data
* System designed to provide profile-based resume evaluation and scoring

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/test/` | GET | Health Check |
| `/api/upload/` | POST | Upload Resume & Extract Text |
| `/api/analyze/` | POST | Analyze Resume & Return Score |

---

## 🌐 Frontend Flow

1. Upload Resume OR Paste Text
2. Extracted text auto-filled
3. Enter optional details
4. Click Analyze
5. Get:

   * 📊 Score Visualization
   * 🧾 Candidate Evaluation
   * 🧠 Extracted Skills
   * 📊 Structured Extracted Data

---

## 🚀 Setup & Run

```bash
git clone https://github.com/Atharv317/Resume-Analyzer.git

cd Resume-Analyzer

pip install -r requirements.txt

python manage.py runserver
```

---

## 🧠 How It Works

1. Resume uploaded
2. Text extracted from PDF/DOCX
3. Skills extracted using NLP + synonym mapping
4. Feature engineering applied
5. Features scaled using trained scaler
6. ML model predicts probability
7. Threshold applied → score & evaluation

---

## ✅ Current Capabilities

* Resume Parsing & Validation
* NLP-based Skill Extraction
* Resume Scoring using ML
* Feature Engineering Pipeline
* Experience & Project Extraction
* Interactive Frontend Visualization
* REST API-based Architecture
* Spam & Invalid Resume Detection

---

## 🏆 Highlights

* 🚀 Built full-stack ML system from scratch
* 💡 Combined NLP + structured ML features
* ⚙️ Designed complete feature engineering pipeline
* 🧩 Implemented custom interaction features
* 📊 Implemented threshold tuning
* 🔥 Solved real-world preprocessing & parsing issues
* 🎯 Built responsive frontend with meaningful interpretation

---

## 🔮 Future Improvements

### 🤖 AI & NLP Enhancements

* Advanced NLP (spaCy / Transformers)
* Skill Semantic Matching
* Job Description Matching & Resume Scoring
* Resume Section Parsing
* Improved Dataset with Real-world Resume Data
* AI Assistant for Resume Feedback

### 🚀 Product Enhancements

* 💼 Job Recommendation System
* 🔐 User Authentication & Profile Management
* 💳 Payment Gateway Integration
* 🎨 Advanced Dashboard & UI/UX Improvements

### ☁️ Deployment & Scaling

* 🐳 Docker-based Containerization
* ☁️ Cloud Deployment (AWS / GCP / Azure)
* 📈 Production-ready Scalable API

---

## 👨‍💻 Author

**Atharv Shukla**

* 💼 LinkedIn: https://www.linkedin.com/in/atharv-shukla315/
* 🧠 LeetCode: https://leetcode.com/AtharvShukla31

---

⭐ Star this repo if you find it useful!
