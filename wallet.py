import random
from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service
from bitcoinlib.services.bitcoind import Bitcoind

from parser_utils import ad_to_dict
from logger import logger

# Replace with your Bitcoin node configuration
BITCOIN_RPC_URL = 'http://your_bitcoin_node_rpc_url'
BITCOIN_RPC_USER = 'your_rpc_user'
BITCOIN_RPC_PASSWORD = 'your_rpc_password'

def get_block_timestamp(block_number=None):
    """
    Returns the block timestamp
    if no block_number is provided, then returns the last block timestamp
    :param block_number:
    :return:
    """
    # Connect to Bitcoin node
    service = Bitcoind(url=BITCOIN_RPC_URL, rpcuser=BITCOIN_RPC_USER, rpcpassword=BITCOIN_RPC_PASSWORD)
    if service.ping():
        logger.info("Connected to Bitcoin node")
        if not block_number:
            # Get the latest block if no block number is provided
            block_number = service.getblockcount()
            logger.debug("No block number is provided, fetching latest block")

        logger.info(f"Fetching for block number {block_number}")

        # Get the block details
        block = service.getblock(block_number)
        block = ad_to_dict(block)
        return block.get('time')

    else:
        logger.error("Failed to connect to Bitcoin node")
        raise ConnectionError('Unable to connect to Bitcoin node')

def get_trx_receipt(trx_hash):
    """
    Returns the transaction receipt for the given transaction hash
    :param trx_hash:
    :return:
    """
    # Connect to Bitcoin node
    service = Bitcoind(url=BITCOIN_RPC_URL, rpcuser=BITCOIN_RPC_USER, rpcpassword=BITCOIN_RPC_PASSWORD)
    if service.ping():
        logger.info("Connected to Bitcoin node")
        try:
            return service.gettransaction(trx_hash)
        except Exception as e:
            logger.debug("Transaction not found")
            print('Transaction not found')
            return None
    else:
        logger.error("Failed to connect to Bitcoin node")
        raise ConnectionError('Unable to connect to Bitcoin node')
