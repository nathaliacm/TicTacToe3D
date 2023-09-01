import socket
import json
import pygame
from TicTacToeView import TicTacToeView

class TicTacToeClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        
        pygame.init()
        self.view = TicTacToeView()
        self.clock = pygame.time.Clock()
        self.view.run()  
        self.server_data = None  

    def receive_data(self):
        while True:
            data = self.client.recv(1024)
            if not data:
                break
            self.server_data = json.loads(data.decode())

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.close()
                    pygame.quit()
                    running = False

            self.send_data()
            self.receive_data()

            self.view.update_board(self.server_data)
            self.view.update_screen()

            self.clock.tick(30) 


    def send_data(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.close()
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.view.is_my_turn():
                        cell_row, cell_col = self.view.get_cell_index(*pygame.mouse.get_pos())
                        if self.view.board_states[cell_row][cell_col] == "":
                            self.view.handle_mouse_click(0, cell_row, cell_col)
                            self.send_board()  
            self.clock.tick(30)  
            self.send_board()  

    def send_board(self):
        board_data = json.dumps(self.view.board_states)
        self.client.sendall(board_data.encode())

if __name__ == "__main__":
    client = TicTacToeClient("127.0.0.1", 12345)
    client.run()
