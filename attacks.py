from node import Node


def sybil_attack(nodes, num):
    print("\n[SYBIL ATTACK]")
    for i in range(num):
        fake = Node(f"sybil_{i}")
        fake.malicious = True
        nodes.append(fake)


def collusion_attack(nodes, ids):
    print("\n[COLLUSION ATTACK]")
    for n in nodes:
        if n.node_id in ids:
            n.malicious = True


def eclipse_attack(target, malicious_nodes):
    print(f"\n[ECLIPSE ATTACK on Node {target.node_id}]")

    # Target node is surrounded by malicious peers
    target.peers = malicious_nodes
    target.eclipsed = True

    # Malicious nodes also connect back to the target
    for attacker in malicious_nodes:
        if target not in attacker.peers:
            attacker.peers.append(target)