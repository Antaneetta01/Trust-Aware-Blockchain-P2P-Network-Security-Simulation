import hashlib
import time
import random

class Transaction:
    def __init__(self, sender):
        self.sender = sender
        self.timestamp = time.time()
        self.tx_id = hashlib.sha256(
            f"{sender}{self.timestamp}{random.random()}".encode()
        ).hexdigest()


class Block:
    def __init__(self, transactions, prev_hash="0"):
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.timestamp = time.time()
        self.nonce = random.randint(0, 100000)
        self.block_hash = self.compute_hash()

    def compute_hash(self):
        data = str(self.prev_hash) + str(self.timestamp) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()