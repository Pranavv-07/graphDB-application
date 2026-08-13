from database import test_connection


print("========================================")
print("       SkillGraph Connection Test")
print("========================================")
print()

try:
    result = test_connection()

    print("Connected to CognoDB successfully!")
    print(f"Database returned: {result}")

except Exception as error:
    print("Could not connect to CognoDB.")
    print()
    print("Error:")
    print(error)
