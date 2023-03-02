import random
# import threading

from .constants import *
from assets.board import Board
from assets.model import Model
# from assets.game import Player

class Game:
    def __init__(self, type=str, starting_player=None, board=None, model=None) -> None:
        self.type = type
        self.starting_player = WHO_STARTS_GAME if starting_player is None else starting_player
        self.board = Board(BOARD_STARTING_STATE) if board is None else board
        self.model = Model(AI_MODEL) if model is None else model
        if self.starting_player == RANDOM:
            if random.randint(0,1) == 0:
                self.activePlayer = PLAYER_1
            else:
                self.activePlayer = PLAYER_2
        else:
            self.activePlayer = self.starting_player
        self.turn = 0
        self.move = 0
        self.winner = None


    def execute_turn(self):
        # Info about turn
        print(f"TURN BEGINS - {self.activePlayer}")
        print(f"turn: {self.turn} move: {self.move}")
        # Validate board
        if not self.board.is_board_valid(): 
            print(f"WARNING: Board state is not valid")
        # Several moves can be made in one turn
        while True:
            # Find legal moves
            self.legal_moves = self.board.legal_moves(self.activePlayer,self.turn,self.move)
            if self.turn == 1 and self.move == 0: # Allow to rotate board after first turn
                self.legal_moves.append(0)

            # Check if legal moves exist
            if self.legal_moves == []: 
                print(f"\nNo legal moves for {self.activePlayer}")
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
            elif not self.board.sow_seeds(self.activePlayer,pit): # If no additional move
                break
            else: # Additional move
                self.move += 1
                print(f"\nADDITIONAL MOVE GRANTED, move {self.move}")

        # Change turn
        self.change_turn()


    def select_pit(self, legal_moves=None):
        if self.activePlayer == "Human":
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
            else: # Computer
                self.model._initTurn(self)
                pit, value = self.model.bestTurn(self.model.algorithm, self.board, self.model.depth, True, self.model.negInf, self.model.posInf)
                print("\nComputer evaluates board to " + str(value))
                return pit


    def change_turn(self):
        if self.activePlayer == PLAYER_1:
            self.activePlayer = PLAYER_2
        else:
            self.activePlayer = PLAYER_1
        self.turn += 1
        self.move = 0
        print("-" * 20)
