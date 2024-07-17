

from decimal import Decimal
import json
from datetime import datetime

# Google transaction parser
# Google transaction data structure
# Given data structure
BQUERY_TRX_STRUCTURE = {
    'tx_hash': 'STRING',
    'nonce': 'INTEGER',
    'transaction_index': 'INTEGER',
    'from_address': 'STRING',
    'to_address': 'STRING',
    'value': 'NUMERIC',
    'gas': 'INTEGER',
    'gas_price': 'INTEGER',
    'input': 'STRING',
    'receipt_cumulative_gas_used': 'INTEGER',
    'receipt_gas_used': 'INTEGER',
    'receipt_contract_address': 'STRING',
    'receipt_root': 'STRING',
    'receipt_status': 'INTEGER',
    'block_timestamp': 'TIMESTAMP',
    'block_number': 'INTEGER',
    'block_hash': 'STRING',
    'max_fee_per_gas': 'INTEGER',
    'max_priority_fee_per_gas': 'INTEGER',
    'transaction_type': 'INTEGER',
    'receipt_effective_gas_price': 'INTEGER'
}


# Custom JSON encoder to handle Decimal and Date time objects
class DecimalEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle Decimal and datetime objects
    """

    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        if isinstance(o, datetime):
            return int(o.timestamp())
        return super().default(o)


def get_bquery_trx(trx_tuple) -> dict:
    """
    returns the dict of bquery transactions
    :param trx_tuple: the bigquery transaction tuple
    :return: json_dict: dict of bquery transactions
    """
    # Create a dictionary from the tuple using the data structure
    transaction_dict = dict(zip(BQUERY_TRX_STRUCTURE.keys(), trx_tuple))
    # print(transaction_dict)
    # Convert the dictionary to JSON
    json_data = json.dumps(transaction_dict, indent=2, cls=DecimalEncoder)
    json_dict = json.loads(json_data)
    return json_dict


# Parse Attribute dictionary to dictionary
def ad_to_dict(dict_to_parse):
    """
    converts an attribute dictionary to dict
    :param dict_to_parse: Attribute dictionary to convert to dict
    :return: parsed_dict: converted attribute dictionary
    """
    # convert any 'AttributeDict' type found to 'dict'
    if not dict_to_parse:
        return None
    parsed_dict = dict(dict_to_parse)
    for key, val in parsed_dict.items():
        if 'list' in str(type(val)):
            parsed_dict[key] = [parse_value(x) for x in val]
        else:
            parsed_dict[key] = parse_value(val)
    return parsed_dict


def parse_value(val):
    """
    check for nested dict structures to iterate through
    :param val:
    :return:
    """
    # check for nested dict structures to iterate through
    if 'dict' in str(type(val)).lower():
        return ad_to_dict(val)
    # convert 'HexBytes' type to 'str'
    if 'HexBytes' in str(type(val)):
        return val.hex()
    return val
