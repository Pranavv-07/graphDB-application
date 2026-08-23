import textwrap
import traceback

import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION — first Streamlit call in the module
# ---------------------------------------------------------
st.set_page_config(
    page_title="SkillGraph Explorer",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core logic imports
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
# HELPERS
# ---------------------------------------------------------

def load_data():
    """Load all top-level lists from CognoDB. Returns (data_dict, error)."""
    try:
        return ({
            "skills":   get_all_skills()   or [],
            "projects": get_all_projects() or [],
            "jobs":     get_all_jobs()     or [],
            "students": get_all_students() or [],
        }, None)
    except Exception as e:
        return (None, e)


def render_error(message: str, exc: Exception = None):
    st.error(message)
    if exc is not None:
        with st.expander("Error details"):
            tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
            st.code("".join(tb_lines), language="text")


def safe_selectbox(label: str, options, key=None, help=None):
    """Selectbox wrapper — shows an info message when options list is empty."""
    if not options:
        st.info(f"No options available for: {label}")
        return None
    return st.selectbox(label, options, key=key, help=help)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
data, load_error = load_data()
if load_error is not None:
    render_error("SkillGraph could not connect to CognoDB.", load_error)
    st.stop()

all_skills   = data.get("skills",   [])
all_projects = data.get("projects", [])
all_jobs     = data.get("jobs",     [])
all_students = data.get("students", [])

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hero */
    .hero-container {
        padding: 1.5rem 0 2.5rem 0;
        border-bottom: 1px solid rgba(128, 128, 128, 0.15);
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.4rem;
        color: var(--text-color);
        line-height: 1.1;
    }
    .main-title span {
        color: var(--primary-color);
    }
    .subtitle {
        font-size: 1.05rem;
        color: rgba(128, 128, 128, 0.85);
        font-weight: 400;
        margin: 0;
    }

    /* Section headings */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: var(--text-color);
    }
    .section-desc {
        font-size: 0.95rem;
        color: rgba(128, 128, 128, 0.8);
        margin-bottom: 1.75rem;
    }

    /* Cards */
    .sg-card {
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.18);
        margin-bottom: 1rem;
        background-color: var(--secondary-background-color);
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .sg-card:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
        border-color: var(--primary-color);
    }
    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 0.2rem;
    }
    .card-subtitle {
        font-size: 0.9rem;
        color: rgba(128, 128, 128, 0.8);
        font-weight: 400;
        line-height: 1.5;
    }

    /* Match score layout */
    .match-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
    }
    .match-score-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary-color);
        line-height: 1;
        white-space: nowrap;
    }
    .match-score-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: rgba(128, 128, 128, 0.65);
        font-weight: 600;
        margin-top: 4px;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.28em 0.75em;
        font-size: 0.8em;
        font-weight: 600;
        border-radius: 999px;
        background-color: rgba(128, 128, 128, 0.1);
        color: var(--text-color);
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin: 0.2em 0.2em 0 0;
        letter-spacing: 0.01em;
    }
    .badge-primary {
        background-color: var(--primary-color);
        color: #fff;
        border-color: var(--primary-color);
    }

    /* Tab labels */
    div[data-testid="stTabs"] button {
        font-size: 0.95rem;
        font-weight: 600;
    }

    /* Sidebar */
    .sidebar-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: rgba(128,128,128,0.65);
        margin-bottom: 0.3rem;
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
        <div class="main-title">🔗 Skill<span>Graph</span></div>
        <div class="subtitle">Explore connections between students, skills, projects, and careers.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### SkillGraph")
    st.markdown(
        """
        A graph database application that maps students,
        skills, projects, technologies, and job opportunities
        as an interconnected knowledge graph.

        ---

        **Student Explorer**
        Find students by skill and see their proficiency level.

        **Project Explorer**
        Explore the technology stack behind each project.

        **Job Matching**
        Rank candidates against job skill requirements.

        **Student Graph**
        Traverse a student's full connected graph.
        """,
    )
    st.divider()
    st.caption("SkillGraph · CognoDB · Neo4j Driver")
    st.divider()
    st.caption("Made by Pranav Vedula")

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Student Explorer",
    "Project Explorer",
    "Job Matching",
    "Student Graph",
])


