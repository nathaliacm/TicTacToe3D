import pygame

class TicTacToeLogic:
    # Verifica vitória em tabuleiros individuais
    @staticmethod
    def check_board_winner(board):
        for row in board:
            first_symbol = row[0]
            if first_symbol != "" and all(cell == first_symbol for cell in row):
                return first_symbol
        
        for col in range(3):
            first_symbol = board[0][col]
            if first_symbol != "" and all(board[row][col] == first_symbol for row in range(3)):
                return first_symbol
        
        if board[0][0] != "" and all(board[i][i] == board[0][0] for i in range(3)):
            return board[0][0]
        
        if board[0][2] != "" and all(board[i][2 - i] == board[0][2] for i in range(3)):
            return board[0][2]
        
        return None

    # Verifica vitória nas camadas diagonais tridimensionais
    @staticmethod
    def check_diagonal_3d_winner(board):
        for layer in range(3):
            # Verifica a diagonal principal da camada diagonal
            diagonal_main = [board[i][i][layer] for i in range(3)]
            if all(cell == diagonal_main[0] and cell != "" for cell in diagonal_main):
                return diagonal_main[0]

            # Verifica a diagonal secundária da camada diagonal
            diagonal_secondary = [board[i][2 - i][layer] for i in range(3)]
            if all(cell == diagonal_secondary[0] and cell != "" for cell in diagonal_secondary):
                return diagonal_secondary[0]

        for layer in range(3):
            # Verifica a diagonal principal ao longo dos planos
            diagonal_plane_main = [board[i][i][i] for i in range(3)]
            if all(cell == diagonal_plane_main[0] and cell != "" for cell in diagonal_plane_main):
                return diagonal_plane_main[0]
            
            # Verifica a diagonal secundária ao longo dos planos
            diagonal_plane_secondary = [board[i][2 - i][i] for i in range(3)]
            if all(cell == diagonal_plane_secondary[0] and cell != "" for cell in diagonal_plane_secondary):
                return diagonal_plane_secondary[0]

        return None

    # Verifica as colunas entre tabuleiros
    @staticmethod
    def check_column_winner(board, col):
        for layer in range(3):
            if all(board[i][col][layer] == board[0][col][layer] and board[i][col][layer] != "" for i in range(3)):
                return board[0][col][layer]
        return None

    @staticmethod
    def check_winner(board):
        for i, tab in enumerate(board):
            board_winner = TicTacToeLogic.check_board_winner(tab)
            if board_winner:
                print(f"Jogador '{board_winner}' venceu no tabuleiro {i + 1}!")
                return board_winner
        
        for col in range(3):
            diagonal_3d_winner = TicTacToeLogic.check_diagonal_3d_winner(board)
            if diagonal_3d_winner:
                print(f"Jogador '{diagonal_3d_winner}' venceu nas camadas diagonais entre tabuleiros!")
                return diagonal_3d_winner

        for col in range(3):
            column_winner = TicTacToeLogic.check_column_winner(board, col)
            if column_winner:
                print(f"Jogador '{column_winner}' venceu nas colunas entre tabuleiros!")
                return column_winner

        return None

