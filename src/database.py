__author__ = "Daniel Della-Noce"
__author_email__ = "daniel@isociel.com"
__license__ = "MIT"

import pymongo.database
import pymongo.collection
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import settings
from pymongo.results import DeleteResult
# import logging
from logger import logging
import json

"""
This class is for basic CRUD operations on a MongoDB server

WARNING -
For educationnal purposes only, do not use in production.
https://kb.objectrocket.com/mongo-db/how-to-update-a-mongodb-document-in-python-356
https://kb.objectrocket.com/mongo-db/how-to-update-multiple-mongodb-documents-in-python-359
https://kb.objectrocket.com/mongo-db/python-mongoclient-examples-1050
https://realpython.com/introduction-to-mongodb-and-python/
https://medium.com/analytics-vidhya/crud-operations-in-mongodb-using-python-49b7850d627e
https://codevoweb.com/api-with-python-fastapi-and-mongodb-jwt-authentication/
"""

class MongoDB:
    def __init__(self):
        # logger config
        # logging.basicConfig(level=logging.INFO,
        #                     format='%(asctime)s: %(levelname)s %(funcName)s %(message)s',
        #                     datefmt='%Y-%m-%d %H:%M:%S')
        self.myClient = None
        self.myClient: MongoClient

        self.myDatabase: pymongo.database.Database
        self.myDatabase = None

        self.myCollection: pymongo.collection.Collection
        self.myCollection = None

        self.initMongoDB()
        self.initDB()
        self.initCollection()

    def addOneDocument1(self, myFilter: dict, document: dict) -> dict | None:
        """
        Add one element only if the filter is not found
        :param myFilter: Selection criteria of update query
        :param document: New data to be updated
        :return: Return the original document before it was updated/replaced or
        None if no document matches the query.
        """
        # the _id field is also included. This field is always included unless specifically excluded.
        self.myCollection: pymongo.collection.Collection
        result = self.myCollection.find_one_and_update(myFilter, {'$set': document}, {"_id": False}, upsert=True)
        # print(f'DATABASE.PY:: type(result)={type(result)} - {result}')
        if result is None:
            logging.info(f'Element {document.get("id")} added to collection {settings.MONGO_INITDB_COLLECTION}')
        else:
            logging.info(f'Element {result.get("id")} updated')
        return result
        # return None

    def initMongoDB(self):
        """
        Establish a connection to the MongoDB server
        :return: Client handle if successuful or None
        """
        # List all fields from URI
        # for k, v in parse_uri(mongodbURI).items():
        #     logging.info(f'{k}: {v}')

        # try:
        myclient: MongoClient = MongoClient(settings.MONGO_DB_URI, timeoutMS=settings.MONGO_DB_TIMEOUT)
        logging.info(f'MongoClient = {myclient}')
        # except ConnectionFailure as e:
        #     logging.error(f'ConnectionFailure to database {settings.MONGO_DB_URI}: {e}')
        #     return None
        # except ConnectionRefusedError as e:
        #     logging.error(f'ConnectionRefusedError to database {settings.MONGO_DB_URI}: {e}')
        #     return None
        # except Exception as e:
        #     logging.error(f'ConnectionRefusedError to database {settings.MONGO_DB_URI}: {e}')
        #     return None
        # else:
            # logging.info(f'type(myclient) = {type(myclient)}')
            # print(f'Type(myclient) = {type(myclient)}')
        self.myClient = myclient

    @staticmethod
    def pingDB():
        client = MongoClient(settings.MONGO_DB_URI, timeoutMS=settings.DB_TIMEOUT)
        try:
            # The ping command is cheap and does not require auth.
            client.admin.command('ping')
        except ConnectionFailure as exc:
            logging.error(f'ConnectionFailure: Server not available: {exc}')
            return False
        else:
            logging.info(f'round_trip_time={client.round_trip_time}')
            return True

    def initDB(self):
        """
        Init the database
        :return:
        """
        # Get all collection(s)
        try:
            dbLists: [str] = self.myClient.list_database_names()
        except Exception as e:
            logging.error(f'Fatal error in MongoDB: {e}')
            self.myDatabase = None
        else:
            # MONGO_INITDB_DATABASE
            if settings.MONGO_INITDB_DATABASE in dbLists:
                logging.info(f'{settings.MONGO_INITDB_DATABASE} is in database(s) {dbLists}')
            else:
                logging.info(f'{settings.MONGO_INITDB_DATABASE} is NOT in database(s) {dbLists}')
            # logging.info(f'type(client[collection]) = {type(client[collection])}')
            self.myDatabase = self.myClient[settings.MONGO_INITDB_DATABASE]

    def initCollection(self):
        """
        Init the collection
        :return:
        """
        if self.myDatabase is None:
            logging.error(f'Something went wrong with the database')
            return
        # check if a collection exists
        col_exists = settings.MONGO_INITDB_COLLECTION in self.myDatabase.list_collection_names()
        if col_exists:
            logging.info(f'Collection "{settings.MONGO_INITDB_COLLECTION}" exists')
        else:
            logging.info(f'Collection "{settings.MONGO_INITDB_COLLECTION}" does NOT exists but was created')
        logging.info(f'List of all collection(s) for database "{self.myDatabase.name}" is/are:'
                     f' {self.myDatabase.list_collection_names()}')
        self.myCollection = self.myDatabase[settings.MONGO_INITDB_COLLECTION]

    def addOneDocument(self, myFilter: dict, document: dict) -> dict | None:
        """
        Add one element only if the filter is not found
        :param myFilter: Selection criteria of update query
        :param document: New data to be updated
        :return: Return the original document before it was updated/replaced or
        None if no document matches the query.
        """
        # the _id field is also included. This field is always included unless specifically excluded.
        self.myCollection: pymongo.collection.Collection
        # result = self.myCollection.update_one(myFilter, {'setOnInsert': document}, upsert=True)
        result = self.myCollection.find_one_and_update(myFilter, {'$set': document}, {"_id": False}, upsert=True)
        # print(f'DATABASE.PY:: type(result)={type(result)} - {result}')
        if result is None:
            logging.info(f'Element {document.get("id")} added to collection {settings.MONGO_INITDB_COLLECTION}')
        else:
            logging.info(f'Element {result.get("id")} updated')
        return result
        # return None

    # Destructor
    def __del__(self):
        if self.myClient:
            self.myClient.close()
            logging.info(f'Database was closed and object was destroy')

    def addManyDocuments(self, myFilterKey: str, documents: list[dict]) -> None:
        """
        :param myFilterKey: Selection criteria 'KEY' of update query
        :param documents: The list of documents to add
        :return:
        """
        # self.myCollection: pymongo.collection.Collection
        # self.myCollection.update_many()
        for doc in documents:
            self.addOneDocument({myFilterKey: doc.get(myFilterKey)}, doc)

    def findOneDocument(self, myFilter: dict) -> dict:
        document = self.myCollection.find_one(myFilter, {"_id": False})
        # print(f'Type(document) = {type(document)} -- {document}')
        return document

    def delOneDocument(self, myFilter: dict) -> int:
        """
        Delete one element if the filter is found
        :param myFilter: Selection criteria for delete query
        :return: Returns the number of documents deleted.
        """
        result: pymongo.results.DeleteResult
        result = self.myCollection.delete_one(myFilter)
        logging.info(f'{result.deleted_count} documents deleted')
        return result.deleted_count

    def delAllDocument(self) -> int:
        """
        Delete All Documents in a Collection
        :return: Returns the number of document(s) deleted
        """
        result: pymongo.results.DeleteResult = self.myCollection.delete_many({})
        # result = self.myCollection.delete_many({})
        logging.info(f'{result.deleted_count} documents deleted')
        return result.deleted_count

    def getTotalDocument(self) -> int:
        """
        :return: The total number of documents in a collection
        """
        total_docs = self.myCollection.count_documents({})
        logging.info(f'"{self.myCollection.name}" has a total of [{total_docs}] documents.')
        return total_docs

    def delCollection(self, collection: str) -> None:
        # check if a collection exists
        col_exists = collection in self.myDatabase.list_collection_names()
        # use the database_name.some_collection.drop() method call
        if col_exists:
            # get the collection object if it exists
            col = self.myDatabase[collection]
            # drop the collection
            col.drop()
            logging.info(f'Collection {collection} was deleted')
        else:
            logging.info(f'Collection {collection} does NOT exist')

    def viewAllDocuments(self) -> list:
        """
        Returns all the document of a collection. For troubleshooting only.
        Note: doc is a dictionnary
        :return: A list of all documents in the collection
        """
        allDocuments = []
        for doc in self.myCollection.find({}, {"_id": False}):
            allDocuments.append(doc)
        return allDocuments

    def listAllCollections(self) -> list:
        """
        :return: The list of all the collections
        """
        logging.info(f'list_collection_names() = {self.myDatabase.list_collection_names()}')
        return self.myDatabase.list_collection_names()

    def dbName(self) -> str:
        """
        :return: The list of all the collections
        """
        logging.info(f'list_collection_names() = {self.myDatabase.list_collection_names()}')
        self.myDatabase: pymongo.database.Database
        return self.myDatabase.name

    def updateOne(self, myFilter: dict, updatedFields: dict):
        self.myCollection: pymongo.collection.Collection
        self.myCollection.update_one(myFilter, {'$set': updatedFields})


