import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets = []
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print("Servidor aguardando conexões...")

        while len(self.client_sockets) < 2:
            client_socket, _ = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print(f"Cliente conectado: {client_socket.getpeername()}")

            if len(self.client_sockets) == 2:
                threading.Thread(target=self.handle_clients).start()

    def handle_clients(self):
        print("Dois clientes conectados. Iniciando troca de mensagens...")
        client1, client2 = self.client_sockets

        def forward_messages(from_client, to_client):
            while True:
                message = from_client.recv(1024)
                if not message:
                    break
                to_client.send(message)

        thread1 = threading.Thread(target=forward_messages, args=(client1, client2))
        thread2 = threading.Thread(target=forward_messages, args=(client2, client1))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        print("Conexão encerrada.")
        self.server_socket.close()

if __name__ == "__main__":
    server = Server('127.0.0.1', 12345)
    server.start()