class TicTacToeView:
    def __init__(self):
        self.resigned = False
        self.screen_width = 800
        self.screen_height = 400
        self.board_size = 200
        self.border_color = (70, 70, 70)
        self.line_color = (0, 180, 0)
        self.x_color = (0, 0, 180)
        self.line_thickness = 5

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.board_matrix = [[["" for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.board_positions = [(50, 100), (300, 100), (550, 100)]
        self.board_states = [[["" for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

        self.game_logic = TicTacToeLogic()

    def draw_board(self, x, y):
        pygame.draw.rect(self.screen, self.border_color, (x, y, self.board_size, self.board_size), 6)
        for row in range(3):
            for col in range(3):
                pygame.draw.rect(self.screen, self.border_color,
                                 (x + col * (self.board_size // 3), y + row * (self.board_size // 3),
                                  self.board_size // 3, self.board_size // 3), 3)
        self.draw_resign_button() 

    def get_cell_index(self, x, y, board_x, board_y):
        relative_x = x - board_x
        relative_y = y - board_y
        cell_row = relative_y // (self.board_size // 3)
        cell_col = relative_x // (self.board_size // 3)
        return cell_row, cell_col
    
    def draw_resign_button(self):
        font = pygame.font.Font(None, 24)
        resign_text = font.render("Desistir", True, (200, 0, 20))
        resign_rect = resign_text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))

        button_width = 100
        button_height = 30
        button_rect = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            self.screen_height - 45,
            button_width,
            button_height
        )

        pygame.draw.rect(self.screen, (200, 200, 200), button_rect, border_radius=5)
        self.screen.blit(resign_text, resign_rect)

    def handle_mouse_click(self, board_index, cell_row, cell_col):
        if self.board_states[board_index][cell_row][cell_col] == "":
            # print(f"Tabuleiro {board_index+1}, posição ({cell_row}, {cell_col}) atualizada com '{self.current_player}'")
            self.board_states[board_index][cell_row][cell_col] = self.current_player
            
            self.board_matrix[board_index][cell_row][cell_col] = self.current_player
            
            # print("Estado dos tabuleiros após a jogada:")
            # for i, tab in enumerate(self.board_states):
            #     # print(f"Tabuleiro {i + 1}:")
            #     for row in tab:
            #         # print(row)

            winner = self.game_logic.check_winner(self.board_matrix)
            if winner:
                print(f"Jogador {winner} venceu!")
                self.show_victory_popup(winner)
                # self.running = False
            else:
                self.current_player = "X" if self.current_player == "O" else "O"

    def draw_symbols(self):
        for i, (board_x, board_y) in enumerate(self.board_positions):
            for row in range(3):
                for col in range(3):
                    symbol = self.board_states[i][row][col]
                    cell_x = board_x + col * (self.board_size // 3) 
                    cell_y = board_y + row * (self.board_size // 3)
                    if symbol == "X":
                        line_length = self.board_size // 3 - 20
                        x_start = cell_x + (self.board_size // 6) - (line_length // 2)
                        y_start = cell_y + (self.board_size // 6) - (line_length // 2)
                        x_end = x_start + line_length
                        y_end = y_start + line_length
                        pygame.draw.line(self.screen, self.x_color, (x_start, y_start), (x_end, y_end), 6)
                        pygame.draw.line(self.screen, self.x_color, (x_end, y_start), (x_start, y_end), 6)
                    elif symbol == "O":
                        circle_radius = (self.board_size // 6) - 8
                        pygame.draw.circle(self.screen, self.line_color, (cell_x + self.board_size // 6, cell_y + self.board_size // 6), circle_radius, self.line_thickness)

    def update_screen(self):
        self.screen.fill((255, 255, 255))

        for i, (board_x, board_y) in enumerate(self.board_positions):
            self.draw_board(board_x, board_y)
            self.draw_symbols()

        pygame.display.flip()

    def update_board(self, server_data):
        self.board_states = server_data
        self.update_screen()

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = event.pos
                    for i, (board_x, board_y) in enumerate(self.board_positions):
                        if board_x <= mouseX < board_x + self.board_size and board_y <= mouseY < board_y + self.board_size:
                            cell_row, cell_col = self.get_cell_index(mouseX, mouseY, board_x, board_y)
                            self.handle_mouse_click(i, cell_row, cell_col)
                    if self.screen_width // 2 - 50 <= mouseX < self.screen_width // 2 + 50 and self.screen_height - 45 <= mouseY < self.screen_height - 15:
                        self.resigned = True
                        self.running = False 

            self.update_screen()

        if self.resigned:
            print("Jogador desistiu!")
        pygame.quit()
    
    def reset_game(self):
        self.board_states = [[["" for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.board_matrix = [[["" for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.resigned = False

    def show_victory_popup(self, winner):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Jogador {winner} venceu!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width // 2, 20))

        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (255, 255, 255, 128), overlay.get_rect())
        self.screen.blit(overlay, (0, 0))

        self.draw_symbols() 
        self.screen.blit(text, text_rect)
        pygame.display.update()

        pygame.time.delay(3000)
        self.reset_game()

if __name__ == "__main__":
    view = TicTacToeView()
    view.run()
