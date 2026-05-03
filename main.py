from node import Node
from network import connect_network
from gossip import gossip_phase
from attacks import sybil_attack, collusion_attack, eclipse_attack
from metrics import evaluate
from visualization import plot_trust_evolution
import random


def print_status(nodes):
    print("\n--- Node Status ---")
    for n in nodes:
        print(f"{n.node_id}: Trust={round(n.final_trust)} ({n.get_status()})")


def run():
    random.seed(42)
    nodes = [Node(i) for i in range(6)]

    sybil_attack(nodes, 2)
    collusion_attack(nodes, [1])

    # Connect after adding Sybil nodes
    connect_network(nodes)

    # Eclipse attack on Node 0 using all malicious nodes
    malicious_nodes = [n for n in nodes if n.malicious]
    eclipse_attack(nodes[0], malicious_nodes)

    trust_history = {str(n.node_id): [] for n in nodes}
    attack_step = 0

    for step in range(10):
        print(f"\n--- Step {step} ---")

        for node in nodes:
            node.broadcast_transaction()

        for node in nodes:
            if random.random() < 0.3:
                node.broadcast_block()

        gossip_phase(nodes)

        for n in nodes:
            trust_history[str(n.node_id)].append(n.final_trust)

        print_status(nodes)

    acc, fp = evaluate(nodes)

    print("\n--- Results ---")
    print("Detection Accuracy:", round(acc, 2))
    print("False Positives:", fp)

    plot_trust_evolution(trust_history, nodes, attack_step)


if __name__ == "__main__":
    run()