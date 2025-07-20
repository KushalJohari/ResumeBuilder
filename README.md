# 🧠 AI-Powered Resume Builder

An intelligent Streamlit-based web application that helps users generate professional resumes effortlessly using AI. Users can input their details, get AI-generated summaries, and download their resumes as PDFs.

---

## 🚀 Features

- ✍️ **Interactive Resume Form**  
  Input personal info, education, work experience, skills, and projects.

- 🤖 **AI Summary Generation**  
  Auto-generate a compelling professional summary based on the job title using **LLM** (Groq).

- 📄 **PDF Export**  
  Download resumes in PDF format using **WeasyPrint** (cross-platform compatible).

- 💬 **Built-in Chatbot Assistant**  
  Ask resume-related queries via an AI chatbot in the sidebar.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Backend**: Python, HTML, CSS  
- **AI Models**: Groq’s LLaMA
- **PDF Generator**: WeasyPrint  
- **Deployment Ready**: Docker-compatible

---

## 📦 Installation

### 🔧 Prerequisites

- Python ≥ 3.8  
- pip  
- WeasyPrint dependencies (GTK installed)  
- Docker (optional for deployment)

### 🐍 Local Setup

```bash
git clone https://github.com/yourusername/ResumeBuilder.git
cd ResumeBuilder
python -m venv venv
On Windows use: venv\Scripts\activate
pip install -r requirements.txt
