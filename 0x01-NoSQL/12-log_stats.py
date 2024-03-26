#!/usr/bin/env python3

"""
Provides some stats about Nginx logs stored in MongoDB
"""

import pymongo


def get_nginx_logs_stats(mongo_collection):
    """
    Gets some stats about Nginx logs stored in MongoDB

    Args:
        mongo_collection: pymongo collection object for Nginx logs

    Returns:
        A dict with stats about Nginx logs
    """
    stats = {}

    total_logs = mongo_collection.count_documents({})
    stats['total_logs'] = total_logs
    
    # Count of each HTTP method
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in http_methods:
        count = mongo_collection.count_documents({"method": method})
        method_counts[method] = count
    stats['method_counts'] = method_counts

    # Number of logs wuth method=GET and path=/status
    status_logs_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    stats['status_logs_count'] = status_logs_count

    return stats


def display_stats(stats):
    """
    Displays stats about Nginx logs

    Args:
        stats: A dict of stats about the Nginx logs
    """
    print(f"{stats['total_logs']} logs")

    print("Methods:")
    for method, count in stats['method_counts'].items():
        print(f"\tmethod {method}: {count}")

    print(f"{stats['status_logs_count']} status check")


if __name__ == "__main__":
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['logs']
    nginx_collection = db['nginx']
    
    # Get and display stats
    stats = get_nginx_logs_stats(nginx_collection)
    display_stats(stats)
