#!/usr/bin/env python3

"""
Returns all students sorted by average score
"""

def top_students(mongo_collection):
    """
    Returns all students sorted by average score

    Args:
        mongo_collection: pymongo collection object
    """
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {"_id": "$_id", "averageScore": {"$avg": "$scores.score"}}},
        {"$sort": {"averageScore": -1}},
        {"$project": {"_id": 1, "averageScore": 1}}
    ]

    students = list(mongo_collection.aggregate(pipeline))

    for student in students:
        student["_id"] = str(student["_id"])

    return students


if  __name__ == "__main__":
    pass
