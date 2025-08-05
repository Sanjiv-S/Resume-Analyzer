
# 🧠 Resume Analyzer – ATS-Friendly Resume Screening Tool

A smart web application that analyzes resumes against job descriptions using Natural Language Processing (NLP) and AI, providing detailed feedback and a section-wise ATS (Applicant Tracking System) score breakdown. It helps job seekers improve their resumes and better align them with job roles.

---

## 🚀 Features

- ✅ Resume PDF upload and parsing  
- 🧠 Intelligent resume scoring system (Format, Sections, Content, Skills, Style)  
- 🔍 Job Description-based keyword matching  
- 💡 Section-wise feedback and suggestions  
- 📊 Visual score progress bar  
- 📑 Highlights of matched and missing skills  
- 🧾 Grammar and contact information checks  
- 🧠 Fuzzy & semantic matching (using `fuzzywuzzy` and `sentence-transformers`)  
- 🧬 Categorized skill extraction (Languages, Tools, Projects, Certifications)  
- 🎯 Modern React frontend with animations and progress indicators  
- ⚙️ FastAPI backend for seamless resume analysis

---

## 🖼️ Demo

> Add a screen recording or image of your app here  
![Resume Analyzer Screenshot](./assets/screenshot.png)

---

## 🛠️ Tech Stack

| Frontend      | Backend        | NLP & AI        | Deployment       |
|---------------|----------------|------------------|------------------|
| React.js (with TailwindCSS) | FastAPI (Python) | spaCy, nltk, fuzzywuzzy, sentence-transformers | (Optional) Render / Vercel / Railway / GitHub Pages + Backend API |

---

## 📂 Project Structure

```
resume-analyzer/
├── backend/
│   ├── main.py
│   ├── scorer.py
│   ├── grammar.py
│   ├── skills.py
│   ├── contact_info.py
│   └── utils/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.js
│   │   └── ...
│   └── public/
├── README.md
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### ✅ Backend (FastAPI)

1. Navigate to backend directory:

```bash
cd backend
```

2. Create virtual environment & activate:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the server:

```bash
uvicorn main:app --reload
```

The backend will run on `http://127.0.0.1:8000`

---

### ✅ Frontend (React)

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install frontend dependencies:

```bash
npm install
```

3. Start the React development server:

```bash
npm start
```

Frontend runs on `http://localhost:3000` and connects with FastAPI.

---

## 📊 Sample Output

- **Overall ATS Score:** 78%
- **Section-wise Breakdown:**
  - Contact Info: ✅ Present
  - Education: ✅ Present
  - Experience: ⚠️ Years missing
  - Certifications: ❌ Missing
- **Detected Skills:** Python, SQL, Machine Learning, Pandas
- **Missing Keywords (based on JD):** OOP, REST APIs, Docker
- **Suggestions:** Add certifications section, include more job-relevant skills

---

## 📦 Key Dependencies

- **Backend:**  
  `fastapi`, `uvicorn`, `PyPDF2`, `spacy`, `nltk`, `fuzzywuzzy`, `sentence-transformers`

- **Frontend:**  
  `React`, `Axios`, `TailwindCSS`, `Framer Motion`, `ShadCN`, `Recharts`

---

## 🧠 Future Improvements

- 🧾 Add multilingual resume support  
- 🤖 GPT-based suggestion system for rewriting resumes  
- ☁️ Upload job description files instead of text input  
- 🔐 Authentication for storing analysis history  
- 📈 Analytics dashboard for users

---

## 👤 Author

**Sanjiv S**  
[LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

---

## 📝 License

This project is licensed under the MIT License.
