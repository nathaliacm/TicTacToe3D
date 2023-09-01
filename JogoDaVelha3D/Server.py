import socket
import threading
import json

class TicTacToeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(2) 

        self.clients = []
        self.global_board_states = [[["" for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.lock = threading.Lock()

    def handle_client(self, client_socket, client_address):
        try:
            self.clients.append(client_socket)
            print(f"Nova conexão de {client_address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                with self.lock:
                    received_board = json.loads(data.decode())
                    self.global_board_states = received_board
                    self.current_player = "O" if self.current_player == "X" else "X"
                    for client in self.clients:
                        client.sendall(data)
        except:
            pass
        finally:
            client_socket.close()
            self.clients.remove(client_socket)
            print(f"Conexão de {client_address} encerrada")


    def run(self):
        while len(self.clients) < 2:
            client_socket, client_address = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

        print("Duas conexões ativas.")

if __name__ == "__main__":
    server = TicTacToeServer("127.0.0.1", 12345)
    print("Aguardando conexões...")
    server.run()
