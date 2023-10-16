#!/usr/bin/env python3
"""Module for printing stats about Nginx logs"""

from pymongo import MongoClient


def get_stats():
    """Provides stats about Nginx logs stored in MongoDB.

    Database: logs
    Collection: nginx
    """

    client = MongoClient()
    nginx_collection = client.logs.nginx

    print("{} logs".format(nginx_collection.count_documents({})))

    print_methods(nginx_collection)
    print_get_status(nginx_collection)
    print_ips(nginx_collection)

    client.close()


def print_methods(col):
    """Print the methods and their counts.

    Args:
        col (Collection): nginx collection in the logs database.
    """

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        count = col.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))


def print_get_status(col):
    """Print the number of times path status has been visited
    using the GET method.

    Args:
        col (Collection): nginx collection in the logs database.
    """

    count = col.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(count))


def print_ips(col):
    """Print most frequently visited IPs with the amount of times
    visited.

    Args:
        col (Collection):nginx collection in the logs database.
    """
    cursor = col.aggregate(
        [
            {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10},
        ]
    )

    print("IPs:")

    for doc in cursor:
        print("\t{}: {}".format(doc["_id"], doc["count"]))


if __name__ == "__main__":
    get_stats()