# =========================================================
# TAB 1 — STUDENT EXPLORER
# =========================================================
with tab1:
    st.markdown('<div class="section-title">Find Students by Skill</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Select a skill to see which students have it and how proficient they are.</div>',
        unsafe_allow_html=True
    )

    selected_skill = safe_selectbox("Select a skill", all_skills)

    if selected_skill is not None:
        if st.button("Search", key="find_students_button", type="primary"):
            with st.spinner("Querying graph..."):
                try:
                    found_students = find_students_by_skill(selected_skill)

                    if not found_students:
                        st.info(f"No students found with the skill '{selected_skill}'.")
                    else:
                        st.success(f"{len(found_students)} student(s) found.")
                        cols = st.columns(3)
                        for i, student in enumerate(found_students):
                            prof = student.get("proficiency") or ""
                            prof_colour = {
                                "Expert":       "#16a34a",
                                "Advanced":     "#2563eb",
                                "Intermediate": "#d97706",
                                "Beginner":     "#64748b",
                            }.get(prof, "var(--primary-color)")
                            yrs = student.get("years_experience")
                            yrs_label = (
                                f"{yrs} yr{'s' if yrs != 1 else ''} exp."
                                if yrs else ""
                            )
                            with cols[i % 3]:
                                st.markdown(
                                    f"""
                                    <div class="sg-card">
                                        <div class="card-title">{student['name']}</div>
                                        <div class="card-subtitle">
                                            Year {student['year']} &nbsp;&middot;&nbsp; {student['department']}
                                        </div>
                                        <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px; align-items: center;">
                                            <span class="badge badge-primary">{selected_skill}</span>
                                            <span class="badge" style="background:{prof_colour}; color:#fff; border-color:{prof_colour};">{prof}</span>
                                            {f'<span class="badge">{yrs_label}</span>' if yrs_label else ""}
                                            
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                except Exception as error:
                    render_error("Unable to query SkillGraph.", error)


# =========================================================
# TAB 2 — PROJECT EXPLORER
# =========================================================
with tab2:
    st.markdown('<div class="section-title">Explore Projects</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Select a project to see the technology stack it uses.</div>',
        unsafe_allow_html=True
    )

    selected_project = safe_selectbox("Select a project", all_projects)

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
                st.error("Unable to query project information.", icon="🚨")
                st.caption(f"Error details: {error}")


# =========================================================
# TAB 3 — JOB MATCHING
# =========================================================
with tab3:
    st.markdown('<div class="section-title">Job Matching</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Select a job to rank candidates by how many required skills they possess.</div>',
        unsafe_allow_html=True
    )

    selected_job = safe_selectbox("Select a job", all_jobs)

    if selected_job is not None:
        if st.button("Match Candidates", key="job_match_button", type="primary"):
            with st.spinner("Running graph traversal..."):
                try:
                    results = rank_students_for_job(selected_job)

                    if not results:
                        st.info("No candidates matched the required skills for this position.")
                    else:
                        st.success(f"{len(results)} candidate(s) found.")

                        for rank, student in enumerate(results, start=1):
                            matched = student["matched"]
                            total   = student["total_required"]
                            score   = max(0.0, min(1.0, matched / total if total > 0 else 0.0))
                            badges  = "".join(
                                f'<span class="badge">{s}</span>'
                                for s in student["matching_skills"]
                            )
                            card_html = textwrap.dedent(f"""
                                <div class="sg-card">
                                    <div class="match-row">
                                        <div style="flex: 1;">
                                            <div class="card-title">
                                                <span style="color: var(--primary-color);">#{rank}</span>
                                                &nbsp;{student['student']}
                                            </div>
                                            <div class="card-subtitle" style="margin-bottom: 10px;">
                                                Year {student['year']} &middot; {student['department']}
                                            </div>
                                            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                                                {badges}
                                            </div>
                                        </div>
                                        <div style="text-align: right; flex-shrink: 0;">
                                            <div class="match-score-value">
                                                {matched}<span style="font-size: 1rem; opacity: 0.45;">/{total}</span>
                                            </div>
                                            <div class="match-score-label">skills matched</div>
                                        </div>
                                    </div>
                                </div>
                            """)
                            st.markdown(card_html, unsafe_allow_html=True)
                            st.progress(score)

                except Exception as error:
                    render_error("Unable to calculate job matches.", error)


# =========================================================
# TAB 4 — STUDENT GRAPH
# =========================================================
with tab4:
    st.markdown('<div class="section-title">Student Graph</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Select a student to traverse their full connected graph — skills, projects, technologies, and related jobs.</div>',
        unsafe_allow_html=True
    )

    selected_student = safe_selectbox("Select a student", all_students, key="graph_student")

    if selected_student is not None:
        if st.button("Explore Graph", key="graph_explorer_button", type="primary"):
            with st.spinner("Traversing graph..."):
                try:
                    graph_data = get_student_graph(selected_student)

                    if not graph_data:
                        st.info("No graph data found for this student.")
                    else:
                        st.success(f"Graph loaded for {selected_student}.")
                        st.subheader(graph_data["student"])

                        # --- Skills ---
                        st.markdown("#### Skills")
                        skills_data = [s for s in graph_data["skills"] if s["name"]]
                        if skills_data:
                            cols = st.columns(3)
                            for i, skill in enumerate(skills_data):
                                with cols[i % 3]:
                                    st.markdown(
                                        f"""
                                        <div class="sg-card">
                                            <div class="card-title">{skill['name']}</div>
                                            <div class="card-subtitle">{skill['category']}</div>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                        else:
                            st.info("No skills connected to this student.")

                        # --- Projects ---
                        st.markdown("#### Projects")
                        projects_data = [p for p in graph_data["projects"] if p["name"]]
                        if projects_data:
                            for project in projects_data:
                                st.markdown(
                                    f"""
                                    <div class="sg-card">
                                        <div class="card-title">{project['name']}</div>
                                        <div class="card-subtitle">{project['description']}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                        else:
                            st.info("No projects connected to this student.")

                        # --- Technologies ---
                        st.markdown("#### Technologies")
                        tech_data = [t for t in graph_data["technologies"] if t["name"]]
                        if tech_data:
                            cols = st.columns(3)
                            for i, tech in enumerate(tech_data):
                                with cols[i % 3]:
                                    st.markdown(
                                        f"""
                                        <div class="sg-card">
                                            <div class="card-title">{tech['name']}</div>
                                            <div class="card-subtitle">{tech['category']}</div>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                        else:
                            st.info("No technologies connected through projects.")

                        # --- Related Jobs ---
                        st.markdown("#### Related Jobs")
                        matching_jobs = [j for j in graph_data["matching_jobs"] if j]
                        if matching_jobs:
                            for job in matching_jobs:
                                st.markdown(
                                    f"""
                                    <div class="sg-card">
                                        <div class="card-title">{job}</div>
                                        <div class="card-subtitle">
                                            This role requires skills that {selected_student} has.
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                        else:
                            st.info("No related jobs found.")

                except Exception as error:
                    render_error("Unable to load the student graph.", error)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: rgba(128,128,128,0.6); font-size: 0.85rem; padding: 0.5rem 0;">
        SkillGraph &nbsp;&middot;&nbsp; Built with Streamlit &amp; CognoDB
    </div>
    """,
    unsafe_allow_html=True
)
