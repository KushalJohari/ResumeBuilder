import streamlit as st
import streamlit.components.v1 as components
from weasyprint import HTML
from template import resume_template, resume_ats_template, extract_text_from_resume
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import calendar
import datetime
load_dotenv()

def generate_pdf(html_code):
    return HTML(string=html_code).write_pdf()

months = list(calendar.month_name)[1:]
current_year = datetime.datetime.now().year
Years = [str(year) for year in range(current_year - 10, current_year + 1)]
GradYears = [str(year) for year in range(current_year - 10, current_year + 10)]


model = ChatGroq(model="llama3-8b-8192", streaming=True, api_key=os.environ["GROQ_API_KEY"])

prompt_template = PromptTemplate(template="You are a professional resume writer. Write a **2-3 line summary** (not more) for the resume of a candidate applying for a job as {job}. Do not include key strengths, accomplishments, education, or any headings.", input_variables=["job"])

ats_template = PromptTemplate( input_variables=["resume"],
                template=""" You are an AI-powered resume reviewer acting like an Applicant Tracking System (ATS).
                Evaluate the following resume it should have **project, education** if not that marks will go down. Provide:
                - ATS-style Score out of 100
                - Strengths (bullet points)
                - Weaknesses (bullet points)

                Resume:
                {resume}
                """)
ats_chain = ats_template | model

chain = prompt_template | model

st.title("Resume Builder")
st.markdown("""
<style>

/* 🌑 Dark App Background */
.stApp {
    background-color: #1F1F1F;
    color: #F1F1F1;
    font-family: 'Segoe UI', sans-serif;
}

/* 🌐 Main Title (st.title) */
h1 {
    color: #F1F1F1 !important;
    font-weight: 700 !important;
}

/* 🧭 Sidebar background and padding fix */
section[data-testid="stSidebar"] {
    background-color: #121212 !important;
    padding: 18px;
}

/* ✍️ Sidebar Label Styling */
section[data-testid="stSidebar"] label {
    color: #F1F1F1 !important;
    font-weight: 600 !important;
}

/* 🎛 Sidebar input fields */
section[data-testid="stSidebar"] input {
    background-color: #2B2B2B !important;
    color: #F1F1F1 !important;
    border: 1px solid #444 !important;
    border-radius: 6px !important;
    padding: 8px !important;
}

/* 🧾 All labels in the main area */
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    color: #F1F1F1 !important;
    font-weight: 600 !important;
}

/* ✏️ Input fields styling */
input, textarea {
    background-color: #2B2B2B !important;
    color: #F1F1F1 !important;
    border: 1px solid #444 !important;
    border-radius: 6px !important;
}

/* 📦 Selectbox styling */
div[data-baseweb="select"] > div {
    background-color: #2B2B2B !important;
    color: #F1F1F1 !important;
    border: 1px solid #444 !important;
}

/* 🧩 Expander Panel */
details {
    background-color: #2B2B2B;
    border: 1px solid #444;
    border-radius: 10px;
    padding: 10px;
}
details summary {
    font-size: 17px;
    font-weight: 600;
    color: #F1F1F1;
}

/* 🔘 Buttons */
.stButton>button, .stDownloadButton>button {
    background-color: #0A66C2;
    color: white;
    border-radius: 6px;
    font-weight: 600;
    border: none;
    padding: 10px 20px;
    box-shadow: 1px 2px 6px rgba(0,0,0,0.2);
    transition: 0.3s;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    background-color: #0955A2;
    transform: scale(1.03);
}

</style>
""", unsafe_allow_html=True)




name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("PhoneNo")
summary = st.text_area("Professional Summary")


with st.expander("AIsummary", expanded=True):
    job_title = st.text_input("JobTitle")
    if st.button("Summary using AI") and job_title:
        with st.spinner("Generating..."):
            aisummary = chain.invoke({"job": job_title})
            st.text_area("Summary", value=aisummary.content, height=200)

skills = st.text_area("Skills(coma-separated)")

#Experience
if 'experience' not in st.session_state:
    st.session_state.experience = []

if st.button('Add experience'):
    st.session_state.experience.append({"Job Role":"", "Company":"", "Time":""})