if __name__ == "__main__":
    # Synthetic documents to add
    manyDocuments = [
        {
            "id": "850703190",
            "description": "Document 1",
            "price": 666.66,
            "quantity": 3
        },
        {
            "id": "562641783",
            "description": "Document 2",
            "price": 15.67,
            "quantity": 32
        },
        {
            "id": "342691233",
            "description": "Document 3",
            "price": 9.99,
            "quantity": 6
        },
        {
            "id": "112233445",
            "description": "Document 4",
            "price": 123.12,
            "quantity": 1
        },
        {
            "id": "333333333",
            "description": "Document 5",
            "price": 666.66,
            "quantity": 33
        },
        {
            "id": "444444444",
            "description": "Document 6",
            "price": 1.99,
            "quantity": 555
        },
        {
            "id": "123456789",
            "description": "Document 7",
            "price": 123.45,
            "quantity": 123
        }
    ]
    db = MongoDB()

    # add one element, if exists update it
    # new_val = {'description': 'Trysistors surface mount', 'id': '1234567805', 'price': 5.27, 'quantity': 217}
    # db.addOneDocument({"id": new_val["id"]}, new_val)

    # Insert multiple elements, if exists update them
    # db.addManyDocuments('id', manyDocuments)

    # delete one element if exists
    # del_val = {'id': '1234567802'}
    # db.delOneDocument(del_val)

    # Delete all documents in a collection
    # db.delAllDocument()

    # Find one document
    myDoc = db.findOneDocument({'id': '4444444441'})
    if myDoc is not None:
        print(f'\nfindOneDocuments: {json.dumps(myDoc)}\n')
    else:
        print(f'\nfindOneDocuments: NOT found Type(result) = {type(myDoc)}\n')

    # List all documents in a collection
    docs = db.viewAllDocuments()
    print(f'viewALLDocuments: {json.dumps(docs, indent=3)}')

    # Get the total number of documents in the database
    db.getTotalDocument()

    # Prints all the collections
    logging.info(f'All collections: {db.listAllCollections()}')

    # Prints the database name
    logging.info(f'DB name: {db.dbName()}')

    # Destroy the object
    del db
