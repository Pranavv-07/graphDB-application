from database import driver


# ---------------------------------------------------------------------------
# Constraints
# ---------------------------------------------------------------------------

def create_constraints(session):
    """Create uniqueness constraints for all entity types."""
    constraints = [
        """
        CREATE CONSTRAINT student_name_unique IF NOT EXISTS
        FOR (s:Student)
        REQUIRE s.name IS UNIQUE
        """,
        """
        CREATE CONSTRAINT skill_name_unique IF NOT EXISTS
        FOR (s:Skill)
        REQUIRE s.name IS UNIQUE
        """,
        """
        CREATE CONSTRAINT project_name_unique IF NOT EXISTS
        FOR (p:Project)
        REQUIRE p.name IS UNIQUE
        """,
        """
        CREATE CONSTRAINT technology_name_unique IF NOT EXISTS
        FOR (t:Technology)
        REQUIRE t.name IS UNIQUE
        """,
        """
        CREATE CONSTRAINT job_title_unique IF NOT EXISTS
        FOR (j:Job)
        REQUIRE j.title IS UNIQUE
        """
    ]
    for query in constraints:
        session.run(query)


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

def create_students(session):
    students = [
        {"name": "Pranav",    "year": 3, "department": "CSE", "gpa": 8.9},
        {"name": "Rahul",     "year": 4, "department": "CSE", "gpa": 8.2},
        {"name": "Ananya",    "year": 3, "department": "CSE", "gpa": 9.1},
        {"name": "Arjun",     "year": 4, "department": "CSE", "gpa": 7.8},
        {"name": "Sneha",     "year": 3, "department": "CSE", "gpa": 8.5},
        {"name": "Kiran",     "year": 2, "department": "ECE", "gpa": 7.4},
        {"name": "Meera",     "year": 4, "department": "IT",  "gpa": 8.7},
        {"name": "Rohan",     "year": 3, "department": "CSE", "gpa": 8.0},
        {"name": "Divya",     "year": 2, "department": "IT",  "gpa": 7.9},
        {"name": "Aditya",    "year": 4, "department": "CSE", "gpa": 9.3},
        {"name": "Pooja",     "year": 3, "department": "ECE", "gpa": 8.1},
        {"name": "Siddharth", "year": 4, "department": "CSE", "gpa": 8.6},
        {"name": "Lakshmi",   "year": 2, "department": "IT",  "gpa": 7.5},
        {"name": "Vishal",    "year": 3, "department": "CSE", "gpa": 8.3},
        {"name": "Tanya",     "year": 4, "department": "CSE", "gpa": 9.0},
        {"name": "Nikhil",    "year": 2, "department": "ECE", "gpa": 7.2},
        {"name": "Priya",     "year": 3, "department": "IT",  "gpa": 8.8},
        {"name": "Aman",      "year": 4, "department": "CSE", "gpa": 8.4},
        {"name": "Shreya",    "year": 3, "department": "CSE", "gpa": 7.6},
        {"name": "Varun",     "year": 2, "department": "IT",  "gpa": 7.1},
    ]

    query = """
    UNWIND $students AS student
    MERGE (s:Student {name: student.name})
    SET
        s.year       = student.year,
        s.department = student.department,
        s.gpa        = student.gpa
    """
    session.run(query, students=students)


def create_skills(session):
    skills = [
        {"name": "Python",             "category": "Programming"},
        {"name": "Java",               "category": "Programming"},
        {"name": "JavaScript",         "category": "Programming"},
        {"name": "HTML/CSS",           "category": "Web"},           # FIX: was HTML/CSS/JavaScript — split into proper Skill
        {"name": "C++",                "category": "Programming"},
        {"name": "SQL",                "category": "Database"},
        {"name": "MongoDB",            "category": "Database"},
        {"name": "Machine Learning",   "category": "AI/ML"},
        {"name": "Deep Learning",      "category": "AI/ML"},
        {"name": "Data Analysis",      "category": "Data"},
        {"name": "React",              "category": "Frontend"},
        {"name": "Node.js",            "category": "Backend"},
        {"name": "Docker",             "category": "DevOps"},
        {"name": "Git",                "category": "DevOps"},
        {"name": "REST APIs",          "category": "Backend"},
        {"name": "Cloud (AWS/GCP)",    "category": "Cloud"},
    ]

    query = """
    UNWIND $skills AS skill
    MERGE (s:Skill {name: skill.name})
    SET s.category = skill.category
    """
    session.run(query, skills=skills)


