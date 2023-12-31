#!/usr/bin/env python3
"""schools_by_topic module"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of school having a specific topic.

    Args:
        mongo_collection (Collection): pymongo collection object.
        topic (str): topic to search for.

    Returns:
        Cursor: cursor object of the documents containing the given topic.
    """
    return mongo_collection.find({"topics": topic})
