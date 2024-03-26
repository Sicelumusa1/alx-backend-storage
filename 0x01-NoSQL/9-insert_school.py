#!/usr/bin/env python3

"""
Inserts a new document in a collection based on kwargs
"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs

    Args:
        mongo_collection: the pymongo collection object
        **kwargs: Keyword arguments representing the fields and values

    Returns:
        _id: id of the inserted document.
    """
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)

    return result.inserted_id


if __name__ == "__main__":
    pass