def create_projects(session):
    projects = [
        {
            "name": "AI PDF Explainer",
            "description": "AI-powered application that explains educational PDF documents using Gemini.",
            "status": "Completed"
        },
        {
            "name": "Attendance Scanner",
            "description": "Web-based QR attendance scanning system for college classrooms.",
            "status": "Completed"
        },
        {
            "name": "Hospital Management System",
            "description": "Desktop application for managing hospital records, staff, and appointments.",
            "status": "Completed"
        },
        {
            "name": "Carbon Footprint Calculator",
            "description": "Application for estimating and tracking personal carbon emissions.",
            "status": "In Progress"
        },
        {
            "name": "Stock Market Predictor",
            "description": "LSTM-based deep learning model to predict stock price movements.",
            "status": "Completed"
        },
        {
            "name": "E-Commerce Platform",
            "description": "Full-stack online shopping application with React frontend and Node.js backend.",
            "status": "In Progress"
        },
        {
            "name": "Sentiment Analyser",
            "description": "NLP model to classify tweet sentiment for brand monitoring.",
            "status": "Completed"
        },
        {
            "name": "DevOps Pipeline Toolkit",
            "description": "Automated CI/CD pipeline with Docker containers and cloud deployment.",
            "status": "In Progress"
        },
        {
            "name": "Expense Tracker App",
            "description": "Mobile-first web app for personal expense tracking with analytics.",
            "status": "Completed"
        },
        {
            "name": "Smart Irrigation System",
            "description": "IoT sensor-based irrigation controller using embedded C++.",
            "status": "Completed"
        },
        {
            "name": "SkillGraph Explorer",
            "description": "Graph database application to explore student-skill-job relationships using CognoDB.",
            "status": "Completed"
        },
        {
            "name": "Real-Time Chat App",
            "description": "WebSocket-based real-time messaging application built with Node.js.",
            "status": "In Progress"
        },
    ]

    query = """
    UNWIND $projects AS project
    MERGE (p:Project {name: project.name})
    SET
        p.description = project.description,
        p.status      = project.status
    """
    session.run(query, projects=projects)


def create_technologies(session):
    technologies = [
        {"name": "Python",              "category": "Programming Language"},
        {"name": "Streamlit",           "category": "Framework"},
        {"name": "Gemini",              "category": "AI Platform"},
        {"name": "MoviePy",             "category": "Python Library"},
        {"name": "MySQL",               "category": "Database"},
        {"name": "Java Swing",          "category": "GUI Framework"},
        {"name": "HTML/CSS/JavaScript", "category": "Web"},  # Technology node kept as-is for projects
        {"name": "MongoDB",             "category": "Database"},
        {"name": "React",               "category": "Frontend Framework"},
        {"name": "Node.js",             "category": "Backend Runtime"},
        {"name": "Docker",              "category": "DevOps"},
        {"name": "TensorFlow",          "category": "ML Framework"},
        {"name": "PyTorch",             "category": "ML Framework"},
        {"name": "AWS",                 "category": "Cloud Platform"},
        {"name": "Flask",               "category": "Backend Framework"},
        {"name": "PostgreSQL",          "category": "Database"},
    ]

    query = """
    UNWIND $technologies AS technology
    MERGE (t:Technology {name: technology.name})
    SET t.category = technology.category
    """
    session.run(query, technologies=technologies)


