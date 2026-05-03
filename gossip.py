def gossip_phase(nodes):
    for node in nodes:
        for peer in node.peers:
            peer.receive_gossip(node.share_gossip(), node)

    for node in nodes:
        node.update_global_trust()

    for node in nodes:
        node.update_final_trust()