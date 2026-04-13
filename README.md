# 🚀 AI Resume Analyzer (Hybrid ML + NLP)

An end-to-end AI-powered resume analysis system that evaluates candidate profiles using a hybrid approach combining structured data and NLP-based skill extraction.

---

## 🧠 Overview

This project automates resume screening by extracting text from resumes, identifying relevant skills using NLP, and predicting candidate suitability using a machine learning model.

It integrates backend APIs, feature engineering, and a trained ML model into a complete pipeline.

---

## ✨ Features

- 📄 Resume Upload (PDF / DOCX)
- 🧹 Text Extraction (PyPDF2, python-docx)
- 🧠 NLP-based Skill Extraction
- 📊 Machine Learning Resume Scoring
- 🎯 Candidate Selection Prediction
- ⚖️ Threshold Optimization (F1-score based)
- ⚡ REST API using Django
- 🌐 Basic Frontend for interaction

---

## 🏗️ System Architecture

Resume → Text Extraction → NLP Skill Processing → Feature Engineering → ML Model → Prediction

---

## 🧪 Tech Stack

### 🔹 Backend
- Django
- Django REST Framework

### 🔹 Machine Learning
- Scikit-learn (Logistic Regression)

### 🔹 NLP
- Regex-based Skill Extraction

### 🔹 Data Processing
- Pandas, NumPy

### 🔹 File Handling
- PyPDF2, python-docx

### 🔹 Frontend
- HTML, CSS, JavaScript

---

## 📊 Model Details

- **Model:** Logistic Regression  
- **Type:** Binary Classification (Selected / Not Selected)

### Features Used:
- Academic: CGPA, Education Level  
- Experience: Internships, Projects, Work Experience  
- Skills: Skill Count (extracted via NLP)  

### Engineered Features:
- Skill Density  
- CGPA-based flags  
- Experience-based flags  
- Interaction features  

### Threshold:
- Optimized to **0.45** using F1-score

---

## 📈 Key Insights

- Default threshold (0.5) produced biased predictions  
- Threshold tuning improved class balance  
- Feature engineering improved model behavior  
- Synthetic dataset limited model performance (ROC AUC ≈ 0.5)  
- Focus on building a scalable hybrid ML pipeline  

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|------------|
| `/api/test/` | GET | Health check |
| `/api/upload/` | POST | Upload resume & extract text |
| `/api/analyze/` | POST | Analyze resume |

---

## 🌐 Frontend Flow

1. Upload resume OR paste text  
2. Extracted text displayed  
3. Enter optional details (age, CGPA)  
4. Click Analyze  
5. Get:
   - Score  
   - Selection result  
   - Extracted skills  

---

## 🚀 Setup & Run

git clone https://github.com/Atharv317/Resume-Analyzer.git  
cd Resume-Analyzer  

pip install -r requirements.txt  

python manage.py runserver  

---

## 🧠 How It Works

1. Resume uploaded  
2. Text extracted (PDF/DOCX)  
3. NLP extracts skills  
4. Feature engineering applied  
5. Features scaled  
6. ML model predicts probability  
7. Threshold applied → final decision  

---

## 🏆 Highlights

- 🚀 Built full-stack ML system from scratch  
- 💡 Integrated NLP with structured ML features  
- ⚙️ Designed feature engineering pipeline  
- 📊 Implemented threshold tuning for better predictions  
- 🔥 Solved real-world ML deployment issues  

---

## 🔮 Future Improvements
 
- Advanced NLP (spaCy / Transformers)  
- Skill embeddings (semantic matching)  
- Resume section detection  
- Auto extraction of CGPA, experience  
- Improved UI/UX  
- Deployment (Docker / Cloud)

---

## 👨‍💻 Author

**Atharv Shukla**

- 💼 LinkedIn: https://www.linkedin.com/in/atharv-shukla315/  
- 🧠 LeetCode: https://leetcode.com/AtharvShukla31  

---

⭐ Star this repo if you find it useful!
