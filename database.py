import atexit
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables from .env
load_dotenv()

# Read and sanitize connection details
COGNODB_URI = (os.getenv("COGNODB_URI") or "").strip()
COGNODB_USERNAME = (os.getenv("COGNODB_USERNAME") or "").strip()
COGNODB_PASSWORD = (os.getenv("COGNODB_PASSWORD") or "").strip()

# Validate that all required values are present
if not COGNODB_URI:
    raise ValueError("COGNODB_URI is missing from .env")
if not COGNODB_USERNAME:
    raise ValueError("COGNODB_USERNAME is missing from .env")
if not COGNODB_PASSWORD:
    raise ValueError("COGNODB_PASSWORD is missing from .env")

# Create the Neo4j driver.
# bolt+ssc:// already encodes "encrypted + trust self-signed certificate",
# so no extra encrypted= / trust= kwargs are needed or allowed by the driver.
try:
    driver = GraphDatabase.driver(
        COGNODB_URI,
        auth=(COGNODB_USERNAME, COGNODB_PASSWORD),
    )
except Exception as e:
    raise RuntimeError(
        f"SkillGraph could not create a database driver for '{COGNODB_URI}'. "
        f"Check your .env credentials and that the CognoDB instance is running. "
        f"Original error: {e}"
    ) from e

# Ensure the driver is cleanly closed when the process exits,
# preventing the ResourceWarning: unclosed BoltDriver error in neo4j v6.
atexit.register(driver.close)


def test_connection():
    """
    Verify connectivity to CognoDB. Returns 1 on success, raises on failure.
    """
    driver.verify_connectivity()
    with driver.session() as session:
        result = session.run("RETURN 1 AS result")
        record = result.single()
        return record["result"]
