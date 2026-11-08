
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def generate_feedback(
    resume_text,
    job_role,
    matching_skills,
    missing_skills
):

    api_key = os.getenv("GROQ_API_KEY")


    if not api_key:

        return (
            "AI feedback is not configured.\n\n"
            "Please add your Groq API key to the .env file."
        )


    try:

        client = Groq(
            api_key=api_key
        )


        prompt = f"""
You are a professional resume reviewer.

Analyze the following resume for the selected job role.

Job Role:
{job_role}

Matching Skills:
{matching_skills}

Missing Skills:
{missing_skills}

Resume:
{resume_text}


Give simple and useful feedback for a college student.

Include these sections:

1. Overall Assessment
2. Resume Strengths
3. Areas to Improve
4. Three Specific Suggestions

Keep the response concise, clear and professional.
Do not invent skills or experience that are not present in the resume.
"""


        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )


        return response.choices[0].message.content


    except Exception as e:

        return (
            "Unable to generate AI feedback.\n\n"
            f"Error: {str(e)}"
        )
