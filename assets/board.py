from copy import deepcopy
from multiprocessing.dummy import active_children
from .constants import *
import numpy as np


class Board:
    def __init__(self, board=None, score=None, previous_state=None, player_1=None, player_2=None) -> None:
        # Init custom board or create default one
        self.player_1 = player_1
        self.player_2 = player_2
        # Init board
        if board:
            self.board = board
        elif BOARD_STARTING_STATE == None:
            self.board = {self.player_1 : [], self.player_2 : []}
            for i in self.board:
                for j in range(PITS):
                    self.board[i].append(SEEDS)
        elif BOARD_STARTING_STATE:
            self.board = {self.player_1 : BOARD_STARTING_STATE['Player 1'], self.player_2 : BOARD_STARTING_STATE['Player 2']}
        else:
            raise ValueError('Cannot init board')
        # Init score
        if score:
            self.score = score
        else:
            self.score = {self.player_1 : 0, self.player_2 : 0}

        self.max_score = PITS * SEEDS * 2
        self.previous_state = previous_state


    def draw_board(self):
        # NB! Fix the hardcoded oponnent and player keys
        player_board = self.board[self.player_1]
        opponent_board = list(reversed(self.board[self.player_2]))
        print("\n ",opponent_board) # Reverse opponent board
        print(self.score[self.player_2], " " * 19, self.score[self.player_1]) # Stores
        print(" ", player_board)  # Player board

    def get_legal_moves(self,active_player):
        moves = []
        for pit, i in zip(self.board[active_player], range(1, 7)):
            if pit > 0:
                moves.append(i)
        return moves

    def apply_move(self, active_player, pit):
        # NB! Use numpy array for board to increment all pits at once
        # Validate move
        if pit not in [1, 2, 3, 4, 5, 6]:
            raise ValueError('Invalid pit')
        # Apply move
        active_pit = pit - 1 # Take note of the active pit and map it to the list
        seeds_in_hand = self.board[active_player][active_pit] # Get seeds from pit
        self.board[active_player][active_pit] = 0 # Set seeds in pit to 0
        active_board_side = active_player # Take note of the current board side
        while(True):
            if active_board_side == active_player: # If current board side is active player's
                # Three cases are possible:
                # Seeds in hand does not reach the score pit
                if seeds_in_hand <= PITS - active_pit - 1:
                    # Increment seeds_in_hand number of pits
                    self.board[active_player][active_pit + 1 : active_pit + 1 + seeds_in_hand] = map(lambda x: x + 1, self.board[active_player][active_pit + 1 : active_pit + 1 + seeds_in_hand])
                    # Set the active pit to last dropped seed
                    active_pit = active_pit + seeds_in_hand
                    break
                # Seeds in hand reaches the score pit exactly
                elif seeds_in_hand == PITS - active_pit:
                    # Increment seeds_in_hand number of pits
                    self.board[active_player][active_pit + 1 : PITS] = map(lambda x: x + 1, self.board[active_player][active_pit + 1 : PITS]) 
                    # Increment score
                    self.score[active_player] += 1
                    # Get additional turn
                    return True
                # Seeds in hand can reach beyond the score pit 
                else: # seeds_in_hand > PITS - active_pit:
                    # Increment seeds_in_hand number of pits
                    self.board[active_player][active_pit + 1 : PITS] = map(lambda x: x + 1, self.board[active_player][active_pit + 1 : PITS]) 
                    # Increment score
                    self.score[active_player] += 1
                    # Subtract the number of pits that were incremented
                    seeds_in_hand -= PITS - active_pit
                    # Set active pit to 0
                    active_pit = 0
                    # Switch active board side
                    active_board_side = self.switch_active_side(active_board_side)
                    continue
            else: # If current board side is opponent's
                # Two cases are possible:
                # Seeds in hand reaches up to or including the last pit
                if seeds_in_hand <= PITS:
                    # Increment seeds_in_hand number of pits
                    self.board[active_board_side][active_pit : active_pit + seeds_in_hand] = map(lambda x: x + 1, self.board[active_board_side][active_pit : active_pit + seeds_in_hand])
                    break
                # Seeds in hand go beyond last pit
                else: # seeds_in_hand > PITS:
                    # Increment all pits
                    self.board[active_board_side][active_pit : PITS] = map(lambda x: x + 1, self.board[active_board_side][active_pit : PITS])
                    # Subtract the number of pits that were incremented
                    seeds_in_hand -= PITS - active_pit
                    # Set active pit to -1 (to be incremented to 0)
                    active_pit = -1
                    # Switch active board side
                    active_board_side = self.switch_active_side(active_board_side)
                    continue
                
        # Capture logic. Check if last seed was dropped in empty pit in active player's side and if opponent's pit is not empty
        if active_board_side == active_player:
            if self.board[active_player][active_pit] == 1:
                if self.board[self.switch_active_side(active_player)][PITS - active_pit - 1] > 0:
                    # Take all seeds from both pits
                    self.score[active_player] += self.board[active_player][active_pit] + self.board[self.switch_active_side(active_player)][PITS - active_pit - 1]
                    self.board[active_player][active_pit] = self.board[self.switch_active_side(active_player)][PITS - active_pit - 1] = 0
        return False

    def switch_active_side(self,active_board_side):
        if active_board_side == self.player_1:
            return self.player_2
        else: #self.player_2
            return self.player_1

    def revert_move(self):
        # Difficult to implement, deepcopy self approach does not work because player_1 and player_2 memory addresses change
        # If one would be so inclined, hash could be calculated at player init and used as a key in the dictionary
        pass

    def rotate_board(self):
        # Rotate board
        temp_board = self.board[self.player_2]
        self.board[self.player_2] = self.board[self.player_1]
        self.board[self.player_1] = temp_board
        # Rotate score
        temp_score = self.score[self.player_2]
        self.score[self.player_2] = self.score[self.player_1]
        self.score[self.player_1] = temp_score

    # Check if game is over
    def check_winner(self):
        if self.score[self.player_1] > self.max_score / 2:
            return self.player_1
        elif self.score[self.player_2] > self.max_score / 2:
            return self.player_2
        elif self.score[self.player_1] == self.score[self.player_2] ==  self.max_score / 2:
            return 'DRAW'

        return None

    def is_board_valid(self):
        return self.score[self.player_1] + self.score[self.player_2] + sum(self.board[self.player_1]) + sum(self.board[self.player_2])  == self.max_score

    def evaluate_position(self, proponent, opponent):
        winner = self.check_winner()
        if winner == proponent:
            return 1000
        elif winner == opponent:
            return -1000
        elif winner == 'DRAW':
            return 0
        else:
            return self.score[proponent] - self.score[opponent]

    def heuristic_value(self, player):
        value = 0
        for i in range(PITS):
            pit = PITS - i - 1 # reverse order
            if self.board[player][pit] == i + 1:
                value += 1

        # 6 pit clear variations
        if self.board[player][0] == 6:
            pass # should be calculated in some algorithmic way, recursive?
        # 5 pit clear variations
        if self.board[player][1] == 5:
            pass # should be calculated in some algorithmic way, recursive?
        # 4 pit clear variations
        if self.board[player][2] == 4:
            if self.board[player][2:] == [4,3,2,1]:
                value += 5 # 9 (nominal) - 4 (generated by loop)
            if self.board[player][2:] == [4,3,2,0]:
                value += 5 # 8 (nominal) - 3 (generated by loop)
            if self.board[player][2:] == [4,3,1,1]:
                value += 4 # 7 (nominal) - 3 (generated by loop)
            if self.board[player][2:] == [4,3,1,0]:
                value += 4 # 6 (nominal) - 2 (generated by loop)
            if self.board[player][2:] == [4,3,0,1]:
                value += 4 # 7 (nominal) - 3 (generated by loop)
            if self.board[player][2:] == [4,3,0,0]:
                value += 4 # 6 (nominal) - 2 (generated by loop)
            if self.board[player][2:] == [4,2,2,1]:
                value += 6 # 9 (nominal) - 3 (generated by loop)
            if self.board[player][2:] == [4,2,2,0]:
                value += 6 # 8 (nominal) - 2 (generated by loop)
            if self.board[player][2:] == [4,2,1,1]:
                value += 5 # 7 (nominal) - 2 (generated by loop)
            if self.board[player][2:] == [4,2,1,0]:
                value += 5 # 6 (nominal) - 1 (generated by loop)
            if self.board[player][2:] == [4,2,0,1]:
                value += 5 # 7 (nominal) - 2 (generated by loop)
            if self.board[player][2:] == [4,2,0,0]:
                value += 5 # 6 (nominal) - 1 (generated by loop)
            if self.board[player][2:] == [4,1,1,1]:
                value += 2 # 4 (nominal) - 2 (generated by loop)
            if self.board[player][2:] == [4,1,1,0]:
                value += 2 # 3 (nominal) - 1 (generated by loop)
            if self.board[player][2:] == [4,1,0,1]:
                value += 1 # 3 (nominal) - 2 (generated by loop)
            if self.board[player][2:] == [4,1,0,0]:
                value += 1 # 2 (nominal) - 1 (generated by loop)
            if self.board[player][2:] == [4,0,1,1]:
                value += 3 # 5 (nominal) - 2 (generated by loop)
            if self.board[player][2:] == [4,0,1,0]:
                value += 1 # 4 (nominal) - 1 (generated by loop)
            if self.board[player][2:] == [4,0,0,1]:
                value += 1 # 3 (nominal) - 2 (generated by loop)
            if self.board[player][2:] == [4,0,0,0]:
                value += 1 # 2 (nominal) - 1 (generated by loop)
        # 3 pit clear variations
        elif self.board[player][3] == 3:
            if self.board[player][3:] == [3,2,1]: # 3 pit clear
                value += 2 # 5 (nominal) - 3 (generated by loop)
            if self.board[player][3:] == [3,2,0]: # 3 pit clear
                value += 2 # 4 (nominal) - 2 (generated by loop)
            if self.board[player][3:] == [3,1,1]: # 3 pit clear
                value += 3 # 5 (nominal) - 2 (generated by loop)
            if self.board[player][3:] == [3,1,0]: # 3 pit clear
                value += 3 # 4 (nominal) - 1 (generated by loop)
            if self.board[player][3:] == [3,0,1]: # 3 pit clear
                value += 1 #3 (nominal) - 2 (generated by loop)
            if self.board[player][3:] == [3,0,0]: # 3 pit clear
                value += 1 #2 (nominal) - 1 (generated by loop)
        # 2 pit clear variations
        elif self.board[player][4] == 2:
            # 2 pit full clear
            if self.board[player][4:] == [2,1]: # 2 pit clear
                value += 1 # 3 (nominal) - 2 (generated by loop)
            # 2 pit partial clear
            if self.board[player][4:] == [2,0]: # 2 pit clear
                value += 1 # 2 (nominal) - 1 (generated by loop)

        return value
