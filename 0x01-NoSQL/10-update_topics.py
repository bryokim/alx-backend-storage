#!/usr/bin/env python3
"""update_topics module"""


def update_topics(mongo_collection, name, topics):
    """Changes all topics of a school document based on the name

    Args:
        mongo_collection (Collection): pymongo collection object.
        name (str): name of the school to update.
        topics (List[str]): List of topics.
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
