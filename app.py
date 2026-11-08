import streamlit as st
import pdfplumber

from analyzer import find_skills
from job_roles import JOB_ROLES
from ai_feedback import generate_feedback


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="ResumeIQ - AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
}

header {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* HERO */

.hero {
    background: linear-gradient(
        135deg,
        #111827 0%,
        #312e81 55%,
        #4f46e5 100%
    );

    padding: 45px 50px;
    border-radius: 24px;
    color: white;
    margin-bottom: 30px;

    box-shadow: 0 15px 40px rgba(49, 46, 129, 0.20);
}

.hero-badge {
    display: inline-block;

    background: rgba(255,255,255,0.12);

    padding: 8px 15px;

    border-radius: 30px;

    font-size: 13px;

    border: 1px solid rgba(255,255,255,0.18);

    margin-bottom: 16px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -1px;
}

.hero-text {
    font-size: 18px;
    color: #e5e7eb;
    max-width: 720px;
    line-height: 1.6;
    margin-top: 12px;
}


/* CARDS */

.card {
    background: white;

    padding: 25px;

    border-radius: 18px;

    border: 1px solid #e5e7eb;

    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);

    margin-bottom: 20px;
}


/* SECTION */

.section-title {
    font-size: 24px;
    font-weight: 750;
    color: #111827;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 20px;
}


/* SCORE */

.score-card {
    background: linear-gradient(
        135deg,
        #eef2ff,
        #f5f3ff
    );

    border: 1px solid #c7d2fe;

    padding: 28px;

    border-radius: 20px;

    text-align: center;

    margin-bottom: 20px;
}

.score-label {
    color: #6366f1;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.score-number {
    font-size: 58px;
    font-weight: 800;
    color: #312e81;
    margin: 5px 0;
}

.score-role {
    color: #4b5563;
    font-size: 14px;
}


/* SKILL BADGES */

.skill-badge {
    display: inline-block;

    background: #eef2ff;

    color: #3730a3;

    padding: 7px 12px;

    border-radius: 20px;

    margin: 4px;

    font-size: 13px;

    font-weight: 600;

    border: 1px solid #c7d2fe;
}

.missing-badge {
    display: inline-block;

    background: #fef2f2;

    color: #b91c1c;

    padding: 7px 12px;

    border-radius: 20px;

    margin: 4px;

    font-size: 13px;

    font-weight: 600;

    border: 1px solid #fecaca;
}


/* AI */

.ai-card {
    background: linear-gradient(
        135deg,
        #faf5ff,
        #eef2ff
    );

    border: 1px solid #ddd6fe;

    padding: 28px;

    border-radius: 20px;

    margin-bottom: 15px;
}

.ai-title {
    font-size: 22px;
    font-weight: 750;
    color: #4c1d95;
    margin-bottom: 8px;
}

.ai-description {
    color: #6b7280;
    font-size: 14px;
}


/* TIPS */

.tip-card {
    background: white;

    border: 1px solid #e5e7eb;

    padding: 22px;

    border-radius: 16px;

    height: 150px;

    box-shadow: 0 5px 15px rgba(15,23,42,0.04);
}

.tip-title {
    font-size: 17px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 8px;
}

.tip-text {
    font-size: 14px;
    color: #6b7280;
    line-height: 1.5;
}


/* EMPTY STATE */

.empty-card {
    background: white;

    border: 1px solid #e5e7eb;

    padding: 50px;

    border-radius: 20px;

    text-align: center;

    margin-top: 20px;
}

.empty-icon {
    font-size: 55px;
}

.empty-title {
    font-size: 25px;
    font-weight: 700;
    color: #111827;
}

.empty-text {
    color: #6b7280;
    font-size: 15px;
}


/* FOOTER */

.footer {
    text-align: center;

    color: #9ca3af;

    font-size: 13px;

    margin-top: 50px;

    padding-top: 25px;

    border-top: 1px solid #e5e7eb;
}


/* BUTTON */

.stButton > button {

    width: 100%;

    border-radius: 10px;

    border: none;

    padding: 12px 20px;

    font-weight: 650;

    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );

    color: white;

    transition: all 0.2s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(79,70,229,0.25);
}


/* FILE UPLOADER */

