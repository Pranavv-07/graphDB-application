from database import driver


def find_students_by_skill(skill_name):
    """
    Find all students who have a particular skill.
    Returns name, year, department plus proficiency and years_experience
    from the HAS_SKILL relationship.
    """

    query = """
    MATCH (student:Student)-[r:HAS_SKILL]->(skill:Skill)
    WHERE skill.name = $skill_name

    RETURN
        student.name        AS name,
        student.year        AS year,
        student.department  AS department,
        r.proficiency       AS proficiency,
        r.years_experience  AS years_experience

    ORDER BY
        CASE r.proficiency
            WHEN 'Expert'       THEN 1
            WHEN 'Advanced'     THEN 2
            WHEN 'Intermediate' THEN 3
            WHEN 'Beginner'     THEN 4
            ELSE 5
        END,
        student.name
    """

    with driver.session() as session:
        result = session.run(
            query,
            skill_name=skill_name
        )

        return [record.data() for record in result]


def find_project_technologies(project_name):
    """
    Find all technologies used by a project.
    """

    query = """
    MATCH (project:Project)-[:USES]->(technology:Technology)
    WHERE project.name = $project_name

    RETURN
        technology.name AS name,
        technology.category AS category

    ORDER BY technology.name
    """

    with driver.session() as session:
        result = session.run(
            query,
            project_name=project_name
        )

        return [record.data() for record in result]


def find_projects_using_technology(technology_name):
    """
    Find all projects that use a particular technology.
    """

    query = """
    MATCH (project:Project)-[:USES]->(technology:Technology)
    WHERE technology.name = $technology_name

    RETURN
        project.name AS name,
        project.description AS description

    ORDER BY project.name
    """

    with driver.session() as session:
        result = session.run(
            query,
            technology_name=technology_name
        )

        return [record.data() for record in result]


def find_jobs_for_student(student_name):
    """
    Find jobs that require skills possessed by a student.

    Graph traversal:

    Student
       ↓ HAS_SKILL
    Skill
       ↑ REQUIRES
    Job
    """

    query = """
    MATCH (student:Student)-[:HAS_SKILL]->(skill:Skill)
          <-[:REQUIRES]-(job:Job)

    WHERE student.name = $student_name

    RETURN
        job.title AS title,
        job.company AS company,
        job.location AS location,
        collect(DISTINCT skill.name) AS matching_skills

    ORDER BY size(matching_skills) DESC, job.title
    """

    with driver.session() as session:
        result = session.run(
            query,
            student_name=student_name
        )

        return [record.data() for record in result]


def rank_students_for_job(job_title):
    """
    Rank students according to how many skills
    they share with the selected job.
    Only returns students with at least 1 matching skill.
    """

    query = """
    MATCH (job:Job)-[:REQUIRES]->(required_skill:Skill)

    WHERE job.title = $job_title

    WITH
        job,
        collect(DISTINCT required_skill.name) AS required_skills

    MATCH (student:Student)

    OPTIONAL MATCH (student)-[:HAS_SKILL]->(student_skill:Skill)

    WITH
        job,
        required_skills,
        student,
        collect(DISTINCT student_skill.name) AS student_skills

    WITH
        student,
        required_skills,
        [
            skill IN required_skills
            WHERE skill IN student_skills
        ] AS matching_skills

    WHERE size(matching_skills) > 0

    RETURN
        student.name       AS student,
        student.year       AS year,
        student.department AS department,
        size(required_skills)  AS total_required,
        size(matching_skills)  AS matched,
        matching_skills

    ORDER BY matched DESC, student.name
    """

    with driver.session() as session:
        result = session.run(
            query,
            job_title=job_title
        )

        return [record.data() for record in result]


def get_all_skills():
    """
    Return all skills available in SkillGraph.
    """

    query = """
    MATCH (skill:Skill)
    RETURN skill.name AS name
    ORDER BY skill.name
    """

    with driver.session() as session:
        result = session.run(query)

        return [
            record["name"]
            for record in result
        ]


def get_all_projects():
    """
    Return all projects available in SkillGraph.
    """

    query = """
    MATCH (project:Project)
    RETURN project.name AS name
    ORDER BY project.name
    """

    with driver.session() as session:
        result = session.run(query)

        return [
            record["name"]
            for record in result
        ]


def get_all_technologies():
    """
    Return all technologies available in SkillGraph.
    """

    query = """
    MATCH (technology:Technology)
    RETURN technology.name AS name
    ORDER BY technology.name
    """

    with driver.session() as session:
        result = session.run(query)

        return [
            record["name"]
            for record in result
        ]


def get_all_jobs():
    """
    Return all jobs available in SkillGraph.
    """

    query = """
    MATCH (job:Job)
    RETURN job.title AS title
    ORDER BY job.title
    """

    with driver.session() as session:
        result = session.run(query)

        return [
            record["title"]
            for record in result
        ]

def get_student_graph(student_name):
    """
    Get the connected graph information for a student.

    Traversals:

    Student -> HAS_SKILL -> Skill

    Student -> WORKED_ON -> Project -> USES -> Technology

    Student -> HAS_SKILL -> Skill <- REQUIRES <- Job
    """

    query = """
    MATCH (student:Student {name: $student_name})

    OPTIONAL MATCH (student)-[:HAS_SKILL]->(skill:Skill)
    WITH student, collect(DISTINCT skill) AS skills

    OPTIONAL MATCH (student)-[:WORKED_ON]->(project:Project)
    WITH student, skills, collect(DISTINCT project) AS projects

    OPTIONAL MATCH (project:Project)-[:USES]->(technology:Technology)
    WHERE project IN projects
    WITH student, skills, projects,
         collect(DISTINCT technology) AS technologies

    OPTIONAL MATCH (job:Job)-[:REQUIRES]->(job_skill:Skill)
    WHERE job_skill IN skills
    WITH student, skills, projects, technologies,
         collect(DISTINCT job) AS jobs

    RETURN
        student.name AS student,

        [
            skill IN skills
            WHERE skill IS NOT NULL
            | {
                name: skill.name,
                category: skill.category
            }
        ] AS skills,

        [
            project IN projects
            WHERE project IS NOT NULL
            | {
                name: project.name,
                description: project.description
            }
        ] AS projects,

        [
            technology IN technologies
            WHERE technology IS NOT NULL
            | {
                name: technology.name,
                category: technology.category
            }
        ] AS technologies,

        [
            job IN jobs
            WHERE job IS NOT NULL
            | job.title
        ] AS matching_jobs
    """

    with driver.session() as session:
        result = session.run(
            query,
            student_name=student_name
        )

        record = result.single()

        if not record:
            return None

        return record.data()
def get_all_students():
    """
    Return all students available in SkillGraph.
    """

    query = """
    MATCH (student:Student)
    RETURN student.name AS name
    ORDER BY student.name
    """

    with driver.session() as session:
        result = session.run(query)

        return [
            record["name"]
            for record in result
        ]