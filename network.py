import random

def connect_network(nodes, max_peers=3):
    for node in nodes:
        node.peers = random.sample(
            [n for n in nodes if n != node],
            k=min(max_peers, len(nodes)-1)
        )