[data-testid="stFileUploader"] {

    background: white;

    border-radius: 14px;

    padding: 10px;

    border: 1px solid #e5e7eb;
}


/* SELECT BOX */

div[data-baseweb="select"] > div {

    border-radius: 10px;
}


/* METRICS */

[data-testid="stMetric"] {

    background: white;

    padding: 18px;

    border-radius: 15px;

    border: 1px solid #e5e7eb;

    box-shadow: 0 4px 12px rgba(15,23,42,0.04);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.html("""
<div class="hero">

    <div class="hero-badge">
        ✨ AI-Powered Resume Analysis
    </div>

    <div class="hero-title">
        ResumeIQ
    </div>

    <div class="hero-text">
        Analyze your resume, discover missing skills,
        measure job compatibility, and get personalized
        AI feedback in seconds.
    </div>

</div>
""")


# =========================================================
# INPUT SECTION
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.html("""
    <div class="card">

        <div class="section-title">
            🎯 Target Job Role
        </div>

        <div class="section-subtitle">
            Choose the role you are preparing for.
        </div>

    </div>
    """)

    job_role = st.selectbox(
        "Select Job Role",
        list(JOB_ROLES.keys()),
        label_visibility="collapsed"
    )


with col2:

    st.html("""
    <div class="card">

        <div class="section-title">
            📄 Upload Resume
        </div>

        <div class="section-subtitle">
            Upload your resume in PDF format.
        </div>

    </div>
    """)

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )


# =========================================================
# WHEN RESUME IS UPLOADED
# =========================================================