for i, exp in enumerate(st.session_state.experience):
    with st.expander(f"Experience {i + 1}", expanded=True):
        st.session_state.experience[i]["Job Role"] = st.text_input(f"Job Role", value=exp["Job Role"], key=f"Job Role_{i}")
        st.session_state.experience[i]["Company"] = st.text_input(f"Company", value=exp["Company"], key=f"Company_{i}")
        start_month = st.selectbox("Start Month", months, key=f"start_month_{i}")
        end_month = st.selectbox("End Month", months, key=f"end_month_{i}")
        year = st.selectbox("Year", Years, key=f"year_{i}")
        st.session_state.experience[i]["Time"] = f"{start_month} - {end_month} ({year})"
        if st.button(f"Delete Experience {i + 1}", key=f"delete_exp_{i}"):
            st.session_state.experience.pop()
            st.rerun()

#Projects
if 'projects' not in st.session_state:
    st.session_state.projects = []

if st.button('Add Project'):
    st.session_state.projects.append({"title":"", "summary":""})

for i, proj in enumerate(st.session_state.projects):
    with st.expander(f"Project {i + 1}", expanded=True):
        st.session_state.projects[i]["title"] = st.text_input(f"Project Title {i+1}", value=proj["title"], key=f"title_{i}")
        st.session_state.projects[i]["summary"] = st.text_area(f"Project Summary {i+1}", value=proj["summary"], key=f"summary_{i}")
        if st.button(f"Delete Project {i + 1}", key=f"delete_proj_{i}"):
            st.session_state.projects.pop()
            st.rerun()

#Education
if 'education' not in st.session_state:
    st.session_state.education = []

if st.button('Add education'):
    st.session_state.education.append({"Course":"", "College":"", "Graduation Year":""})

for i, edu in enumerate(st.session_state.education):
    with st.expander(f"Education {i + 1}", expanded=True):
        st.session_state.education[i]["Course"] = st.text_input(f"Course", value=edu["Course"], key=f"Course{i}")
        st.session_state.education[i]["College"] = st.text_input(f"College", value=edu["College"], key=f"College_{i}")
        st.session_state.education[i]["Graduation Year"] = f"Year of Graduation: {st.selectbox('Year', GradYears, key=f'grad_year_{i}')}"
        if st.button(f"Delete Education {i + 1}", key=f"delete_edu_{i}"):
            st.session_state.education.pop()
            st.rerun()

st.sidebar.title("Promptfolio")

chat_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
            You are a professional resume writing assistant. Answer the following question or give tips:
            {user_input}
            Give clear and helpful guidance. If the user asks anything **not related to resumes**, politely respond with:
            "I'm only trained to answer resume-related questions. I can't help with that."
            """
            )

another_chain = chat_prompt | model

user_input = st.sidebar.text_input("Ask me anything about resume")

if user_input:
    with st.sidebar:
        with st.spinner("Generating answer"):
            response = ""
            placeholder = st.empty()
            for chunk in model.stream(chat_prompt.format(user_input=user_input)):
                response += chunk.content
                placeholder.markdown(response)
if name:
    html_code = resume_template(name, email, phone, summary, skills, st.session_state.experience, st.session_state.education, st.session_state.projects)

    st.subheader("Resume Preview")
    components.html(html_code, height=800, scrolling=True)
    
    pdf_file = generate_pdf(html_code)
    st.download_button(
        label= "Download PDF",
        data= pdf_file,
        file_name= "resume.pdf",
        mime= "application/pdf"
    )

with st.expander("Check ATS Score"):
    if st.button("ATS score of this resume"):
        with st.spinner("Generating score..."):
            text_for_ats = resume_ats_template(name, email, phone, summary, skills, st.session_state.experience, st.session_state.education, st.session_state.projects)
            ats_score = ats_chain.invoke({'resume': text_for_ats})
            st.markdown(f"""
                        <div style='color:black ; font-size:16px; line-height:1.6;'>
                        <pre style='white-space:pre-wrap;'>{ats_score.content}</pre>
                        </div>
                        """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your resume for ATS score(PDF or DOCX)", type=['pdf','docx'], key='resume_upload')
    if uploaded_file and st.button("Evaluate Score by Uploading"):
        with st.spinner("Generating score"):
            resume_text =  extract_text_from_resume(uploaded_file)
            ats_score = ats_chain.invoke({'resume': resume_text})
            st.markdown(f"""
                    <div style='color:black ; font-size:16px; line-height:1.6;'>
                    <pre style='white-space:pre-wrap;'>{ats_score.content}</pre>
                    </div>
                    """, unsafe_allow_html=True)
        
