# 🚀 AI Resume Analyzer (Hybrid ML + NLP)

An end-to-end AI-powered resume analysis system that evaluates candidate profiles using a hybrid approach combining structured features and NLP-based skill extraction.

---

## 🧠 Overview

This project automates resume screening by extracting text from resumes, identifying relevant skills using NLP, and scoring candidate profiles using a machine learning model.

It integrates backend APIs, feature engineering, and a trained ML model into a complete pipeline with a clean interactive UI.

---

## ✨ Features

* 📄 Resume Upload (PDF / DOCX)
* 🧹 Text Extraction (PyPDF2, python-docx)
* 🧠 NLP-based Skill Extraction (with synonym handling)
* 📊 Machine Learning Resume Scoring
* 🎯 Candidate Evaluation (Score-based classification)
* ⚖️ Threshold Optimization (F1-score based)
* ⚡ REST API using Django
* 🌐 Interactive Frontend with score visualization
* 🏷️ Skill Tag Rendering (clean UI display)

---

## 🏗️ System Architecture

Resume → Text Extraction → Skill Extraction → Feature Engineering → ML Model → Score + Evaluation

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

### Features Used:

* Academic: CGPA
* Experience: Internships, Projects, Work Experience
* Skills: Skill Count (NLP extracted)
* Resume: Length, Skill Density

### Engineered Features:

* Skill Density
* CGPA flags
* Experience flags
* Interaction features (e.g., CGPA × Skills, Experience × Projects)

### Threshold:

* Optimized to **0.45** using F1-score

---

## 📈 Key Insights

* Default threshold (0.5) led to imbalanced predictions
* Threshold tuning improved model stability
* Feature engineering improved decision consistency
* Synthetic dataset limited overall accuracy (~65%)
* System designed to behave as a **resume scoring tool rather than strict classifier**

---

## 🔌 API Endpoints

| Endpoint        | Method | Description                     |
| --------------- | ------ | ------------------------------- |
| `/api/test/`    | GET    | Health check                    |
| `/api/upload/`  | POST   | Upload resume & extract text    |
| `/api/analyze/` | POST   | Analyze resume and return score |

---

## 🌐 Frontend Flow

1. Upload resume OR paste text
2. Extracted text auto-filled
3. Enter optional details
4. Click Analyze
5. Get:

   * 📊 Score (visual bar)
   * 🧾 Candidate evaluation (Strong / Good / Needs Improvement)
   * 🧠 Extracted skills (tag-based UI)
   * 📊 Structured extracted data

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
2. Text extracted (PDF/DOCX)
3. Skills extracted using NLP + synonyms
4. Feature engineering applied
5. Features scaled
6. ML model predicts probability
7. Threshold applied → score & evaluation

---

## 🏆 Highlights

* 🚀 Built full-stack ML system from scratch
* 💡 Combined NLP + structured ML features
* ⚙️ Designed complete feature engineering pipeline
* 📊 Implemented threshold tuning
* 🔥 Solved real-world issues like feature mismatch & preprocessing bugs
* 🎯 Built user-friendly UI with meaningful interpretation

---

## 🔮 Future Improvements

- 🤖 Advanced NLP (spaCy / Transformers) for better context understanding  
- 🧠 Skill Semantic Matching (embedding-based skill similarity)  
- 🎯 Job Description Matching & Resume Scoring  
- 📄 Resume Section Parsing (Education, Experience, Skills auto-detection)  
- 📊 Improved Dataset (real-world resumes & job data)  
- 🤖 AI Assistant for resume feedback and suggestions  

### 🚀 Product Enhancements
- 💼 Job Recommendation System based on user profile  
- 🔐 User Authentication & Profile Management  
- 💳 Payment Gateway Integration (premium features / resume insights)  
- 🎨 Advanced UI/UX (dashboard, analytics, better visualization)  

### ☁️ Deployment & Scaling
- 🐳 Docker-based containerization  
- ☁️ Cloud Deployment (AWS / GCP / Azure)  
- 📈 Scalable API with production-ready setup
  
---

## 👨‍💻 Author

**Atharv Shukla**

* 💼 LinkedIn: https://www.linkedin.com/in/atharv-shukla315/
* 🧠 LeetCode: https://leetcode.com/AtharvShukla31

---

⭐ Star this repo if you find it useful!
