import os

from dotenv import load_dotenv
from neo4j import GraphDatabase 

# Load variables from the .env file
load_dotenv()


# Read CognoDB connection details
COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")


# Check that all required values exist
if not COGNODB_URI:
    raise ValueError("COGNODB_URI is missing from .env")

if not COGNODB_USERNAME:
    raise ValueError("COGNODB_USERNAME is missing from .env")

if not COGNODB_PASSWORD:
    raise ValueError("COGNODB_PASSWORD is missing from .env")


# Create the Neo4j driver
driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
)


def test_connection():
    """
    Test the connection between SkillGraph and CognoDB.
    """

    driver.verify_connectivity()

    with driver.session() as session:
        result = session.run("RETURN 1 AS result")
        record = result.single()

        return record["result"]
