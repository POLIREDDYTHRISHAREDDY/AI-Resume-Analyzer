
import re


SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "MongoDB",
    "MySQL",
    "Git",
    "GitHub",
    "Django",
    "Flask",
    "FastAPI",
    "REST API",
    "Pandas",
    "NumPy",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "TensorFlow",
    "PyTorch",
    "Power BI",
    "Excel",
    "Data Analysis",
    "Streamlit"
]


def find_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILLS:

        skill_lower = skill.lower()

        if re.search(
            r'\b' + re.escape(skill_lower) + r'\b',
            text
        ):

            found_skills.append(skill)

    return found_skills