def create_jobs(session):
    jobs = [
        {
            "title": "AI Developer Intern",
            "company": "Wexa AI",
            "location": "Remote",
            "salary_range": "₹25,000–40,000/month"
        },
        {
            "title": "Backend Developer Intern",
            "company": "TechLabs",
            "location": "Hyderabad",
            "salary_range": "₹20,000–35,000/month"
        },
        {
            "title": "Data Analyst Intern",
            "company": "DataWorks",
            "location": "Remote",
            "salary_range": "₹18,000–30,000/month"
        },
        {
            "title": "Frontend Developer Intern",
            "company": "WebTech",
            "location": "Bangalore",
            "salary_range": "₹20,000–32,000/month"
        },
        {
            "title": "Full Stack Developer Intern",
            "company": "StartupHub",
            "location": "Pune",
            "salary_range": "₹22,000–38,000/month"
        },
        {
            "title": "DevOps Intern",
            "company": "CloudBase",
            "location": "Remote",
            "salary_range": "₹20,000–33,000/month"
        },
        {
            "title": "Machine Learning Engineer Intern",
            "company": "IntelliCore",
            "location": "Bangalore",
            "salary_range": "₹30,000–50,000/month"
        },
        {
            "title": "Database Administrator Intern",
            "company": "DataVault",
            "location": "Chennai",
            "salary_range": "₹18,000–28,000/month"
        },
    ]

    query = """
    UNWIND $jobs AS job
    MERGE (j:Job {title: job.title})
    SET
        j.company      = job.company,
        j.location     = job.location,
        j.salary_range = job.salary_range
    """
    session.run(query, jobs=jobs)


# ---------------------------------------------------------------------------
# Relationships
# ---------------------------------------------------------------------------

