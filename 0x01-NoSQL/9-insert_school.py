#!/usr/bin/env python3
"""insert_school module"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs

    Args:
        mongo_collection (Collection): pymongo collection object.

    Returns:
        Any: id of the inserted document or an empty string if kwargs
            was empty.
    """
    if kwargs:
        inserted = mongo_collection.insert_one(kwargs)
        return inserted.inserted_id
    else:
        return ""
