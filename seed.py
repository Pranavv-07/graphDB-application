from database import driver


def create_constraints(session):
    """
    Create uniqueness constraints for important entities.
    """

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


def create_students(session):
    students = [
        {
            "name": "Pranav",
            "year": 3,
            "department": "CSE"
        },
        {
            "name": "Rahul",
            "year": 4,
            "department": "CSE"
        },
        {
            "name": "Ananya",
            "year": 3,
            "department": "CSE"
        },
        {
            "name": "Arjun",
            "year": 4,
            "department": "CSE"
        },
        {
            "name": "Sneha",
            "year": 3,
            "department": "CSE"
        }
    ]

    query = """
    UNWIND $students AS student

    MERGE (s:Student {name: student.name})
    SET
        s.year = student.year,
        s.department = student.department
    """

    session.run(query, students=students)


def create_skills(session):
    skills = [
        {"name": "Python", "category": "Programming"},
        {"name": "Java", "category": "Programming"},
        {"name": "JavaScript", "category": "Programming"},
        {"name": "SQL", "category": "Database"},
        {"name": "Machine Learning", "category": "AI"},
        {"name": "React", "category": "Frontend"},
        {"name": "Data Analysis", "category": "Data"},
        {"name": "MongoDB", "category": "Database"}
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
            "description": "AI-powered application that explains educational PDF documents."
        },
        {
            "name": "Attendance Scanner",
            "description": "Web-based QR attendance scanning system."
        },
        {
            "name": "Hospital Management System",
            "description": "Application for managing hospital records and operations."
        },
        {
            "name": "Carbon Footprint Calculator",
            "description": "Application for estimating personal carbon emissions."
        }
    ]

    query = """
    UNWIND $projects AS project

    MERGE (p:Project {name: project.name})
    SET p.description = project.description
    """

    session.run(query, projects=projects)


def create_technologies(session):
    technologies = [
        {"name": "Python", "category": "Programming Language"},
        {"name": "Streamlit", "category": "Framework"},
        {"name": "Gemini", "category": "AI Platform"},
        {"name": "MoviePy", "category": "Python Library"},
        {"name": "MySQL", "category": "Database"},
        {"name": "Java Swing", "category": "GUI Framework"},
        {"name": "HTML/CSS/JavaScript", "category": "Web"},
        {"name": "MongoDB", "category": "Database"},
        {"name": "React", "category": "Frontend Framework"}
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
            "location": "Remote"
        },
        {
            "title": "Backend Developer Intern",
            "company": "TechLabs",
            "location": "Hyderabad"
        },
        {
            "title": "Data Analyst Intern",
            "company": "DataWorks",
            "location": "Remote"
        },
        {
            "title": "Frontend Developer Intern",
            "company": "WebTech",
            "location": "Bangalore"
        }
    ]

    query = """
    UNWIND $jobs AS job

    MERGE (j:Job {title: job.title})
    SET
        j.company = job.company,
        j.location = job.location
    """

    session.run(query, jobs=jobs)


def create_student_skill_relationships(session):
    relationships = [
        ("Pranav", "Python"),
        ("Pranav", "SQL"),
        ("Pranav", "Java"),
        ("Pranav", "Machine Learning"),

        ("Rahul", "Python"),
        ("Rahul", "JavaScript"),
        ("Rahul", "React"),
        ("Rahul", "SQL"),

        ("Ananya", "Python"),
        ("Ananya", "Machine Learning"),
        ("Ananya", "Data Analysis"),
        ("Ananya", "SQL"),

        ("Arjun", "Java"),
        ("Arjun", "SQL"),
        ("Arjun", "MongoDB"),

        ("Sneha", "JavaScript"),
        ("Sneha", "React"),
        ("Sneha", "Python")
    ]

    query = """
    UNWIND $relationships AS relationship

    MATCH (student:Student {name: relationship.student})
    MATCH (skill:Skill {name: relationship.skill})

    MERGE (student)-[:HAS_SKILL]->(skill)
    """

    data = [
        {
            "student": student,
            "skill": skill
        }
        for student, skill in relationships
    ]

    session.run(query, relationships=data)