def create_student_skill_relationships(session):
    """
    HAS_SKILL relationships now carry two properties:
      - proficiency   : "Beginner" | "Intermediate" | "Advanced" | "Expert"
      - years_experience : integer (approximate years of practice)
    """
    relationships = [
        # (student, skill, proficiency, years_experience)
        ("Pranav",    "Python",           "Advanced",     2),
        ("Pranav",    "SQL",              "Intermediate", 1),
        ("Pranav",    "Java",             "Intermediate", 1),
        ("Pranav",    "Machine Learning", "Advanced",     2),
        ("Pranav",    "Git",              "Intermediate", 2),

        ("Rahul",     "Python",           "Advanced",     3),
        ("Rahul",     "JavaScript",       "Advanced",     2),
        ("Rahul",     "React",            "Intermediate", 2),
        ("Rahul",     "SQL",              "Intermediate", 2),
        ("Rahul",     "Node.js",          "Beginner",     1),

        ("Ananya",    "Python",           "Expert",       3),
        ("Ananya",    "Machine Learning", "Expert",       3),
        ("Ananya",    "Deep Learning",    "Advanced",     2),
        ("Ananya",    "Data Analysis",    "Advanced",     2),
        ("Ananya",    "SQL",              "Intermediate", 2),

        ("Arjun",     "Java",             "Advanced",     3),
        ("Arjun",     "SQL",              "Advanced",     3),
        ("Arjun",     "MongoDB",          "Intermediate", 2),
        ("Arjun",     "C++",             "Intermediate", 2),

        ("Sneha",     "JavaScript",       "Advanced",     2),
        ("Sneha",     "React",            "Advanced",     2),
        ("Sneha",     "HTML/CSS",         "Expert",       3),  # FIX: uses the corrected Skill name
        ("Sneha",     "Python",           "Intermediate", 1),

        ("Kiran",     "C++",             "Advanced",     3),
        ("Kiran",     "Python",           "Intermediate", 1),
        ("Kiran",     "SQL",              "Beginner",     1),

        ("Meera",     "Python",           "Advanced",     3),
        ("Meera",     "Data Analysis",    "Advanced",     3),
        ("Meera",     "SQL",              "Advanced",     3),
        ("Meera",     "Machine Learning", "Intermediate", 2),

        ("Rohan",     "JavaScript",       "Intermediate", 2),
        ("Rohan",     "React",            "Intermediate", 1),
        ("Rohan",     "Node.js",          "Intermediate", 2),
        ("Rohan",     "MongoDB",          "Beginner",     1),

        ("Divya",     "HTML/CSS",         "Advanced",     2),  # FIX: corrected Skill name
        ("Divya",     "JavaScript",       "Intermediate", 1),
        ("Divya",     "React",            "Beginner",     1),

        ("Aditya",    "Python",           "Expert",       4),
        ("Aditya",    "Machine Learning", "Expert",       3),
        ("Aditya",    "Deep Learning",    "Expert",       3),
        ("Aditya",    "Docker",           "Advanced",     2),
        ("Aditya",    "Cloud (AWS/GCP)",  "Intermediate", 2),
        ("Aditya",    "Git",              "Advanced",     3),

        ("Pooja",     "Python",           "Intermediate", 2),
        ("Pooja",     "SQL",              "Intermediate", 2),
        ("Pooja",     "Data Analysis",    "Intermediate", 1),

        ("Siddharth", "Java",             "Expert",       4),
        ("Siddharth", "SQL",              "Expert",       4),
        ("Siddharth", "REST APIs",        "Advanced",     3),
        ("Siddharth", "Docker",           "Intermediate", 2),

        ("Lakshmi",   "Python",           "Beginner",     1),
        ("Lakshmi",   "HTML/CSS",         "Intermediate", 1),  # FIX: corrected Skill name
        ("Lakshmi",   "JavaScript",       "Beginner",     1),

        ("Vishal",    "Python",           "Advanced",     3),
        ("Vishal",    "Machine Learning", "Advanced",     2),
        ("Vishal",    "Data Analysis",    "Advanced",     2),
        ("Vishal",    "SQL",              "Intermediate", 2),
        ("Vishal",    "Git",              "Intermediate", 2),

        ("Tanya",     "Python",           "Expert",       4),
        ("Tanya",     "Machine Learning", "Expert",       4),
        ("Tanya",     "Deep Learning",    "Expert",       3),
        ("Tanya",     "Data Analysis",    "Advanced",     3),
        ("Tanya",     "SQL",              "Advanced",     3),
        ("Tanya",     "Cloud (AWS/GCP)",  "Intermediate", 2),

        ("Nikhil",    "C++",             "Advanced",     2),
        ("Nikhil",    "Python",           "Beginner",     1),

        ("Priya",     "JavaScript",       "Advanced",     3),
        ("Priya",     "React",            "Advanced",     2),
        ("Priya",     "Node.js",          "Advanced",     2),
        ("Priya",     "HTML/CSS",         "Advanced",     3),  # FIX: corrected Skill name
        ("Priya",     "MongoDB",          "Intermediate", 2),

        ("Aman",      "Python",           "Advanced",     3),
        ("Aman",      "Docker",           "Advanced",     2),
        ("Aman",      "Cloud (AWS/GCP)",  "Advanced",     2),
        ("Aman",      "Git",              "Advanced",     3),
        ("Aman",      "REST APIs",        "Advanced",     2),

        ("Shreya",    "Python",           "Intermediate", 2),
        ("Shreya",    "SQL",              "Intermediate", 1),
        ("Shreya",    "Data Analysis",    "Beginner",     1),

        ("Varun",     "JavaScript",       "Beginner",     1),
        ("Varun",     "HTML/CSS",         "Intermediate", 1),  # FIX: corrected Skill name
    ]

    query = """
    UNWIND $relationships AS rel
    MATCH (student:Student {name: rel.student})
    MATCH (skill:Skill    {name: rel.skill})
    MERGE (student)-[r:HAS_SKILL]->(skill)
    SET
        r.proficiency       = rel.proficiency,
        r.years_experience  = rel.years_experience
    """

    data = [
        {
            "student":          student,
            "skill":            skill,
            "proficiency":      proficiency,
            "years_experience": years_experience,
        }
        for student, skill, proficiency, years_experience in relationships
    ]

    session.run(query, relationships=data)


