import streamlit as st

# Core logic imports - Left untouched as requested
from queries import (
    find_students_by_skill,
    find_project_technologies,
    find_projects_using_technology,
    find_jobs_for_student,
    rank_students_for_job,
    get_all_skills,
    get_all_projects,
    get_all_jobs,
    get_all_students,
    get_student_graph
)
# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="SkillGraph Explorer",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ---------------------------------------------------------
# LOAD DATA FROM COGNODB
# ---------------------------------------------------------

try:
    skills = get_all_skills()
    projects = get_all_projects()
    jobs = get_all_jobs()
    students = get_all_students()

except Exception as error:
    st.error("SkillGraph could not load data from CognoDB.")
    st.write("Please check the Terminal for the full error.")
    st.stop()

# ---------------------------------------------------------
# CUSTOM CSS (Theme-Aware)
# ---------------------------------------------------------
# We use Streamlit's native CSS variables to ensure perfect 
# rendering in both Light and Dark modes.
st.markdown(
    """
    <style>
    /* Typography & Spacing */
    .hero-container {
        padding: 1rem 0 2.5rem 0;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
        color: var(--text-color);
        line-height: 1.2;
    }
    .main-title span {
        color: var(--primary-color);
    }
    .subtitle {
        font-size: 1.15rem;
        color: rgba(128, 128, 128, 0.9);
        font-weight: 400;
        margin: 0;
    }
    .section-title {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: var(--text-color);
    }
    .section-desc {
        font-size: 1rem;
        color: rgba(128, 128, 128, 0.8);
        margin-bottom: 2rem;
    }

    /* Modern Card Layouts */
    .sg-card {
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        margin-bottom: 1rem;
        background-color: var(--secondary-background-color);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .sg-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
        border-color: var(--primary-color);
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 0.25rem;
    }
    .card-subtitle {
        font-size: 0.95rem;
        color: rgba(128, 128, 128, 0.8);
        font-weight: 500;
    }
    
    /* Metrics & Badges */
    .match-score-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .match-score-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--primary-color);
        line-height: 1;
        text-align: right;
    }
    .match-score-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: rgba(128, 128, 128, 0.7);
        font-weight: 600;
        margin-top: 4px;
        text-align: right;
    }
    .badge {
        display: inline-block;
        padding: 0.35em 0.8em;
        font-size: 0.85em;
        font-weight: 600;
        border-radius: 20px;
        background-color: rgba(128, 128, 128, 0.1);
        color: var(--text-color);
        border: 1px solid rgba(128, 128, 128, 0.3);
        margin: 0.2em 0.2em 0 0;
        transition: all 0.2s ease;
    }
    .badge-primary {
        background-color: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }

    /* Streamlit overrides for cleaner look */
    div[data-testid="stTabs"] button {
        font-size: 1.1rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <div class="main-title">Skill<span>Graph</span></div>
        <div class="subtitle">Explore connections between students, skills, projects, and careers.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.title("Navigation")
    st.markdown(
        """
        Welcome to **SkillGraph**. Use the interactive modules to query the knowledge base.
        
        <br>
        
        **🔎 Student Explorer**  
        Discover students possessing specific technical skills.

        **🛠 Project Explorer**  
        Break down real-world projects into their core technologies.

        **💼 Job Matching**  
        Intelligently rank students against job requirements.
        """,
        unsafe_allow_html=True
    )
    st.divider()
    st.caption("v2.0 • Enhanced UI Edition")

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3 , tab4= st.tabs([
    "🔎 Student Explorer",
    "🛠 Project Explorer",
    "💼 Job Matching",
    "🧑‍🎓 Student Graph"
])


# =========================================================
# TAB 1 — STUDENT EXPLORER
# =========================================================
with tab1:
    st.markdown('<div class="section-title">Find Students by Skill</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Select a skill to find students who have cultivated that expertise.</div>', unsafe_allow_html=True)

    selected_skill = st.selectbox(
    "Select a skill",
    skills
)

    search_clicked = st.button(
    "Search Students",
    key="find_students_button",
    type="primary"
)

    if search_clicked:
        with st.spinner(f"Searching Graph for '{selected_skill}' experts..."):
            try:
                students = find_students_by_skill(selected_skill)
                st.write("") # Spacer

                if not students:
                    st.info(f"No students found with the skill '{selected_skill}'. Try another one.", icon="ℹ️")
                else:
                    st.success(f"Discovered {len(students)} matching student(s).", icon="✅")
                    
                    # Responsive grid layout using Streamlit columns
                    cols = st.columns(3)
                    for index, student in enumerate(students):
                        with cols[index % 3]:
                            st.markdown(
                                f"""
                                <div class="sg-card">
                                    <div class="card-title">👤 {student['name']}</div>
                                    <div class="card-subtitle">
                                        🎓 Year {student['year']}<br>
                                        🏛️ {student['department']}
                                    </div>
                                    <div style="margin-top: 10px;">
                                        <span class="badge badge-primary">{selected_skill}</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
            except Exception as error:
                st.error("Unable to query SkillGraph.", icon="🚨")
                st.caption(f"Error details: {error}")


# =========================================================
# TAB 2 — PROJECT EXPLORER
# =========================================================
with tab2:
    st.markdown('<div class="section-title">Explore Projects</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Analyze the technology stack behind active projects.</div>', unsafe_allow_html=True)

    selected_project = st.selectbox(
    "Select a project",
    projects
)

    explore_clicked = st.button(
    "Analyze Stack",
    key="explore_project_button",
    type="primary"
)

    if explore_clicked:
        with st.spinner("Analyzing project architecture..."):
            try:
                technologies = find_project_technologies(selected_project)
                st.write("") # Spacer
                
                if not technologies:
                    st.info("No technologies are mapped to this project yet.", icon="ℹ️")
                else:
                    st.subheader(f"Architecture for {selected_project}")
                    st.write("Core Technologies:")
                    
                    cols = st.columns(4)
                    for index, technology in enumerate(technologies):
                        with cols[index % 4]:
                            st.markdown(
                                f"""
                                <div class="sg-card" style="text-align: center; padding: 1.5rem 1rem;">
                                    <div class="card-title" style="font-size: 1.1rem;">{technology['name']}</div>
                                    <div class="badge" style="margin-top: 8px;">{technology['category']}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
            except Exception as error:
                st.error("Unable to query project information.")
                st.caption(f"Error details: {error}")


# =========================================================
# TAB 3 — JOB MATCHING
# =========================================================
with tab3:
    st.markdown('<div class="section-title">Intelligent Job Matching</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Algorithmically rank candidates based on shared skills with job requirements.</div>', unsafe_allow_html=True)

    selected_job = st.selectbox(
    "Select a job",
    jobs
)

    match_clicked = st.button(
    "Run Matchmaker Engine",
    key="job_match_button",
    type="primary"
)

    if match_clicked:
        with st.spinner("Calculating multi-dimensional graph matches..."):
            try:
                results = rank_students_for_job(selected_job)
                st.write("") # Spacer

                if not results:
                    st.info("No viable candidates were found for this position.", icon="ℹ️")
                else:
                    st.success(f"Matched {len(results)} potential candidate(s).", icon="✅")
                    
                    # Displaying results dynamically with rich UI
                    for index, student in enumerate(results, start=1):
                        matched = student["matched"]
                        total = student["total_required"]
                        percentage = (matched / total) * 100 if total > 0 else 0
                        
                        # Generate styled HTML badges for matched skills
                        badges_html = "".join([f'<span class="badge">{skill}</span>' for skill in student["matching_skills"]])
                        
                        # Use a single, dedented string for the markdown to prevent 
                        # Streamlit from misinterpreting indented divs as code blocks
                        import textwrap
                        card_html = textwrap.dedent(f"""
                            <div class="sg-card" style="margin-bottom: 0.5rem;">
                                <div class="match-score-container">
                                    <div>
                                        <div class="card-title"><span style="color: var(--primary-color);">#{index}</span> &nbsp;{student['student']}</div>
                                        <div class="card-subtitle" style="margin-bottom: 12px;">
                                            🎓 Year {student['year']} &nbsp;•&nbsp; 🏛️ {student['department']}
                                        </div>
                                        <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                                            {badges_html}
                                        </div>
                                    </div>
                                    <div>
                                        <div class="match-score-value">{matched}<span style="font-size: 1.2rem; color: rgba(128,128,128,0.5);">/{total}</span></div>
                                        <div class="match-score-label">Reqs Met</div>
                                    </div>
                                </div>
                            </div>
                        """)
                        
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Add a visual progress bar linked to the score
                        st.progress(percentage / 100)
                        st.write("") # Small spacer before next student

            except Exception as error:
                st.error("Unable to calculate job matches.", icon="🚨")
                st.caption(f"Error details: {error}")

# =========================================================
# TAB 4 — GRAPH EXPLORER
# =========================================================

with tab4:

    st.markdown(
        '<div class="section-title">Explore Student Graph</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore the connected skills, projects, technologies "
        "and jobs associated with a student."
    )

    selected_student = st.selectbox(
        "Select a student",
        students,
        key="graph_student"
    )

    explore_graph_clicked = st.button(
        "Explore Graph",
        key="graph_explorer_button",
        type="primary"
    )

    if explore_graph_clicked:

        with st.spinner("Traversing SkillGraph..."):

            try:

                graph_data = get_student_graph(
                    selected_student
                )

                if not graph_data:

                    st.info(
                        "No graph data was found for this student."
                    )

                else:

                    st.success(
                        f"Graph loaded for {selected_student}."
                    )

                    # -----------------------------------------
                    # STUDENT
                    # -----------------------------------------

                    st.subheader(
                        f"👤 {graph_data['student']}"
                    )

                    # -----------------------------------------
                    # SKILLS
                    # -----------------------------------------

                    st.markdown("### 🧠 Skills")

                    skills_data = [
                        skill
                        for skill in graph_data["skills"]
                        if skill["name"] is not None
                    ]

                    if skills_data:

                        columns = st.columns(3)

                        for index, skill in enumerate(
                            skills_data
                        ):

                            with columns[index % 3]:

                                st.markdown(
                                    f"""
                                    <div class="card">

                                    <div class="card-title">
                                    {skill['name']}
                                    </div>

                                    <div class="card-subtitle">
                                    {skill['category']}
                                    </div>

                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                    else:

                        st.info(
                            "No skills connected to this student."
                        )

                    # -----------------------------------------
                    # PROJECTS
                    # -----------------------------------------

                    st.markdown("### 🛠 Projects")

                    projects_data = [
                        project
                        for project in graph_data["projects"]
                        if project["name"] is not None
                    ]

                    if projects_data:

                        for project in projects_data:

                            st.markdown(
                                f"""
                                <div class="card">

                                <div class="card-title">
                                {project['name']}
                                </div>

                                <div class="card-subtitle">
                                {project['description']}
                                </div>

                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    else:

                        st.info(
                            "No projects connected to this student."
                        )

                    # -----------------------------------------
                    # TECHNOLOGIES
                    # -----------------------------------------

                    st.markdown("### ⚙️ Technologies")

                    technologies_data = [
                        technology
                        for technology
                        in graph_data["technologies"]
                        if technology["name"] is not None
                    ]

                    if technologies_data:

                        columns = st.columns(3)

                        for index, technology in enumerate(
                            technologies_data
                        ):

                            with columns[index % 3]:

                                st.markdown(
                                    f"""
                                    <div class="card">

                                    <div class="card-title">
                                    {technology['name']}
                                    </div>

                                    <div class="card-subtitle">
                                    {technology['category']}
                                    </div>

                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                    else:

                        st.info(
                            "No technologies connected through projects."
                        )

                    # -----------------------------------------
                    # MATCHING JOBS
                    # -----------------------------------------

                    st.markdown("### 💼 Related Jobs")

                    matching_jobs = [
                        job
                        for job in graph_data["matching_jobs"]
                        if job is not None
                    ]

                    if matching_jobs:

                        for job in matching_jobs:

                            st.markdown(
                                f"""
                                <div class="card">

                                <div class="card-title">
                                {job}
                                </div>

                                <div class="card-subtitle">
                                This job requires skills connected
                                to {selected_student}.
                                </div>

                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    else:

                        st.info(
                            "No related jobs found."
                        )

            except Exception as error:

                st.error(
                    "Unable to explore the student graph."
                )

                st.caption(
                    f"Error details: {error}"
                )
# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: rgba(128, 128, 128, 0.7); font-size: 0.9rem;">
        <strong>SkillGraph</strong> • Designed with Streamlit & Knowledge Graphs
    </div>
    """, 
    unsafe_allow_html=True
)
