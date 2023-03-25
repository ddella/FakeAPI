import logging
import json
from app.definitions import Category, Item

from enum import Enum
from pydantic import BaseModel, parse_file_as, parse_obj_as
from fastapi.encoders import jsonable_encoder
from os import getenv

# The file simulates a fake database for our data
DATABASE = getenv('DATABASE', 'data.json')

def writeJSON(filename: str, myList: list[Item]) -> bool:
    """
    Writes the list of Pydantic model "Item" to a file.
    :param filename: name of the file
    :param myList: the list of Pydantic model "Item"
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
    # each item of myList is converted from Pydantic model to a dict and added to a list
    try:
        record = [jsonable_encoder(d) for d in myList]
    except Exception as e:
        # "myList" was empty, just write an empty list in the JSON file
        record = []

    # the list of dict is saved to a JSON file
    json.dump(record, out_file, indent=3)
    out_file.close()
    return True

def readJSON(filename: str) -> list[Item]:
    """
    Read a JSON file that contains a list of Pydantic model "Item" that represents synthetic data
    :param filename: JSON file to read
    :return: True if success, False otherwise
    """
    try:
        with open(filename, 'r', encoding='utf-8') as jsonFile:
            data_loaded = json.load(jsonFile)
        jsonFile.close()
        logging.info(f'JSON file "{filename}" was read successfully')
        return parse_obj_as(list[Item], data_loaded)
    except IOError as e:
        # The database could be empty, it's not an error but user should be warned
        logging.warning(f'IOErro: {e}')
        # Empty list of Item
        return []

def readData() -> list[Item]:
    return readJSON(DATABASE)

def writeData(listOfItems):
    writeJSON(DATABASE, listOfItems)


if __name__ == "__main__":
    items = [
        Item(id=100, description="Hammer", price=9.99, quantity=20, category=Category.TOOLS),
        Item(id=101, description="Jeans", price=39.99, quantity=100, category=Category.CLOTHES),
        Item(id=102, description="Apple", price=0.50, quantity=150, category=Category.GROCERY),
        Item(id=103, description="Radio AM/FM", price=25.49, quantity=5, category=Category.CONSUMABLES),
    ]

    # logger config
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(levelname)s %(funcName)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # Read the data file (fake database)
    # if not readJSON(DATABASE):
    #     writeJSON(DATABASE, importedSyntheticData)
    #     logging.info(f'Empty file {DATABASE} created')
    # print(importedSyntheticData)
    writeJSON(DATABASE, items)
