import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(1024)
            if not message:
                break
            print(" - ", message.decode('utf-8'))

    def send_message(self, message):
        self.client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    client = Client('127.0.0.1', 12345)
    client.connect()

    while True:
        message = input()
        client.send_message(message)
