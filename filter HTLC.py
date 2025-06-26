from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('')
db = client['btc'] 
collection = db['bitcoin_transactions']  

def if_htlc(tx):
    htlc_patterns = ['OP_IF', 'OP_HASH160', 'OP_EQUALVERIFY', 'OP_CHECKLOCKTIMEVERIFY', 'OP_ELSE', 'OP_ENDIF']
    
    for vout in tx['vout']:
        script = vout['scriptPubKey']['asm']
        contains_all_patterns = True  
        
        for pattern in htlc_patterns:
            if pattern not in script:
                contains_all_patterns = False  
                break  
        
        if contains_all_patterns:
            return True  
    
    return False  

#  filter HTLC transactions
htlc_transactions = []
for tx in collection.find():
    if if_htlc(tx):
        htlc_transactions.append(tx)

# Output
for htlc_tx in htlc_transactions:
    print(htlc_tx)

# Close DB
client.close()



