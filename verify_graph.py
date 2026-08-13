from database import driver


queries = {
    "Students": "MATCH (s:Student) RETURN count(s) AS count",
    "Skills": "MATCH (s:Skill) RETURN count(s) AS count",
    "Projects": "MATCH (p:Project) RETURN count(p) AS count",
    "Technologies": "MATCH (t:Technology) RETURN count(t) AS count",
    "Jobs": "MATCH (j:Job) RETURN count(j) AS count",
    "HAS_SKILL relationships": """
        MATCH ()-[r:HAS_SKILL]->()
        RETURN count(r) AS count
    """,
    "WORKED_ON relationships": """
        MATCH ()-[r:WORKED_ON]->()
        RETURN count(r) AS count
    """,
    "USES relationships": """
        MATCH ()-[r:USES]->()
        RETURN count(r) AS count
    """,
    "REQUIRES relationships": """
        MATCH ()-[r:REQUIRES]->()
        RETURN count(r) AS count
    """
}


with driver.session() as session:

    print()
    print("========================================")
    print("       SkillGraph Database Check")
    print("========================================")
    print()

    for name, query in queries.items():

        result = session.run(query)
        record = result.single()

        print(f"{name}: {record['count']}")
