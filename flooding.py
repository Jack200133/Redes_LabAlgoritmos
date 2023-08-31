import json
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    # Funcion para agregar vecinos
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
    
    # Funcion para enviar mensaje (Dado que manejamos un arbol de conexiones,
    # de manera recursiva, enviamos los mensajes simulando el flooding)
    def send_message(self, message, target, seen=None, log=None):
        if not seen:
            seen = {self.name}
        if not log:
            log = []

        message['headers']['hop_count'] += 1

        # Por todos los vecinos del nodo enviamos el mensaje
        # tomando en cuenta no repetir un nodo
        for neighbor in self.neighbors:
            if neighbor.name not in seen:
                seen.add(neighbor.name)
                new_msg = message.copy()
                new_msg['headers'] = message['headers'].copy()
                new_msg['headers']['from'] = self.name
                new_msg['headers']['to'] = neighbor.name
                log.append(new_msg)
                neighbor.send_message(new_msg, target, seen, log)

        return log


def simulate_flooding():
    # Grafo
    A = Node('A')
    B = Node('B')
    C = Node('C')
    D = Node('D')
    E = Node('E')
    
    # Definimos las conexiones
    A.add_neighbor(B)
    A.add_neighbor(C)
    B.add_neighbor(A)
    C.add_neighbor(B)
    D.add_neighbor(C)
    D.add_neighbor(E)
    C.add_neighbor(B)
    B.add_neighbor(D)
    E.add_neighbor(D)

    # Mensaje Inicial
    message = {
        "type": "info",
        "headers": {
            "from": "A",
            "to": "E",
            "hop_count": 0
        },
        "payload": "Hello from A to E!"
    }

    # Iniciar el flooding en A hacia E
    target = 'E'
    logs = A.send_message(message, target)

    # Guardar el log en un JSON
    with open('flooding_log.json', 'w') as f:
        json.dump(logs, f, indent=4)

    # imprimit el log
    for log_entry in logs:
        print(log_entry)

    # Visualizar el grafo
    G = nx.Graph()
    nodes = [A, B, C, D, E]
    for node in nodes:
        G.add_node(node.name)
        for neighbor in node.neighbors:
            G.add_edge(node.name, neighbor.name)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)

    edge_labels = dict(((u, v), "{} -> {}".format(u, v)) for u, v in G.edges())
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()


if __name__ == "__main__":
    simulate_flooding()
