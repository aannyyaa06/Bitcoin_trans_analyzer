import time
import datetime
from google.cloud import bigquery
from db import insert_bulk_bitcoin_transactions
from parser_utils import get_bquery_trx
from utils import get_utc_date_1_hours_ago, time_to_next_run
from logger import logger
from datetime import datetime, timezone
import os

# Set up BigQuery client
# client = bigquery.Client.from_service_account_json("C:\\Users\\ashis\\Downloads\\ferrous-kayak-427014-i0-bf11e05599d8.json")
# cred_path = os.path.join('..','bitcoin' 'cred', 'cred.json')
client = bigquery.Client.from_service_account_json("C:\\Users\\ashis\\Desktop\\aanya\\bitcoin\\cred\\cred.json")

#SYN_DIST_IN_MIN = 15  # denotes the latest block at time of sync

# Function definitions
def get_last_synced_block():
    try:
        with open('last_sync_block.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def get_block_timestamp(block_number):
    # implement logic to get block timestamp from BigQuery or other source
    pass

def check_sync_status(_last_block_timestamp):
    """
    Checks the sync status, is it fine to sync?
    :return:
    """
    logger.info("Checking sync status")
    current_timestamp = int(datetime.now(timezone.utc).timestamp())
    if (current_timestamp - _last_block_timestamp) / 60 < SYN_DIST_IN_MIN:
        logger.info("Last sync too recent, waiting...")
        wait_time = time_to_next_run()
        logger.info(f"Sleeping until next run ({wait_time} seconds)")
        time.sleep(wait_time)

def fetch_block_transactions(block_number):
    # Construct the query
    min_date = get_utc_date_1_hours_ago()
    max_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    query = f"""
            SELECT
  block_hash,
  block_number,
  block_timestamp,
  inputs,
  outputs
FROM
  bigquery-public-data.crypto_bitcoin.transactions
WHERE
    block_timestamp_month = DATE_TRUNC(CURRENT_DATE(), MONTH)
AND block_number between 851132 and 851133

    """
    print("Querying :", query)
    # Execute the query
    query_job = client.query(query)
    results = query_job.result()
    print(results)
    # Process and store the extracted data
    all_transactions = []
    for row in results:
        transaction_data = row.values()  # Access transaction data as a tuple
        all_transactions.append(get_bquery_trx(transaction_data))
        # print(all_transactions)

    return all_transactions

def insert_bulk_transactions(transactions, table_name):
    # implement logic to insert transactions into your database
    pass

# Main script
while True:
    # last_block_no = get_last_synced_block()
    last_block_no =851132 

    try:
        for block_number in range(last_block_no, last_block_no +2):
            transactions = fetch_block_transactions(block_number)
            print("Got trxs:", len(transactions))
            if transactions:
                insert_bulk_bitcoin_transactions(block_number,transactions)
                print(f'Inserted transactions for block {block_number} successfully')
    except Exception as e:
        logger.exception(e)
    
