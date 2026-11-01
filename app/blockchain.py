import hashlib
import json
from datetime import datetime


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        self.chain.append({
            "index": 1,
            "timestamp": str(datetime.utcnow()),
            "data": "Genesis Block",
            "previous_hash": "0",
            "hash": "0"
        })

    def get_previous_block(self):
        return self.chain[-1]

    def create_block(self, data):

        previous_block = self.get_previous_block()

        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.utcnow()),
            "data": data,
            "previous_hash": previous_block["hash"]
        }

        block["hash"] = self.calculate_hash(block)

        self.chain.append(block)

        return block

    def calculate_hash(self, block):

        block_string = json.dumps(
            block,
            sort_keys=True
        ).encode()

        return hashlib.sha256(block_string).hexdigest()