if uploaded_file is not None:

    st.success("✓ Resume uploaded successfully")


    # =====================================================
    # EXTRACT TEXT
    # =====================================================

    text = ""

    try:

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

    except Exception as e:

        st.error(f"Unable to read the PDF: {e}")

        st.stop()


    if not text.strip():

        st.error(
            "No readable text was found in this PDF. "
            "Please upload a text-based resume."
        )

        st.stop()


    # =====================================================
    # FIND SKILLS
    # =====================================================

    skills = find_skills(text)

    required_skills = JOB_ROLES[job_role]


    # =====================================================
    # MATCH SKILLS
    # =====================================================

    skill_names_lower = [
        skill.lower()
        for skill in skills
    ]

    matching_skills = []

    missing_skills = []


    for skill in required_skills:

        if skill.lower() in skill_names_lower:

            matching_skills.append(skill)

        else:

            missing_skills.append(skill)


    # =====================================================
    # SCORE
    # =====================================================

    if len(required_skills) > 0:

        score = int(
            (len(matching_skills) /
             len(required_skills)) * 100
        )

    else:

        score = 0


    # =====================================================
    # ANALYSIS HEADER
    # =====================================================

    st.html("""
    <div style="margin-top:35px;">

        <div class="section-title">
            📊 Resume Analysis
        </div>

        <div class="section-subtitle">
            Here's how your resume matches the selected role.
        </div>

    </div>
    """)


    # =====================================================
    # SCORE + METRICS
    # =====================================================

    score_col, metric1, metric2 = st.columns(
        [1.2, 1, 1]
    )


    with score_col:

        st.html(f"""
        <div class="score-card">

            <div class="score-label">
                Job Match Score
            </div>

            <div class="score-number">
                {score}%
            </div>

            <div class="score-role">
                {job_role}
            </div>

        </div>
        """)


    with metric1:

        st.metric(
            "Skills Detected",
            len(skills)
        )


    with metric2:

        st.metric(
            "Skills Missing",
            len(missing_skills)
        )


    st.progress(score / 100)


    # =====================================================
    # MATCHING + MISSING
    # =====================================================

    st.html("""
    <div style="margin-top:25px;"></div>
    """)


    skill_col1, skill_col2 = st.columns(2)


    # -----------------------------------------------------
    # MATCHING SKILLS
    # -----------------------------------------------------

    with skill_col1:

        st.html("""
        <div class="card">

            <div class="section-title">
                ✅ Matching Skills
            </div>

            <div class="section-subtitle">
                Skills found in your resume.
            </div>

        </div>
        """)

        if matching_skills:

            badges = ""

            for skill in matching_skills:

                badges += f"""
                <span class="skill-badge">
                    ✓ {skill}
                </span>
                """

            st.html(badges)

        else:

            st.warning(
                "No matching skills found."
            )


    # -----------------------------------------------------
    # MISSING SKILLS
    # -----------------------------------------------------

    with skill_col2:

        st.html("""
        <div class="card">

            <div class="section-title">
                ⚠️ Missing Skills
            </div>

            <div class="section-subtitle">
                Skills required for this role but not detected.
            </div>

        </div>
        """)

        if missing_skills:

            badges = ""

            for skill in missing_skills:

                badges += f"""
                <span class="missing-badge">
                    ✕ {skill}
                </span>
                """

            st.html(badges)

        else:

            st.success(
                "Excellent! All required skills are present."
            )


    # =====================================================
    # RESUME STRENGTH
    # =====================================================

    st.html("""
    <div class="card">

        <div class="section-title">
            💪 Resume Strength
        </div>

    </div>
    """)


    if score >= 80:

        st.success(
            "Excellent match! Your resume is strongly aligned "
            "with this job role."
        )

    elif score >= 60:

        st.info(
            "Good match! Your resume has a solid foundation "
            "for this role."
        )

    elif score >= 40:

        st.warning(
            "Moderate match. Adding more relevant skills "
            "could improve your score."
        )

    else:

        st.error(
            "Low match. Consider building more skills "
            "related to this role."
        )


    # =====================================================
    # AI FEEDBACK
    # =====================================================

    st.html("""
    <div class="ai-card">

        <div class="ai-title">
            🤖 AI Resume Feedback
        </div>

        <div class="ai-description">
            Get personalized feedback about your resume
            using AI.
        </div>

    </div>
    """)


    if st.button(
        "✨ Generate AI Feedback",
        key="ai_feedback_button"
    ):

        with st.spinner(
            "AI is reviewing your resume..."
        ):

            feedback = generate_feedback(
                text,
                job_role,
                matching_skills,
                missing_skills
            )


        st.html("""
        <div class="card">

            <div class="section-title">
                🤖 AI Review
            </div>

        </div>
        """)

        st.write(feedback)


    # =====================================================
    # QUICK TIPS
    # =====================================================

    st.html("""
    <div style="margin-top:35px;">

        <div class="section-title">
            💡 Quick Improvement Tips
        </div>

        <div class="section-subtitle">
            Simple changes that can strengthen your resume.
        </div>

    </div>
    """)


    tip1, tip2, tip3 = st.columns(3)


    with tip1:

        st.html("""
        <div class="tip-card">

            <div class="tip-title">
                🎯 Relevant Skills
            </div>

            <div class="tip-text">
                Add skills that are directly related
                to your target job.
            </div>

        </div>
        """)


    with tip2:

        st.html("""
        <div class="tip-card">

            <div class="tip-title">
                📈 Quantify Results
            </div>

            <div class="tip-text">
                Mention numbers, percentages,
                improvements, or measurable results.
            </div>

        </div>
        """)


    with tip3:

        st.html("""
        <div class="tip-card">

            <div class="tip-title">
                💻 Showcase Projects
            </div>

            <div class="tip-text">
                Include strong projects with
                technologies and GitHub links.
            </div>

        </div>
        """)


    # =====================================================
    # ALL DETECTED SKILLS
    # =====================================================

    st.html("""
    <div style="margin-top:35px;"></div>
    """)


    with st.expander("🧠 View All Detected Skills"):

        if skills:

            badges = ""

            for skill in skills:

                badges += f"""
                <span class="skill-badge">
                    {skill}
                </span>
                """

            st.html(badges)

        else:

            st.warning(
                "No technical skills detected."
            )


    # =====================================================
    # EXTRACTED RESUME TEXT
    # =====================================================

    with st.expander("📄 View Extracted Resume Text"):

        st.text_area(
            "Resume Content",
            text,
            height=400
        )


# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.html("""
    <div class="empty-card">

        <div class="empty-icon">
            📄
        </div>

        <div class="empty-title">
            Ready to analyze your resume?
        </div>

        <div class="empty-text">
            Select your target job role and upload
            your PDF resume to get started.
        </div>

    </div>
    """)


# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="footer">

    <b>ResumeIQ</b> · AI Resume Analyzer

    <br><br>

    Built with Python · Streamlit · NLP · Groq AI

</div>
""")