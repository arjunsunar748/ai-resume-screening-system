# 🤖 AI Resume Screening & ATS System

An AI-powered Applicant Tracking System (ATS) that automatically analyzes resumes, extracts key information, matches candidates with job descriptions, and ranks applicants based on their suitability. This project helps recruiters reduce manual screening time while providing candidates with accurate resume analysis and feedback.

---

## 🚀 Features

### 👤 User Features
- Upload Resume (PDF/DOCX)
- Upload Job Description
- AI Resume Analysis
- Resume Score (0-100)
- ATS Compatibility Check
- Skill Matching
- Experience Matching
- Education Matching
- Keyword Analysis
- Missing Skills Detection
- Resume Improvement Suggestions
- Candidate Dashboard
- Resume History

### 🛠️ Admin Features
- Admin Dashboard
- Manage Users
- Manage Job Descriptions
- View All Resumes
- Candidate Ranking
- Analytics Dashboard
- Download Reports
- System Logs

### 🤖 AI Features
- Resume Parsing
- Job Description Parsing
- Semantic Similarity Matching
- Skill Extraction
- Experience Extraction
- Education Extraction
- Named Entity Recognition (NER)
- Resume Ranking
- AI Recommendation Engine
- AI Feedback Generation

---

# 📊 System Workflow

```
Resume Upload
      │
      ▼
Resume Parser
      │
      ▼
Information Extraction
      │
      ▼
Job Description Parser
      │
      ▼
Skill Matching
      │
      ▼
Semantic Similarity
      │
      ▼
ATS Score Generation
      │
      ▼
Candidate Ranking
      │
      ▼
Final AI Report
```

---

# 🏗️ Tech Stack

## Frontend

- React.js
- Vite
- Tailwind CSS
- React Router
- Axios

## Backend

- FastAPI
- Python
- Uvicorn

## Database

- PostgreSQL

## AI & Machine Learning

- Hugging Face Transformers
- Sentence Transformers
- spaCy
- PyMuPDF
- python-docx
- scikit-learn
- NumPy
- Pandas

## Authentication

- JWT Authentication
- Password Hashing (bcrypt)

## Deployment

- Vercel (Frontend)
- Render / Railway (Backend)
- Neon PostgreSQL
- Hugging Face Hub (Models)

---

# 📁 Project Structure

```
AI-Resume-Screening-System/
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── database/
│   ├── ai/
│   ├── utils/
│   ├── uploads/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── assets/
│   └── package.json
│
├── datasets/
├── notebooks/
├── docs/
└── README.md
```

---

# 🧠 AI Pipeline

```
Resume
      │
      ▼
Text Extraction
      │
      ▼
Cleaning
      │
      ▼
Skill Extraction
      │
      ▼
Embedding Generation
      │
      ▼
Job Description Embedding
      │
      ▼
Cosine Similarity
      │
      ▼
Resume Score
      │
      ▼
Ranking
```

---

# 📈 Resume Score Factors

| Criteria | Weight |
|-----------|--------|
| Skills Match | 35% |
| Experience | 25% |
| Education | 15% |
| Keywords | 15% |
| Resume Quality | 10% |

---

# 🖥️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ai-resume-screening-system.git
```

## Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 📦 Environment Variables

```
DATABASE_URL=

SECRET_KEY=

JWT_ALGORITHM=

ACCESS_TOKEN_EXPIRE_MINUTES=

HF_TOKEN=
```

---

# 📊 API Endpoints

### Authentication

```
POST /register

POST /login
```

### Resume

```
POST /resume/upload

GET /resume/history

DELETE /resume/{id}
```

### Job Description

```
POST /job/upload

GET /jobs
```

### AI

```
POST /ai/analyze

POST /ai/match

GET /ai/report/{id}
```

---

# 📸 Screenshots

- Login Page
- Dashboard
- Resume Upload
- ATS Score
- Candidate Ranking
- Admin Dashboard

(Add screenshots here after development)

---

# 🎯 Future Improvements

- AI Interview Integration
- Resume Builder
- Multi-language Resume Parsing
- OCR Support
- Email Notifications
- Recruiter Portal
- Company Dashboard
- AI Chat Assistant
- Interview Scheduling
- Analytics & Reports

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Arjun Sunar**

Computer Science Engineering Student

Mid-West University, Nepal

GitHub: https://github.com/arjunsunar748

LinkedIn: https://www.linkedin.com/in/arjun-sunar-428331348/

---

## ⭐ Support

If you like this project, please give it a ⭐ on GitHub!
