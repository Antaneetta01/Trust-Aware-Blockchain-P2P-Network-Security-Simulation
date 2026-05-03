import hashlib
import random
import string
from blockchain import Transaction, Block


def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


class Node:
    def __init__(self, node_id):
        self.node_id = node_id

        self.private_key = generate_key()
        self.public_key = generate_key()
        self.identity = hashlib.sha256(self.public_key.encode()).hexdigest()

        self.local_trust = 100
        self.global_trust = 100
        self.final_trust = 100

        self.peers = []
        self.received_gossip = []

        self.mempool = []
        self.blockchain = []

        self.malicious = False
        self.eclipsed = False

    # -------- Transactions --------
    def create_transaction(self):
        tx = Transaction(self.identity)
        self.mempool.append(tx)
        return tx

    def broadcast_transaction(self):
        for peer in self.peers:
            tx = Transaction(self.identity)
            peer.receive_transaction(tx, self)

    def receive_transaction(self, tx, sender):
        if sender.final_trust <= 30:
            return

        if sender.malicious:
            sender.update_local_trust(False)

            # The victim of repeated malicious traffic also suffers some trust uncertainty
            if self.eclipsed:
                self.update_local_trust(False, penalty=5)

            return

        self.mempool.append(tx)
        sender.update_local_trust(True)

    # -------- Blocks --------
    def create_block(self):
        if len(self.mempool) < 3:
            return None

        block = Block(self.mempool[:3])
        self.blockchain.append(block)
        self.mempool = self.mempool[3:]
        return block

    def broadcast_block(self):
        if self.malicious:
            block = Block([])
        else:
            block = self.create_block()

        if not block:
            return

        for peer in self.peers:
            peer.receive_block(block, self)

    def receive_block(self, block, sender):
        if sender.final_trust <= 30:
            return

        if sender.malicious or len(block.transactions) == 0:
            sender.update_local_trust(False)

            if self.eclipsed:
                self.update_local_trust(False, penalty=5)

            return

        self.blockchain.append(block)
        sender.update_local_trust(True)

    # -------- Trust --------
    def update_local_trust(self, valid, penalty=12):
        if valid:
            self.local_trust = min(100, self.local_trust + 1)
        else:
            self.local_trust = max(0, self.local_trust - penalty)

    def share_gossip(self):
        if self.malicious:
            return 100
        return self.final_trust

    def receive_gossip(self, value, sender):
        if sender.final_trust > 70 and not sender.malicious:
            self.received_gossip.append(value)

    def update_global_trust(self):
        if self.received_gossip:
            self.global_trust = sum(self.received_gossip) / len(self.received_gossip)
        else:
            # If a node receives no trusted gossip, trust slightly decays
            self.global_trust = max(0, self.global_trust - 2)

        self.received_gossip.clear()

    def update_final_trust(self):
        self.final_trust = 0.75 * self.local_trust + 0.25 * self.global_trust

    def get_status(self):
        if self.final_trust > 70:
            return "Trusted"
        elif self.final_trust > 30:
            return "Suspicious"
        else:
            return "Malicious"