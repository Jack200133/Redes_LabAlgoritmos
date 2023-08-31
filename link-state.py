import heapq


class Link_State():
    def __init__(self):
        self.nombre = input("Ingresa el nombre del nodo.\n>> ")
        vecinos = input(
            "Ingresa los vecinos separados por \",\".\n>> ").split(",")
        pesos = input("Ingresa los pesos separados por \",\".\n>> ").split(",")
        self.tabla_enrutamiento = {}
        self.vecinos_pesos = list(zip(vecinos, pesos))
        print(f"Estos son los vecinos de {self.nombre}: ", self.vecinos_pesos)
        self.topologia = {
            'A': [('B', 4), ('C', 2)],
            'B': [('A', 4)],
            'C': [('C', 2)],
        }
        self.dijkstra()

    def camino(self, destination):
        path = [destination]
        while self.anterior[destination] is not None:
            destination = self.anterior[destination]
            path.insert(0, destination)
        return path

    def siguiente_nodo(self, destination):
        path = self.camino(destination)
        if len(path) > 1:
            return path[1]
        return path[0]

    def recibir_mensaje(self, emisor, receptor, mensaje):
        if self.nombre == receptor:
            print("Mensaje recibido: ", mensaje)
        else:
            print("De: ", emisor)
            print("Manda:", mensaje)
            print("El siguiente nodo en el camino es:",
                  self.siguiente_nodo(receptor))

    def dijkstra(self):
        self.distancias = {}
        self.anterior = {}
        self.fila = []

        for node in self.topologia:
            if node == self.nombre:
                self.distancias[node] = 0
                heapq.heappush(self.fila, (0, node))
            else:
                self.distancias[node] = float("inf")
                heapq.heappush(self.fila, (float("inf"), node))
            self.anterior[node] = None

        while self.fila:
            u = heapq.heappop(self.fila)
            u = u[1]
            for v in self.topologia[u]:
                alt = self.distancias[u] + v[1]
                if alt < self.distancias[v[0]]:
                    self.distancias[v[0]] = alt
                    self.anterior[v[0]] = u
                    for i in range(len(self.fila)):
                        if self.fila[i][1] == v[0]:
                            self.fila[i] = (alt, v[0])
                            heapq.heapify(self.fila)

        for node, anterior_node in self.anterior.items():
            if anterior_node is not None:
                path = self.camino(node)
                self.tabla_enrutamiento[node] = (path, self.distancias[node])


node = Link_State()
opcion = 0
while opcion != "3":
    print("\n")
    print("1. Enviar mensaje")
    print("2. Recibir mensaje")
    print("3. Salir")
    opcion = input(">> ")
    if opcion == "1":
        mensaje = input("Mensaje:\n>> ")
        destino = input("Destino:\n>> ")
        siguiente = node.siguiente_nodo(destino)
        print("mensaje: ", mensaje)
        print("siguiente nodo: ", siguiente)
    elif opcion == "2":
        mensaje = input(
            "Ingrese al emisor, receptor y mensaje separados por \",\"\n>> ")
        mensaje = mensaje.split(",")
        node.recibir_mensaje(mensaje[0], mensaje[1], mensaje[2])
