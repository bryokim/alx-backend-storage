#!/usr/bin/env python3
"""top_students module"""


def top_students(mongo_collection):
    """Returns all students sorted by average score

    Args:
        mongo_collection (Collection): pymongo collection object.

    Returns:
        CommandCursor: Students with the average score calculated and
            sorted in descending order.
    """
    return mongo_collection.aggregate(
        [
            {
                "$addFields": {
                    "averageScore": {
                        "$toDouble": {
                            "$avg": {
                                "$map": {
                                    "input": "$topics",
                                    "as": "topic",
                                    "in": {"$toDouble": "$$topic.score"},
                                }
                            }
                        },
                    }
                }
            },
            {"$sort": {"averageScore": -1}},
        ]
    )