def create_project_relationships(session):
    relationships = [
        ("Pranav",    "AI PDF Explainer"),
        ("Pranav",    "Attendance Scanner"),
        ("Pranav",    "SkillGraph Explorer"),
        ("Rahul",     "Attendance Scanner"),
        ("Rahul",     "E-Commerce Platform"),
        ("Rahul",     "Real-Time Chat App"),
        ("Ananya",    "Carbon Footprint Calculator"),
        ("Ananya",    "Sentiment Analyser"),
        ("Ananya",    "Stock Market Predictor"),
        ("Arjun",     "Hospital Management System"),
        ("Sneha",     "Carbon Footprint Calculator"),
        ("Sneha",     "E-Commerce Platform"),
        ("Kiran",     "Smart Irrigation System"),
        ("Meera",     "Sentiment Analyser"),
        ("Meera",     "Expense Tracker App"),
        ("Rohan",     "Real-Time Chat App"),
        ("Rohan",     "Expense Tracker App"),
        ("Divya",     "E-Commerce Platform"),
        ("Aditya",    "Stock Market Predictor"),
        ("Aditya",    "DevOps Pipeline Toolkit"),
        ("Pooja",     "Expense Tracker App"),
        ("Siddharth", "Hospital Management System"),
        ("Siddharth", "Real-Time Chat App"),
        ("Vishal",    "Sentiment Analyser"),
        ("Tanya",     "Stock Market Predictor"),
        ("Tanya",     "SkillGraph Explorer"),
        ("Priya",     "E-Commerce Platform"),
        ("Priya",     "Real-Time Chat App"),
        ("Aman",      "DevOps Pipeline Toolkit"),
        ("Aman",      "SkillGraph Explorer"),
    ]

    query = """
    UNWIND $relationships AS rel
    MATCH (student:Student {name: rel.student})
    MATCH (project:Project {name: rel.project})
    MERGE (student)-[:WORKED_ON]->(project)
    """

    data = [
        {"student": student, "project": project}
        for student, project in relationships
    ]

    session.run(query, relationships=data)


def create_project_technology_relationships(session):
    relationships = [
        ("AI PDF Explainer",        "Python"),
        ("AI PDF Explainer",        "Streamlit"),
        ("AI PDF Explainer",        "Gemini"),
        ("AI PDF Explainer",        "MoviePy"),

        ("Attendance Scanner",      "HTML/CSS/JavaScript"),
        ("Attendance Scanner",      "MongoDB"),
        ("Attendance Scanner",      "Flask"),

        ("Hospital Management System", "Java Swing"),
        ("Hospital Management System", "MySQL"),

        ("Carbon Footprint Calculator", "Python"),
        ("Carbon Footprint Calculator", "Streamlit"),
        ("Carbon Footprint Calculator", "MongoDB"),

        ("Stock Market Predictor",  "Python"),
        ("Stock Market Predictor",  "TensorFlow"),
        ("Stock Market Predictor",  "PyTorch"),

        ("E-Commerce Platform",     "React"),
        ("E-Commerce Platform",     "Node.js"),
        ("E-Commerce Platform",     "MongoDB"),
        ("E-Commerce Platform",     "HTML/CSS/JavaScript"),

        ("Sentiment Analyser",      "Python"),
        ("Sentiment Analyser",      "TensorFlow"),
        ("Sentiment Analyser",      "PostgreSQL"),

        ("DevOps Pipeline Toolkit", "Docker"),
        ("DevOps Pipeline Toolkit", "AWS"),
        ("DevOps Pipeline Toolkit", "Python"),

        ("Expense Tracker App",     "React"),
        ("Expense Tracker App",     "Node.js"),
        ("Expense Tracker App",     "PostgreSQL"),

        ("Smart Irrigation System", "Python"),
        ("Smart Irrigation System", "MySQL"),

        ("SkillGraph Explorer",     "Python"),
        ("SkillGraph Explorer",     "Streamlit"),

        ("Real-Time Chat App",      "Node.js"),
        ("Real-Time Chat App",      "MongoDB"),
        ("Real-Time Chat App",      "HTML/CSS/JavaScript"),
    ]

    query = """
    UNWIND $relationships AS rel
    MATCH (project:Project    {name: rel.project})
    MATCH (technology:Technology {name: rel.technology})
    MERGE (project)-[:USES]->(technology)
    """

    data = [
        {"project": project, "technology": technology}
        for project, technology in relationships
    ]

    session.run(query, relationships=data)


