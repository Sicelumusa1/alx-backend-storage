#!/usr/bin/env python3

"""
Returns the list of school having a specific topic
"""

import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic

    Args:
        mongo_collection:pymongo collection object
        topic (str): topic searched
    Returns:
        List of dicts representing scholls with the specific topic
    """
    schools = list(mongo_collection.find({"topics": topic}))
    return schools


if __name__ == "__main__":
    pass
