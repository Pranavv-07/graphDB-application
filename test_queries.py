from queries import rank_students_for_job


results = rank_students_for_job(
    "AI Developer Intern"
)

print("Student ranking:")
print()

for student in results:
    print(
        f"{student['student']} | "
        f"{student['matched']}/{student['total_required']} "
        f"skills | "
        f"Matching: {student['matching_skills']}"
    )