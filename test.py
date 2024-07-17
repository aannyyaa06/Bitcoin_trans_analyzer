from pymongo import MongoClient
from config import mongo_user_name, mongo_password, mongo_host, mongo_port, db_name
from logger import logger
from config import db_name
import bitcoin

mongo_uri = f'mongodb://ras:ras_password@172.29.27.114:27017/'
def insert_bitcoin_transaction(tx_hex, _collection='bitcoin_transactions'):
    """
    Inserts a single Bitcoin transaction into the db
    :param _collection:
    :param tx_hex: hexadecimal representation of the Bitcoin transaction
    :return:
    """
    client = MongoClient(mongo_uri)
    db = client.get_database(db_name)
    collection = db.get_collection(_collection)

    try:
        # Decode the transaction hex
        tx = bitcoin.deserialize(tx_hex)

        # Extract relevant information from the transaction
        tx_data = {
            "_id": tx.GetHash(),
            "tx_hash": tx.GetHash(),
            "version": tx.nVersion,
            "lock_time": tx.nLockTime,
            "vin": [{"txid": vin.prevout.hash, "vout": vin.prevout.n} for vin in tx.vin],
            "vout": [{"value": vout.nValue, "scriptPubKey": vout.scriptPubKey} for vout in tx.vout]
        }

        # Insert or update the transaction in the database
        collection.update_one({"_id": tx_data["tx_hash"]}, {"$set": tx_data}, upsert=True)
        logger.info("Bitcoin transaction inserted/updated into MongoDB successfully.")
    except Exception as e:
        logger.exception("unable to insert the Bitcoin transaction")
    finally:
        client.close()

def insert_bulk_bitcoin_transactions(tx_hex_list, _collection='bitcoin_transactions'):
    """
    Inserts multiple Bitcoin transactions into the db
    :param _collection:
    :param tx_hex_list: list of hexadecimal representations of Bitcoin transactions
    :return:
    """
    client = MongoClient(mongo_uri)
    db = client.get_database(db_name)
    collection = db.get_collection(_collection)

    try:
        requests = []

        tx_data = tx_hex_list
        # Create a bulk write request
        requests.append({"UpdateOne": {"filter": {"_id": tx_data["block_number"]}, "update": {"$set": tx_data}, "upsert": True}})
        
        # Execute the bulk write
        collection.insert_many()
        logger.info("Bulk Bitcoin transactions inserted/updated into MongoDB successfully.")
    except Exception as e:
        logger.exception("unable to insert the Bitcoin transactions")
    finally:
        client.close()