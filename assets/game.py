import random
# import threading

from .constants import *
from assets.board import Board
from assets.model import Model

class Game:
    def __init__(self, type=str, player_1=object, player_2=object, starting_player=None, board=None, model=None) -> None:
        self.type = type
        self.player_1 = player_1
        self.player_2 = player_2
        self.starting_player = WHO_STARTS_GAME if starting_player is None else starting_player
        self.board = Board(player_1=self.player_1, player_2=self.player_2) if board is None else board
        self.model = Model() if model is None else model
        
        # Define starting player
        if self.starting_player == 'Random':
            self.active_player = random.choice([self.player_1, self.player_1])
        elif self.starting_player == 'Player 1':
            self.active_player = self.player_1
        elif self.starting_player == 'Player 2':
            self.active_player = self.player_2
        else:
            raise ValueError('Invalid starting player')
        
        # Define passive player
        if self.active_player == self.player_1:
            self.passive_player = self.player_2
        else:
            self.passive_player = self.player_1

        self.turn = 0
        self.move = 0
        self.winner = None


    def execute_turn(self):
        # Info about turn
        print(f"TURN BEGINS - {self.active_player.name}")
        print(f"turn: {self.turn} move: {self.move}")
        # Validate board
        if not self.board.is_board_valid(): 
            print(f"WARNING: Board state is not valid")
        # Several moves can be made in one turn
        while True:
            # Find legal moves
            self.legal_moves = self.board.get_legal_moves(self.active_player)
            if self.turn == 1 and self.move == 0: # Allow to rotate board after first turn
                self.legal_moves.append(0)

            # Check if legal moves exist
            if self.legal_moves == []: 
                print(f"\nNo legal moves for {self.active_player.name}")
                return True

            # Check if game has winner
            if self.board.check_winner() != None:
                return True

            # Draw board
            self.board.draw_board() 

            # Select pit
            pit = self.select_pit(self.legal_moves)

            # NB! Fix bug with not showing board before turn is made. This is actually threading bug somehow with sleep
            # Execute turn
            if pit == 0: # Special case
                self.board.rotate_board() 
                break
            elif not self.board.apply_move(self.active_player,pit): # If no additional move
                break
            else: # Additional move
                self.move += 1
                print(f"\nADDITIONAL MOVE GRANTED, move {self.move}")

        # Change turn
        self.change_turn()


    def select_pit(self, legal_moves=None):
        if self.active_player.type == "Human":
            while(True):
                pit = None
                try:
                    print("\nPlease input pit:", end = " ")
                    pit = int(input())
                except ValueError:
                    pass

                if pit in legal_moves:
                    return pit
                else:
                    print('Selected pit is not a legal move')
                    print("Please input a number in " + str(legal_moves))

        else: # Computer
            if RANDOM_AI:
                pit = random.choice(legal_moves)
                print("Computer chooses pit:" + str(pit))
                return pit
            else:
                can_rotate = 0 in legal_moves
                can_opponent_rotate = self.turn == 0
                pit, value = self.model.best_turn(self.board, self.active_player, self.passive_player, can_rotate, can_opponent_rotate)
                print("\nComputer evaluates board to " + str(value))
                print("Computer chooses pit:" + str(pit))
                return pit

    def change_turn(self):
        if self.active_player == self.player_1:
            self.active_player, self.passive_player = self.player_2, self.player_1
        else:
            self.active_player, self.passive_player = self.player_1, self.player_2
        self.turn += 1
        self.move = 0
        print("-" * 20)
