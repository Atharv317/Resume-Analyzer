# 🚀 AI Resume Analyzer (Hybrid ML + NLP)

An end-to-end AI-powered resume analysis system that evaluates candidate profiles using a hybrid approach combining structured data and NLP-based skill extraction.

---

## 🧠 Features

* 📄 Resume Upload (PDF/DOCX)
* 🧹 Text Extraction (PyPDF2, python-docx)
* 🧠 NLP-based Skill Extraction
* 📊 Hybrid ML Model (Structured + Skills)
* 🎯 Resume Scoring System
* ⚖️ Threshold Optimization for Balanced Predictions
* ⚡ Django REST API Backend

---

## 🏗️ Architecture

Resume → Text Extraction → Skill Extraction → Feature Engineering → ML Model → Score

---

## 🧪 Tech Stack

* Backend: Django, Django REST Framework
* ML: Scikit-learn (Logistic Regression)
* NLP: Regex-based skill extraction
* Data: Pandas, NumPy
* File Handling: PyPDF2, python-docx

---

## 📊 Model Details

* Model: Logistic Regression
* Features:

  * Structured Data (CGPA, internships, experience, etc.)
  * Skill Vector (Python, ML, Django, etc.)
* Threshold: **0.45 (optimized using F1-score)**

---

## 📈 Key Insights

* Default threshold (0.5) led to biased predictions
* Threshold tuning improved real-world balance
* Synthetic dataset resulted in limited model discrimination (ROC AUC ≈ 0.5)
* Focus was on building a scalable hybrid pipeline

---

## 🔌 API Endpoints

### Test API

GET /api/test/

### Upload Resume

POST /api/upload/

### Analyze Resume

POST /api/analyze/

---

## 🚀 How to Run

git clone https://github.com/Atharv317/Resume-Analyzer.git
cd Resume-Analyzer
pip install -r requirements.txt
python manage.py runserver

---

## 🧠 Future Improvements

* Real resume dataset
* Advanced NLP (spaCy / transformers)
* Skill embeddings
* Frontend UI
* Deployment

---

## 👨‍💻 Author

Atharv Shukla
