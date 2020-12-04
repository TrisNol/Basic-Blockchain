from hashlib import sha256
import json

class Block(dict):

    def __init__(self, index, transactions, timestamp, previous_hash):
        """
        Constructor for the Block class.
        :param index: Unique ID of the block.
        :param transactions: List of transactions (syn.: data)
        :param timestamp: Time of generation of the block
        :param previous_hash: Hash of the previous block in the chain
        """
        super(Block, self).__init__()
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        Returns the hash of the block instance by first converting it into JSON string.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()