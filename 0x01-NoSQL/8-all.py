#!/usr/bin/env python3

"""
Lists all documents in a collection
"""

import pymongo


def list_all(mongo_collection):
    """
    Lists all documents in a collection

    Args:
        mongo_collection: Pymongo collection object

    Returns:
         list: list of all documents in a collection or empty
                list if no document in the collection
    """
    documents = list(mongo_collection.find())
    return documents if documents else []


if __name__ == "__main__":
    pass
