import streamlit as st
import streamlit.components.v1 as components
from weasyprint import HTML
from template import resume_template
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

chain = prompt_template | model

st.title("Resume Builder")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("PhoneNo")
summary = st.text_area("Professional Summary")



with st.expander("AIsummary", expanded=True):
    job_title = st.text_input("JobTitle")
    if st.button("Summary using AI") and job_title:
        with st.spinner("Generating..."):
            summary = chain.invoke({"job": job_title})
            st.text_area("Summary", value=summary.content, height=200)

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
        st.session_state.experience[i]["Time"] = f"{st.selectbox('Start Month',months)} - {st.selectbox('End Month', months)}, {st.selectbox('Year', Years)}"

#Projects
if 'projects' not in st.session_state:
    st.session_state.projects = []

if st.button('Add Project'):
    st.session_state.projects.append({"title":"", "summary":""})

for i, proj in enumerate(st.session_state.projects):
    with st.expander(f"Project {i + 1}", expanded=True):
        st.session_state.projects[i]["title"] = st.text_input(f"Project Title {i+1}", value=proj["title"], key=f"title_{i}")
        st.session_state.projects[i]["summary"] = st.text_area(f"Project Summary {i+1}", value=proj["summary"], key=f"summary_{i}")

#Education
if 'education' not in st.session_state:
    st.session_state.education = []

if st.button('Add education'):
    st.session_state.education.append({"Course":"", "College":"", "Graduation Year":""})

for i, edu in enumerate(st.session_state.education):
    with st.expander(f"Education {i + 1}", expanded=True):
        st.session_state.education[i]["Course"] = st.text_input(f"Course", value=edu["Course"], key=f"Course{i}")
        st.session_state.education[i]["College"] = st.text_input(f"College", value=edu["College"], key=f"College_{i}")
        st.session_state.education[i]["Graduation Year"] = f"Year of Graduation: {st.selectbox('Year', GradYears)}"

st.sidebar.title("ChatWithAI")
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