# jwtauth/database.py
# *** This is the same as app/database.py *** should be ONE module

import logging
import json
from jwtauth.model import UserSchema, USR_DATABASE
from pydantic import parse_obj_as
from fastapi.encoders import jsonable_encoder

def writeJSON(filename: str, myList: list[UserSchema]) -> bool:
    """
    Writes the list of Pydantic model "UserSchema" to a file.
    :param filename: name of the file
    :param myList: the list of Pydantic model "UserSchema"
    :return: True if success, False otherwise
    """
    try:
        out_file = open(filename, 'x', encoding='utf-8')
        logging.info(f'File "{filename}" was created')
    except FileExistsError:
        out_file = open(filename, 'w', encoding='utf-8')
        logging.warning(f'Existing file "{filename}" was overwitten')
    except IOError as e:
        logging.error(f'{e}')
        return False
    # each UserSchema of myList is converted from Pydantic model to a dict and added to a list
    try:
        record = [jsonable_encoder(d) for d in myList]
    except Exception as e:
        # "myList" was empty, just write an empty list in the JSON file
        record = []

    # the list of dict is saved to a JSON file
    json.dump(record, out_file, indent=3)
    out_file.close()
    return True

def readJSON(filename: str) -> list[UserSchema]:
    """
    Read a JSON file that contains a list of Pydantic model "UserSchema" that represents synthetic data
    :param filename: JSON file to read
    :return: True if success, False otherwise
    """
    try:
        with open(filename, 'r', encoding='utf-8') as jsonFile:
            data_loaded = json.load(jsonFile)
        jsonFile.close()
        logging.info(f'JSON file "{filename}" was read successfully')
        return parse_obj_as(list[UserSchema], data_loaded)
    except IOError as e:
        # The database could be empty, it's not an error but user should be warned
        logging.warning(f'IOErro: {e}')
        # Empty list of UserSchema
        return []

def readUsrData() -> list[UserSchema]:
    return readJSON(USR_DATABASE)

def writeUsrData(listOfItems):
    writeJSON(USR_DATABASE, listOfItems)


if __name__ == "__main__":
    importedSyntheticUsrData: list[UserSchema]
    items = [
        UserSchema(id='16fd2706-8baf-433b-82eb-8c7fada847da', fullname="User1 Name1", email="user1@example.com", password="Password1"),
        UserSchema(id='3720f69a-a72f-47b4-8caf-46ff0b83523e', fullname="User2 Name2", email="user2@example.com", password="Password2"),
        UserSchema(id='1b702cc8-4e71-4685-bc48-df62a8205fd7', fullname="User3 Name3", email="user3@example.com", password="Password3"),
        UserSchema(id='ee96aaeb-9f79-44d2-8559-cd5941ed3b29', fullname="User4 Name4", email="user4@example.com", password="Password4"),
    ]

    # logger config
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(levelname)s %(funcName)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # Read the data file (fake user database)
    # if not readJSON(USR_DATABASE):
    #     writeJSON(USR_DATABASE, importedSyntheticUsrData)
    #     logging.info(f'Empty file {USR_DATABASE} created')
    # print(importedSyntheticData)
    writeJSON(USR_DATABASE, items)
