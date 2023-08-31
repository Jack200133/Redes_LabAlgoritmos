import heapq
import json


def load_json(path):
    print("Para cambiar la topoligia cambie el archivo 'topos.json'")
    try:
        with open(path, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("El archivo de topología no se encontró.")
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")


class DijkstraNode():
    
    def __init__(self):
        self.name = input("Ingresa el nombre del nodo: ")
        self.topology = load_json("topos.json")
        self.dijkstra()
    
    def dijkstra(self):
        self.distances = {}
        self.previous = {}
        self.queue = []
        
        for node in self.topology:
            if node == self.name:
                self.distances[node] = 0
                heapq.heappush(self.queue, (0, node))
            else:
                self.distances[node] = float("inf")
                heapq.heappush(self.queue, (float("inf"), node))
            self.previous[node] = None
        
        while self.queue:
            u = heapq.heappop(self.queue)
            u = u[1]
            for v, w in self.topology[u].items():
                alt = self.distances[u] + w
                if alt < self.distances[v]:
                    self.distances[v] = alt
                    self.previous[v] = u
                    for i in range(len(self.queue)):
                        if self.queue[i][1] == v:
                            self.queue[i] = (alt, v)
                            heapq.heapify(self.queue)
        
        self.create_routing_table()
    
    def create_routing_table(self):
        self.routing_table = {}
        for node, previous_node in self.previous.items():
            if previous_node is not None:
                path = self.get_path(node)
                self.routing_table[node] = (path, self.distances[node])

    def get_path(self, destination):
        path = [destination]
        while self.previous[destination] is not None:
            destination = self.previous[destination]
            path.insert(0, destination)
        return path

    def receive_message(self, emisor, receptor, mensaje):
        if receptor == self.name:
            print("El mensaje ha llegado al destino.")
            print(mensaje)
        else:
            siguiente = self.get_path(receptor)[1]
            print(f"Enviar mensaje a {siguiente}. Mensaje: {mensaje}\n")
            print(f"{emisor},{receptor},{mensaje}")
            

def optionHandler(opt):
    if opt == "1":
        msm = "Ingrese el mensaje de la forma 'destino,mensaje': "
        user_input = input(msm)
        user_input = user_input.split(",")
        node.receive_message(node.name, user_input[0], user_input[1])
        return True
    elif opt == "2":
        msm = "Ingrese el mensaje de la forma 'emisor,destino,mensaje': "
        mensaje = input(msm)
        mensaje = mensaje.split(",")
        mensaje = [x.strip() for x in mensaje]
        node.receive_message(mensaje[0], mensaje[1], mensaje[2])
        return True
    elif opt == "3":
        return False
    else:
        print("Opcion invalida.")
        return True


if __name__ == "__main__":
    node = DijkstraNode()
    bandera = True
    while bandera:
        print("--------------Menu--------------")
        print("1. Enviar mensaje")
        print("2. Recibir mensaje")
        print("3. Salir")
        opcion = input("Ingrese opcion: ")
        bandera = optionHandler(opcion)
        
