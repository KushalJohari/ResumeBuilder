# 🧠 AI-Powered Resume Builder

An intelligent Streamlit-based web application that helps users generate professional resumes effortlessly using AI. Users can input their details, get AI-generated summaries, and download their resumes as styled PDFs.

---

## 🚀 Features

- ✍️ **Interactive Resume Form**  
  Input personal info, education, work experience, skills, and projects.

- 🤖 **AI Summary Generation**  
  Auto-generate a compelling professional summary based on the job title using **Groq + LLaMA**.

- 📄 **PDF Export**  
  Download resumes in PDF format using **WeasyPrint** (cross-platform compatible).

- 🗂️ **Add/Delete Resume Sections**  
  Dynamically manage multiple experiences, education, or project entries. Includes delete buttons with `st.rerun()`.

- 💬 **Built-in Chatbot Assistant**  
  Ask resume-related queries via an AI chatbot in the sidebar — with input-clearing functionality.

---

## 🛠️ Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Backend**: Python, HTML, CSS
- **AI Models**: Groq’s [LLaMA](https://groq.com/)
- **PDF Generator**: [WeasyPrint](https://weasyprint.org/)
- **Deployment**: [Render](https://render.com/) *(Docker-compatible)*

---

## 📦 Installation

### 🔧 Prerequisites

- Python ≥ 3.8  
- `pip`  
- WeasyPrint system dependencies (GTK, Cairo, Pango, GDK)  
- Docker (optional, for deployment)

---

### 🐍 Local Setup

```bash
git clone https://github.com/KushalJohari/ResumeBuilder.git
cd ResumeBuilder
python -m venv venv
# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
