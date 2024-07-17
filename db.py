from pymongo import MongoClient
from config import mongo_user_name, mongo_password, mongo_host, mongo_port
from logger import logger
from config import db_name
# Your MongoDB connection string
# These details are to be updated in the config.py
mongo_uri = f'mongodb://ras:ras_password@172.29.27.114:27017/'

def insert_transaction(json_data, _collection='bitcoin_transactions'):
    """
    Inserts  a single transaction into the db and then closes the connection
    :param _collection:
    :param json_data:
    :return:
    """
    client = MongoClient(mongo_uri)
    db = client.get_database(db_name)

    # Choose or create a collection
    collection = db.get_collection(_collection)
    # Set tx_hash as the primary key and update if exists
    try:
        result = collection.update_one(
            {"_id": json_data["tx_hash"]},
            {"$set": json_data},
            upsert=True
        )
    except Exception as e:
        logger.exception("unable to insert the data")
    # Close the MongoDB connection
    client.close()

    if result.upserted_id is not None:
        logger.info("Data inserted into MongoDB successfully.")
        return True
    else:
        logger.info("Data updated in MongoDB successfully.")
        return True


def insert_bulk_bitcoin_transactions(block_number, json_data_list, _collection='bitcoin_transactions'):
    """
    Inserts multiple transactions into the db and then closes the db
    :param _collection:
    :param json_data_list: list of the transactions
    :return:
    """
    # TODO: check if block_number is not null
    try:
        if not block_number:
            raise ValueError("Block number cannot be null")
    except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            return False
        
    
    client = MongoClient(mongo_uri)
    db = client.get_database(db_name)

    # Choose or create a collection
    collection = db.get_collection(_collection)
    logger.debug("start to insert bulk transactions")
    # TODO: take block_number as _id and add trxs as an object
    # result = {}
    # for json_data in json_data_list:
    try:    
        result = collection.update_one(
            {"_id": block_number},
            {"$push": {"transactions": {"$each": json_data_list}}},
        # {"$set": {"transactions": json_data_list}}, # append existing trxs with new trxs
        upsert=True
        )
    except Exception as e:
        logger.exception("unable to insert the data")
    # Close the MongoDB connection
    client.close()
    if result.upserted_id is not None:
        logger.info("Data inserted into MongoDB successfully.")
        return True
    else:
        logger.info("Data updated in MongoDB successfully.")
        return True
    # logger.debug("successfully inserted bulk transactions")
    # return True
            
    # get trx count for each block from db
    # should get block number andreturn trx count
def insert_bulk_bitcoin_transactions(block_number, json_data_list):
    """
    Inserts multiple transactions into the db and then closes the db
    :param block_number: The block number to insert transactions for
    :param json_data_list: List of the transactions
    :return: Boolean indicating success
    """
    if not block_number:
        logger.error("Block number cannot be null")
        return False

    client = MongoClient(mongo_uri)
    db = client.get_database(db_name)

    # Choose or create a collection
    collection = db.get_collection(collection_name)
    logger.debug("Start to insert bulk transactions")

    try:    
        result = collection.update_one(
            {"_id": block_number},
            {"$push": {"transactions": {"$each": json_data_list}}},
            upsert=True
        )
    except Exception as e:
        logger.exception("Unable to insert the data")
        client.close()
        return False

    # Close the MongoDB connection
    client.close()

    if result.upserted_id is not None:
        logger.info("Data inserted into MongoDB successfully.")
        return True
    else:
        logger.info("Data updated in MongoDB successfully.")
        return True

def get_trx_count_from_db(block_number):
    """
    Gets the transaction count for a specific block number from the db
    :param block_number: Block number to get transaction count for
    :return: Number of transactions for the block
    """
    client = MongoClient(mongo_uri)
    db = client.get_database(db_name)

    # Choose or create a collection
    collection = db.get_collection(collection_name)
    
    try:
        block = collection.find_one({"_id": block_number}, {"transactions": 1})
        if block and "transactions" in block:
            trx_count = len(block["transactions"])
        else:
            trx_count = 0
    except Exception as e:
        logger.exception("Unable to retrieve the transaction count")
        trx_count = None
    finally:
        # Close the MongoDB connection
        client.close()
    
    return trx_count