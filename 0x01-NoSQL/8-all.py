#!/usr/bin/env python3
"""list_all module"""


def list_all(mongo_collection):
    """Lists all documents in a collection

    Args:
        mongo_collection (Collection): pymongo collection object.

    Returns:
        Cursor | List: Return a cursor object if there are documents in
            the collection, else return an empty list.
    """
    all = mongo_collection.find()

    return all
