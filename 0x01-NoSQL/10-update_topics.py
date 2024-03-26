#!/usr/bin/env python3

"""
Changes all topics of a school document based on the name
"""

import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name

    Args:
        mongo_collection: pymongo collection object
        name (str): school name to update
        topics (list): list of topics approached in the school
    """
    result = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
    return result.modified_count


if __name__ == "__main__":
    pass
