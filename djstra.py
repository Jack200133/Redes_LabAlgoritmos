import json
import heapq

def dijkstra(graph, start):
    # Inicialización
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

def main():
    # Suponiendo que el grafo está representado como un diccionario
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }

    start_node = 'A'
    distances = dijkstra(graph, start_node)

    # Crear y enviar paquetes JSON
    for end_node, distance in distances.items():
        packet = {
            "type": "info",
            "headers": {
                "from": start_node,
                "to": end_node,
                "hop_count": distance
            },
            "payload": "Distancia desde {} a {}: {}".format(start_node, end_node, distance)
        }
        print(json.dumps(packet, indent=4))

if __name__ == "__main__":
    main()
