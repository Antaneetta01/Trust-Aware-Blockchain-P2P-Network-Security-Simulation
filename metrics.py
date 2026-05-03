def evaluate(nodes):
    actual_malicious = [n for n in nodes if n.malicious]
    detected_malicious = [
        n for n in nodes
        if n.malicious and n.get_status() == "Malicious"
    ]

    false_positive = sum(
        1 for n in nodes
        if not n.malicious and n.get_status() == "Malicious"
    )

    accuracy = len(detected_malicious) / len(actual_malicious) if actual_malicious else 1

    return accuracy, false_positive