def create_project_relationships(session):
    relationships = [
        ("Pranav", "AI PDF Explainer"),
        ("Pranav", "Attendance Scanner"),
        ("Rahul", "Attendance Scanner"),
        ("Ananya", "Carbon Footprint Calculator"),
        ("Arjun", "Hospital Management System"),
        ("Sneha", "Carbon Footprint Calculator")
    ]

    query = """
    UNWIND $relationships AS relationship

    MATCH (student:Student {name: relationship.student})
    MATCH (project:Project {name: relationship.project})

    MERGE (student)-[:WORKED_ON]->(project)
    """

    data = [
        {
            "student": student,
            "project": project
        }
        for student, project in relationships
    ]

    session.run(query, relationships=data)


def create_project_technology_relationships(session):
    relationships = [
        ("AI PDF Explainer", "Python"),
        ("AI PDF Explainer", "Streamlit"),
        ("AI PDF Explainer", "Gemini"),
        ("AI PDF Explainer", "MoviePy"),

        ("Attendance Scanner", "HTML/CSS/JavaScript"),
        ("Attendance Scanner", "MongoDB"),

        ("Hospital Management System", "Java Swing"),
        ("Hospital Management System", "MySQL"),

        ("Carbon Footprint Calculator", "Python"),
        ("Carbon Footprint Calculator", "Streamlit"),
        ("Carbon Footprint Calculator", "MongoDB")
    ]

    query = """
    UNWIND $relationships AS relationship

    MATCH (project:Project {name: relationship.project})
    MATCH (technology:Technology {name: relationship.technology})

    MERGE (project)-[:USES]->(technology)
    """

    data = [
        {
            "project": project,
            "technology": technology
        }
        for project, technology in relationships
    ]

    session.run(query, relationships=data)


def create_job_skill_relationships(session):
    relationships = [
        ("AI Developer Intern", "Python"),
        ("AI Developer Intern", "SQL"),
        ("AI Developer Intern", "Machine Learning"),

        ("Backend Developer Intern", "Python"),
        ("Backend Developer Intern", "SQL"),
        ("Backend Developer Intern", "MongoDB"),

        ("Data Analyst Intern", "Python"),
        ("Data Analyst Intern", "SQL"),
        ("Data Analyst Intern", "Data Analysis"),

        ("Frontend Developer Intern", "JavaScript"),
        ("Frontend Developer Intern", "React"),
        ("Frontend Developer Intern", "HTML/CSS/JavaScript")
    ]

    query = """
    UNWIND $relationships AS relationship

    MATCH (job:Job {title: relationship.job})
    MATCH (skill:Skill {name: relationship.skill})

    MERGE (job)-[:REQUIRES]->(skill)
    """

    data = [
        {
            "job": job,
            "skill": skill
        }
        for job, skill in relationships
    ]

    session.run(query, relationships=data)


def seed_database():
    with driver.session() as session:
        print("Creating constraints...")
        create_constraints(session)

        print("Creating students...")
        create_students(session)

        print("Creating skills...")
        create_skills(session)

        print("Creating projects...")
        create_projects(session)

        print("Creating technologies...")
        create_technologies(session)

        print("Creating jobs...")
        create_jobs(session)

        print("Creating student-skill relationships...")
        create_student_skill_relationships(session)

        print("Creating student-project relationships...")
        create_project_relationships(session)

        print("Creating project-technology relationships...")
        create_project_technology_relationships(session)

        print("Creating job-skill relationships...")
        create_job_skill_relationships(session)


if __name__ == "__main__":
    try:
        seed_database()

        print()
        print("========================================")
        print("      SkillGraph Seed Complete")
        print("========================================")
        print()
        print("All nodes and relationships were created successfully.")

    except Exception as error:
        print()
        print("========================================")
        print("       SkillGraph Seed Failed")
        print("========================================")
        print()
        print(error)