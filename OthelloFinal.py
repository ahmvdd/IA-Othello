import random 
import copy



# Object used to create new boards


class Board:
    def __init__(self, size):
        self.size = size
        self.board = []

    # Used to fill the "board" property with a list with a length equal to the "size" property
    def create_board(self):
        for y_pos in range(self.size):
            for x_pos in range(self.size):
                #  Create a Tile instance
                #  Gives it the coordinates (depending on x_pos and y_pos)
                #  Add it to the board property
                if x_pos != 0 and x_pos != 7 and y_pos != 0 and y_pos != 7:
                    self.board.append(Tile(x_pos, y_pos, "🟩", "🟩"))
                else:
                    self.board.append(Tile(x_pos, y_pos, "X", "🟩"))
        self.place_initial_pawns()

    #  This will print the game board, depending on the data_type
    #  Data types are "Coordinates", "Type" and "Content"
    def draw_board(self, data_type):
        display_board = []
        line_breaker = 0
        print([0, ' 0', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7'])
        for board_index in self.board:
            if (board_index.x_pos == 0):
                display_board.append(board_index.y_pos)
            if data_type == "Coordinates":
                display_board.append([board_index.x_pos, board_index.y_pos])
            elif data_type == "Type":
                display_board.append(board_index.type)
            else:
                display_board.append(board_index.content)
            line_breaker += 1
            if line_breaker > 7:
                print(display_board)
                line_breaker = 0
                display_board = []
        print("\n")

    # Place the 4 initial pawns at the center of the board (2 white and 2 black)
    def place_initial_pawns(self):
        #  We pick the 4 central tiles
        #  And place 2 black pawns and 2 white pawns
        self.board[27].content = "⚪"
        self.board[28].content = "⚫"
        self.board[35].content = "⚫"
        self.board[36].content = "⚪"

    # Check if the position in inside the board
    # Return true or false depending if it is inside or not
    def is_on_board(self, x_pos, y_pos):
        if x_pos < 0 or x_pos > 7 or y_pos < 0 or y_pos > 7:
            return False
        else:
            return True

    # Check if the tile is an empty tile ("🟩")
    # Return true or false depending if it is empty or not
    def is_tile_empty(self, x_pos, y_pos):
        if self.board[(x_pos) + y_pos * 8].content == "🟩":
            return True
        else:
            return False

    # Takes a position (x_pos, y_pos) and a color
    # Try to simulate the move
    # Returns either false if the move is not valid
    # Or returns which pawns will change color if true
    # The returned list will contain [numbers_of_pawns_to_change, [direction_x, direction_y]]
    def is_legal_move(self, x_pos, y_pos, color):

        # North / Nort-East / East / South-East / South / South-West / West / North-West
        directions = [
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
            [-1, -1],
        ]

        # Opposite of the color of the placed pawn
        if color == "⚪":
            awaited_color = "⚫"
        else:
            awaited_color = "⚪"

        current_x_pos = x_pos
        current_y_pos = y_pos
        is_legal = False
        # [number_of_tile_to_flip, direction]
        # Si on a un pion noir placé en 2,3, on veut:
        # [[1, [1, 0]]
        tiles_to_flip = []

        if (not self.is_tile_empty(current_x_pos, current_y_pos) or not self.is_on_board(current_x_pos, current_y_pos)):
            return False

        # Check for every direction
        for current_dir in directions:
            number_of_tiles_to_flip = 1
            # Get your original coordinates + the direction modifier
            current_x_pos = x_pos + current_dir[0]
            current_y_pos = y_pos + current_dir[1]
            # Check if the new position is on the board and empty
            if self.is_on_board(current_x_pos, current_y_pos):
                #  Get the tile informations
                current_index = self.board[current_x_pos + current_y_pos * 8]
                # If the tile contains a pawn of the opposite color, continue on the line
                while current_index.content == awaited_color:
                    current_x_pos += current_dir[0]
                    current_y_pos += current_dir[1]
                    if self.is_on_board(current_x_pos, current_y_pos):
                        current_index = self.board[current_x_pos +
                                                   current_y_pos * 8]
                        # If the line ends with a pawn of your color, then the move is legal
                        if current_index.content == color:
                            is_legal = True
                            tiles_to_flip.append(
                                [number_of_tiles_to_flip, current_dir])
                            break
                    else:
                        break
                    number_of_tiles_to_flip += 1

        if is_legal:
            return tiles_to_flip
        else:
            return False

    # Takes a position (x_pos, y_pos), an array with a number of tiles to flip and a direction, and a color
    # The array should be obtained with the "is_legal_move" function
    # Doesn't return anything, but will change the color of the tiles selected by "tiles_to_flip"
    def flip_tiles(self, x_pos, y_pos, tiles_to_flip, color):
        # x_pos and y_pos = new pawn position
        # tiles_to_flip = list containing the number of pawn to flip and a direction
        # ex: [
        # [1, [1, 0]],
        # ] means we're changing 1 pawn to the right
        # color = the new color of the pawns to flip
        for current_dir in tiles_to_flip:
            current_x_pos = x_pos + current_dir[1][0]
            current_y_pos = y_pos + current_dir[1][1]
            for nb_tile in range(current_dir[0]):
                current_index = self.board[current_x_pos + current_y_pos * 8]
                current_index.content = color
                current_x_pos += current_dir[1][0]
                current_y_pos += current_dir[1][1]

# Used to create each tile of your board
# Contains a position (x, y), a type to check if it's a boder tile or not, and a content to check if there is a pawn inside the tile


class Tile:
    #   Type is used to check if its an "🟩" empty tile or a "X" border tile
    #   Content is used to check if a pawn is placed o (Empty), B (Black), W (White)
    def __init__(self, x_pos, y_pos, type, content):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type
        self.content = content

# Used to create new ruleset
# Contains the score, the active player, the game_over check and functions allowing to interact with the game


class Game:
    def __init__(self):
        self.score_black = 2
        self.score_white = 2
        self.active_player = "⚫"
        self.is_game_over = False
        self.winner = "Noone"
        self.turn = 0

    # Place a pawn on the board (checks if the move is legal before placing it)
    # It takes a position (x, y), a Board object instance and a color
    # The function will automatically check if the move is valid or not
    def place_pawn(self, x_pos, y_pos, board_instance, color):
        if not board_instance.is_on_board(x_pos, y_pos):
            print("Coordinates outside the board")
        else:
            if board_instance.board[(x_pos) + y_pos * 8].content == "🟩":
                tiles_to_flip = board_instance.is_legal_move(
                    x_pos, y_pos, color)
                if not tiles_to_flip:
                    print("Invalid move")
                else:
                    board_instance.board[(x_pos) + y_pos * 8].content = color
                    board_instance.flip_tiles(
                        x_pos, y_pos, tiles_to_flip, color)
                    print(f"Pion placé en {x_pos}, {y_pos}")
                    self.update_score(board_instance)
                    self.change_active_player()
                    self.check_for_valid_moves(board_instance)
                    board_instance.draw_board("Content")
            else:
                print("There is already a pawn here")

    # Change the active player color from black to white or white to black
    def change_active_player(self):
        # Prend self.active_player et change la couleur du joueur actif
        if self.active_player == "⚫":
            self.active_player = "⚪"
            print("C'est au tour du joueur blanc")
        else:
            self.active_player = "⚫"
            print("C'est au tour du joueur noir")
            
        self.turn += 1

    # Update the players score after a successful move
    def update_score(self, board_instance):
        # Count all the black & white pawns, and update the scores
        w_score = 0
        b_score = 0
        for tile_index in board_instance.board:
            if tile_index.content == "⚪":
                w_score += 1
            elif tile_index.content == "⚫":
                b_score += 1
        self.score_black = b_score
        self.score_white = w_score

    # Check for a valid move, and end the game if there is none for the current player
    def check_for_valid_moves(self, board_instance):
        is_game_over = True
        first_player_can_play = False

        # Check if the current player can play
        for tile_index in board_instance.board:
            move_to_check = board_instance.is_legal_move(
                tile_index.x_pos, tile_index.y_pos, self.active_player)
            if move_to_check != False:
                first_player_can_play = True
                is_game_over = False

        # If not, check for the other player and skip the first player's turn
        if not first_player_can_play:
            self.change_active_player()
            for tile_index in board_instance.board:
                move_to_check = board_instance.is_legal_move(tile_index.x_pos, tile_index.y_pos, self.active_player)
                if move_to_check != False:
                  is_game_over = False  

        # If neither can play, end the game
        if is_game_over:
            self.check_for_winner()
            self.is_game_over = True

    # Compare the score, and print the winner's color
    def check_for_winner(self):
        print("Partie terminée !")
        print("Le joueur noir a: " + str(self.score_black) + " points")
        print("Le joueur white a: " + str(self.score_white) + " points")
        if (self.score_black > self.score_white):
            print("Le joueur noir a gagné !")
            self.winner = "⚫"
        elif (self.score_white > self.score_black):
            print("Le joueur blanc a gagné !")
            self.winner = "⚪"
        else:
            print("Égalité !")



#kjvdfkjvdfvjdfv


# NOUVELLE VERSION //////////////////////////////////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class Bot:
    def __init__(self):
        self.name = "Strategic Bot"
        self.corner_matrix = [
            1000, -10, -10, -10, -10, -10, -10, 1000,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            1000, -10, -10, -10, -10, -10, -10, 1000
        ]

    def evaluate_move(self, board, x, y, player):
        """Évalue un coup à une position donnée."""
        # Définir une matrice pour prioriser les coins
        corner_matrix = [
            1000, -10, -10, -10, -10, -10, -10, 1000,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            -10, -5, -5, -5, -5, -5, -5, -10,
            1000, -10, -10, -10, -10, -10, -10, 1000
        ]
        # Retourne la valeur de la position selon la matrice
        return corner_matrix[x][y]  # Utilise la matrice de coins

    def evaluate_board(self, board, player):
        """Évalue le plateau en fonction des positions des pions."""
        score = 0
        for tile in board.board:
            if tile.content == player:
                score += self.evaluate_move(board, tile.x_pos, tile.y_pos, player)
            elif tile.content == self.get_opponent_color(player):
                score -= self.evaluate_move(board, tile.x_pos, tile.y_pos, player)
        return score

    def get_valid_moves(self, board, player):
        """Récupère les coups valides pour un joueur donné."""
        valid_moves = []
        max_points = float('-inf')
        compteur = 0
        for tile in board.board:
            points = 0
            current_move = board.is_legal_move(tile.x_pos, tile.y_pos, player)
            if current_move != False:
                for i in current_move:
                    points += i[0]
                points += self.corner_matrix[compteur]

                if points > max_points:
                    max_points = points
                    valid_moves = [[tile.x_pos, tile.y_pos]]
                elif points == max_points:
                    valid_moves.append((tile.x_pos, tile.y_pos))
            compteur += 1
                
        return valid_moves

    def simulate_move(self, board, x, y, player):
        """Simule un coup en plaçant un pion sur le plateau."""
        board_copy = copy.deepcopy(board)
        tiles_to_flip = board_copy.is_legal_move(x, y, player)
        if tiles_to_flip:
            board_copy.board[x + y * 8].content = player
            board_copy.flip_tiles(x, y, tiles_to_flip, player)
        return board_copy

    def get_opponent_color(self, player):
        """Retourne la couleur de l'adversaire."""
        return "⚪" if player == "⚫" else "⚫"

    def check_valid_moves(self, board, active_player):
        """Sélectionne le meilleur coup en utilisant l'évaluation des coins."""
        valid_moves = self.get_valid_moves(board, active_player)

        return random.choice(valid_moves)



#dhvbdfhv




# Create a new board & a new game instances
othello_board = Board(8)
othello_game = Game()

# Fill the board with tiles
othello_board.create_board()

# Draw the board
othello_board.draw_board("Content")

# Create 2 bots
myBot = Bot()
otherBot = Bot()




while not othello_game.is_game_over:
    # First player / bot logic goes here
    if (othello_game.active_player == "⚫"):
        move_coordinates = myBot.check_valid_moves(othello_board, othello_game.active_player)
        othello_game.place_pawn(
            move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)
        
    # Second player / bot logic goes here
    else:
        move_coordinates = myBot.check_valid_moves(othello_board, othello_game.active_player)
        if move_coordinates:
            othello_game.place_pawn(
                move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)

    








# version 1/////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



# class Bot:
#     def __init__(self):
#         self.name = "Strategic Bot"

#     # Matrice de récompense pour évaluer les positions sur le plateau
#     reward_matrix = [
#         [15, -5,  3,  5,  5,  3, -5, 15],   
#         [-5,  2,  3,  4,  4,  3, -5, -5],   
#         [ 3,  3,  4,  5,  5,  4,  3,  3],   
#         [ 5,  4,  5,  6,  6,  5,  4,  5],   
#         [ 5,  4,  5,  6,  6,  5,  4,  5],  
#         [ 3,  3,  4,  5,  5,  4,  3,  3],   
#         [-5, -5,  3,  4,  4,  3, -5, -5],  
#         [15, -5,  3,  5,  5,  3, -5, 15],  
#     ]
    
#     def evaluate_move(self, board, x, y, player):
#         """Évalue un coup à une position donnée avec la matrice de récompense."""
#         return self.reward_matrix[y][x]

#     def minimax(self, board, depth, is_maximizing_player, alpha, beta, player):
#         """Minimax avec élagage Alpha-Beta"""
#         valid_moves = self.get_valid_moves(board, player)
        
#         if depth == 0 or not valid_moves:
#             return self.evaluate_board(board, player)

#         if is_maximizing_player:
#             max_eval = float('-inf')
#             for move in valid_moves:
#                 board_copy = self.simulate_move(board, move[0], move[1], player)
#                 eval = self.minimax(board_copy, depth-1, False, alpha, beta, self.get_opponent_color(player))
#                 max_eval = max(max_eval, eval)
#                 alpha = max(alpha, eval)
#                 if beta <= alpha:
#                     break
#             return max_eval
#         else:
#             min_eval = float('inf')
#             for move in valid_moves:
#                 board_copy = self.simulate_move(board, move[0], move[1], player)
#                 eval = self.minimax(board_copy, depth-1, True, alpha, beta, self.get_opponent_color(player))
#                 min_eval = min(min_eval, eval)
#                 beta = min(beta, eval)
#                 if beta <= alpha:
#                     break
#             return min_eval

#     def evaluate_board(self, board, player):
#         """Évalue le plateau en fonction des positions des pions."""
#         score = 0
#         for tile in board.board:
#             if tile.content == player:
#                 score += self.evaluate_move(board, tile.x_pos, tile.y_pos, player)
#         return score

#     def get_valid_moves(self, board, player):
#         """Récupère les coups valides pour un joueur donné."""
#         valid_moves = []
#         for tile in board.board:
#             if tile.content == "🟩":
#                 if board.is_legal_move(tile.x_pos, tile.y_pos, player):
#                     valid_moves.append((tile.x_pos, tile.y_pos))
#         return valid_moves

#     def simulate_move(self, board, x, y, player):
#         """Simule un coup en plaçant un pion sur le plateau."""
#         board_copy = copy.deepcopy(board)
#         tiles_to_flip = board_copy.is_legal_move(x, y, player)
#         if tiles_to_flip:
#             board_copy.board[x + y * 8].content = player
#             board_copy.flip_tiles(x, y, tiles_to_flip, player)
#         return board_copy

#     def get_opponent_color(self, player):
#         """Retourne la couleur de l'adversaire."""
#         return "⚪" if player == "⚫" else "⚫"

#     def check_valid_moves(self, board, active_player):
#         """Sélectionne le meilleur coup en utilisant l'algorithme Minimax."""
#         valid_moves = self.get_valid_moves(board, active_player)
#         best_move = None
#         best_value = float('-inf')

#         # Recherche du meilleur coup à une profondeur maximale

        
#         for move in valid_moves:
#             eval = self.minimax(board, 3, True, float('-inf'), float('inf'), active_player)
#             if eval > best_value:
#                 best_value = eval
#                 best_move = move



#         #Le contrôle des coins est crucial dans Othello


#         def prioritize_corners(self, move, player):
#             corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
#             if move in corners:
#                 return 1000  # Un score très élevé pour les coins
#             return 0  # Sinon, un score de 0
            

#         return best_move


# code final 

# import copy

# class Bot:
#     def __init__(self):
#         self.name = "Strategic Bot"

#     def evaluate_move(self, board, x, y, player):
#         """Évalue un coup à une position donnée."""
#         # Définir une matrice pour prioriser les coins
#         corner_matrix = [
#             [1000, -10, -10, -10, -10, -10, -10, 1000],
#             [-10, -5, -5, -5, -5, -5, -5, -10],
#             [-10, -5, -5, -5, -5, -5, -5, -10],
#             [-10, -5, -5, -5, -5, -5, -5, -10],
#             [-10, -5, -5, -5, -5, -5, -5, -10],
#             [-10, -5, -5, -5, -5, -5, -5, -10],
#             [-10, -5, -5, -5, -5, -5, -5, -10],
#             [1000, -10, -10, -10, -10, -10, -10, 1000]
#         ]
#         # Retourne la valeur de la position selon la matrice
#         return corner_matrix[x][y]  # Utilise la matrice de coins

#     def evaluate_board(self, board, player):
#         """Évalue le plateau en fonction des positions des pions."""
#         score = 0
#         for tile in board.board:
#             if tile.content == player:
#                 score += self.evaluate_move(board, tile.x_pos, tile.y_pos, player)
#             elif tile.content == self.get_opponent_color(player):
#                 score -= self.evaluate_move(board, tile.x_pos, tile.y_pos, player)
#         return score

#     def get_valid_moves(self, board, player):
#         """Récupère les coups valides pour un joueur donné."""
#         valid_moves = []
#         for tile in board.board:
#             if tile.content == "🟩":
#                 if board.is_legal_move(tile.x_pos, tile.y_pos, player):
#                     valid_moves.append((tile.x_pos, tile.y_pos))
#         return valid_moves

#     def simulate_move(self, board, x, y, player):
#         """Simule un coup en plaçant un pion sur le plateau."""
#         board_copy = copy.deepcopy(board)
#         tiles_to_flip = board_copy.is_legal_move(x, y, player)
#         if tiles_to_flip:
#             board_copy.board[x + y * 8].content = player
#             board_copy.flip_tiles(x, y, tiles_to_flip, player)
#         return board_copy

#     def get_opponent_color(self, player):
#         """Retourne la couleur de l'adversaire."""
#         return "⚪" if player == "⚫" else "⚫"

#     def check_valid_moves(self, board, active_player):
#         """Sélectionne le meilleur coup en utilisant l'évaluation des coins."""
#         valid_moves = self.get_valid_moves(board, active_player)
#         best_move = None
#         best_value = float('-inf')

#         # Recherche du meilleur coup basé sur la priorité des coins
#         for move in valid_moves:
#             eval = self.evaluate_board(board, active_player)  # Utilise evaluate_board pour évaluer
#             if eval > best_value:
#                 best_value = eval
#                 best_move = move

#         return best_move
