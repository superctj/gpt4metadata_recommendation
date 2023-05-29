from enum import Enum

from pymongo import MongoClient


MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB_NAME = "icpsr"
MONGO_COLLECTION_NAME = "subject_thesaurus"


class TermRelationshipID(Enum):
    NARROWER = 1
    BROADER = 2
    RELATED = 3
    PREFERRED = 4
    NONPREFERRED = 5


class TermRelationshipName(Enum):
    NARROWER = "narrower terms"
    BROADER = "broader terms"
    RELATED = "related terms"
    PREFERRED = "preferred term"
    NONPREFERRED = "non-preferred term"


def get_mongo_collection():
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = client[MONGO_DB_NAME]
    col = db[MONGO_COLLECTION_NAME]

    return client, col
