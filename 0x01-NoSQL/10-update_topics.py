#!/usr/bin/env python3
"""update_topics module"""

from pymongo.collection import Collection
from typing import List


def update_topics(mongo_collection: Collection, name: str, topics: List[str]):
    """Changes all topics of a school document based on the name

    Args:
        mongo_collection (Collection): pymongo collection object.
        name (str): name of the school to update.
        topics (List[str]): List of topics.
    """
    mongo_collection.update_one(
        {"name": name}, {"$set": {"topics": topics}}, upsert=True
    )
