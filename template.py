import pdfplumber
from docx import Document

def resume_template(name, email, phone, summary, skills, experience, education, projects):
    skills_list = ''.join(f"<li>{skills.strip()}</li>" for skills in skills.split(','))

    project_html = ""
    for project in projects:
        project_html += f"""
            <div style="margin-bottom: 20px;">
                <p><b>{project['title']}</b></p>
                <p>{project['summary']}</p>
            </div>
        """

    experience_html = ""
    for experience in experience:
        experience_html += f"""
            <div style="margin-bottom: 20px;", "font-family= Arial, sans-serif;">
                <p><b>{experience['Job Role']}</b></p>
                <p>{experience['Company']}</p>
                <p><b>{experience['Time']}</b></p>
            </div>

        """

    education_html = ""
    for education in education:
        education_html += f"""
            <div style="margin-bottom: 20px;", "font-family= Arial, sans-serif;">
                <p><b>{education['Course']}</b></p>
                <p>{education['College']}</p>
                <p><b>{education['Graduation Year']}</b></p>
            </div>

        """

    html = f"""
    <html>
    <head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            max-width: 800px;
            margin: auto;
            background: #f9f9f9;
        }}
        h1,p{{
            margin: 0
        }}
        h2 {{
            border-bottom: 2px solid #000;
        }}
        ul {{
            padding-left: 20px;
        }}
    </style>
    </head>
    <body>
        <h1>{name}</h1>
        <p><b>Email:</b> {email} | <b>Phone:</b> {phone}</p>

        <h2>Professional Summary</h2>
        <p>{summary}</p>

        <h2>Skills</h2>
        <ul>
            {skills_list}
        </ul>

        <h2>Experience</h2>
        {experience_html}

        <h2>Projects</h2>
        {project_html}
        
        <h2>Education</h2>
        {education_html}

    </body>
    </html>
    """
    return html

def resume_ats_template(name, email, phone, summary, skills, experience, education, projects):
    skills_list = ', '.join([s.strip() for s in skills.split(',')])

    project_text = ""
    for project in projects:
        project_text += f"- {project['title']}: {project['summary']}\n"

    experience_text = ""
    for exp in experience:
        experience_text += f"- {exp['Job Role']} at {exp['Company']} ({exp['Time']})\n"

    education_text = ""
    for edu in education:
        education_text += f"- {edu['Course']} at {edu['College']} ({edu['Graduation Year']})\n"

    text = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}

            Professional Summary:
            {summary}

            Skills:
            {skills_list}

            Experience:
            {experience_text}

            Projects:
            {project_text}

            Education:
            {education_text}
            """
    return text.strip()

def extract_text_from_resume(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(para.text for para in doc.paragraphs)
    else:
        return ""