def create_job_skill_requirements(session):
    """
    Job REQUIRES Skill relationships.
    NOTE: All skill names here must exactly match Skill node names created
    in create_skills(). HTML/CSS is a Skill; HTML/CSS/JavaScript is a Technology.
    """
    relationships = [
        # AI Developer Intern
        ("AI Developer Intern",              "Python"),
        ("AI Developer Intern",              "Machine Learning"),
        ("AI Developer Intern",              "SQL"),

        # Backend Developer Intern
        ("Backend Developer Intern",         "Python"),
        ("Backend Developer Intern",         "SQL"),
        ("Backend Developer Intern",         "MongoDB"),
        ("Backend Developer Intern",         "REST APIs"),

        # Data Analyst Intern
        ("Data Analyst Intern",              "Python"),
        ("Data Analyst Intern",              "SQL"),
        ("Data Analyst Intern",              "Data Analysis"),

        # Frontend Developer Intern
        ("Frontend Developer Intern",        "JavaScript"),
        ("Frontend Developer Intern",        "React"),
        ("Frontend Developer Intern",        "HTML/CSS"),     # FIX: was "HTML/CSS/JavaScript" (Technology), now correctly the Skill

        # Full Stack Developer Intern
        ("Full Stack Developer Intern",      "JavaScript"),
        ("Full Stack Developer Intern",      "React"),
        ("Full Stack Developer Intern",      "Node.js"),
        ("Full Stack Developer Intern",      "MongoDB"),
        ("Full Stack Developer Intern",      "REST APIs"),

        # DevOps Intern
        ("DevOps Intern",                    "Docker"),
        ("DevOps Intern",                    "Cloud (AWS/GCP)"),
        ("DevOps Intern",                    "Git"),
        ("DevOps Intern",                    "Python"),

        # Machine Learning Engineer Intern
        ("Machine Learning Engineer Intern", "Python"),
        ("Machine Learning Engineer Intern", "Machine Learning"),
        ("Machine Learning Engineer Intern", "Deep Learning"),
        ("Machine Learning Engineer Intern", "Data Analysis"),

        # Database Administrator Intern
        ("Database Administrator Intern",    "SQL"),
        ("Database Administrator Intern",    "MongoDB"),
        ("Database Administrator Intern",    "Python"),
    ]

    query = """
    UNWIND $relationships AS rel
    MATCH (job:Job   {title: rel.job})
    MATCH (skill:Skill {name: rel.skill})
    MERGE (job)-[:REQUIRES]->(skill)
    """

    data = [
        {"job": job, "skill": skill}
        for job, skill in relationships
    ]

    session.run(query, relationships=data)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def seed_database():
    with driver.session() as session:
        print("Creating constraints...")
        create_constraints(session)

        print("Creating students (20)...")
        create_students(session)

        print("Creating skills (16)...")
        create_skills(session)

        print("Creating projects (12)...")
        create_projects(session)

        print("Creating technologies (16)...")
        create_technologies(session)

        print("Creating jobs (8)...")
        create_jobs(session)

        print("Creating student→skill relationships (with proficiency & years_experience)...")
        create_student_skill_relationships(session)

        print("Creating student→project relationships...")
        create_project_relationships(session)

        print("Creating project→technology relationships...")
        create_project_technology_relationships(session)

        print("Creating job→skill (REQUIRES) relationships...")
        create_job_skill_requirements(session)


if __name__ == "__main__":
    try:
        seed_database()
        print()
        print("=" * 50)
        print("       SkillGraph Seed Complete ✅")
        print("=" * 50)
        print()
        print("Nodes created:")
        print("  • 20 Students")
        print("  • 16 Skills")
        print("  • 12 Projects")
        print("  • 16 Technologies")
        print("  •  8 Jobs")
        print()
        print("Relationships created with rich properties:")
        print("  • HAS_SKILL  (proficiency, years_experience)")
        print("  • WORKED_ON")
        print("  • USES")
        print("  • REQUIRES")

    except Exception as error:
        print()
        print("=" * 50)
        print("        SkillGraph Seed Failed ❌")
        print("=" * 50)
        print()
        print(f"Error: {error}")