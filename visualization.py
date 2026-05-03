import matplotlib.pyplot as plt

def plot_trust_evolution(history, nodes, attack_step=None):
    plt.figure(figsize=(10, 6))

    for node_id, values in history.items():
        node = next((n for n in nodes if str(n.node_id) == str(node_id)), None)

        if node and node.malicious:
            plt.plot(values, linestyle='--', label=f"{node_id} (Malicious)")
        else:
            plt.plot(values, label=f"{node_id}")

    if attack_step is not None:
        plt.axvline(x=attack_step, linestyle=':', label="Attack Start")

    plt.xlabel("Time Step")
    plt.ylabel("Trust Score")
    plt.title("Trust Evolution Under Network Attacks")

    plt.legend()
    plt.grid()
    plt.show()