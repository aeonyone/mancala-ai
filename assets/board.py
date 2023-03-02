from multiprocessing.dummy import active_children
from .constants import *
import numpy as np


class Board:
    def __init__(self,board=None) -> None:
        # Init custom board or create default one
        if board == None:
            self.board = {PLAYER_1 : [], PLAYER_2 : []}
            for i in self.board:
                for j in range(PITS):
                    self.board[i].append(SEEDS)
        else:
            self.board = board
        self.score = {PLAYER_1 : 0, PLAYER_2 : 0}
        self.maxScore = PITS * SEEDS * 2


    def legal_moves(self,activePlayer,turn,move):
        moves = []
        for pit, i in zip(self.board[activePlayer], range(1, 7)):
            if pit > 0:
                moves.append(i)
        return moves

    def draw_board(self):
        # NB! Fix the hardcoded oponnent and player keys
        playerBoard = self.board[PLAYER_1]
        opponentBoard = list(reversed(self.board[PLAYER_2]))
        print("\n ",opponentBoard) # Reverse opponent board
        print(self.score[PLAYER_2], " " * 19, self.score[PLAYER_1]) # Stores
        print(" ", playerBoard)  # Player board

    def sow_seeds(self, activePlayer, pit):
        # NB! Use numpy array for board to increment all pits at once
        activePit = pit - 1 # Take note of the active pit and map it to the list
        seedsInHand = self.board[activePlayer][activePit] # Get seeds from pit
        self.board[activePlayer][activePit] = 0 # Set seeds in pit to 0
        activeBoardSide = activePlayer # Take note of the current board side
        while(True):
            if activeBoardSide == activePlayer: # If current board side is active player's
                # Three cases are possible:
                # Seeds in hand does not reach the score pit
                if seedsInHand <= PITS - activePit - 1:
                    # Increment seedsInHand number of pits
                    self.board[activePlayer][activePit + 1 : activePit + 1 + seedsInHand] = map(lambda x: x + 1, self.board[activePlayer][activePit + 1 : activePit + 1 + seedsInHand])
                    # Set the active pit to last dropped seed
                    activePit = activePit + seedsInHand
                    break
                # Seeds in hand reaches the score pit exactly
                elif seedsInHand == PITS - activePit:
                    # Increment seedsInHand number of pits
                    self.board[activePlayer][activePit + 1 : PITS] = map(lambda x: x + 1, self.board[activePlayer][activePit + 1 : PITS]) 
                    # Increment score
                    self.score[activePlayer] += 1
                    # Get additional turn
                    return True
                # Seeds in hand can reach beyond the score pit 
                else: # seedsInHand > PITS - activePit:
                    # Increment seedsInHand number of pits
                    self.board[activePlayer][activePit + 1 : PITS] = map(lambda x: x + 1, self.board[activePlayer][activePit + 1 : PITS]) 
                    # Increment score
                    self.score[activePlayer] += 1
                    # Subtract the number of pits that were incremented
                    seedsInHand -= PITS - activePit
                    # Set active pit to 0
                    activePit = 0
                    # Switch active board side
                    activeBoardSide = self.switch_side(activeBoardSide)
                    continue
            else: # If current board side is opponent's
                # Two cases are possible:
                # Seeds in hand reaches up to or including the last pit
                if seedsInHand <= PITS:
                    # Increment seedsInHand number of pits
                    self.board[activeBoardSide][activePit : activePit + seedsInHand] = map(lambda x: x + 1, self.board[activeBoardSide][activePit : activePit + seedsInHand])
                    break
                # Seeds in hand go beyond last pit
                else: # seedsInHand > PITS:
                    # Increment all pits
                    self.board[activeBoardSide][activePit : PITS] = map(lambda x: x + 1, self.board[activeBoardSide][activePit : PITS])
                    # Subtract the number of pits that were incremented
                    seedsInHand -= PITS - activePit
                    # Set active pit to -1 (to be incremented to 0)
                    activePit = -1
                    # Switch active board side
                    activeBoardSide = self.switch_side(activeBoardSide)
                    continue
                
        # Capture logic. Check if last seed was dropped in empty pit in active player's side and if opponent's pit is not empty
        if activeBoardSide == activePlayer:
            if self.board[activePlayer][activePit] == 1:
                if self.board[self.switch_side(activePlayer)][PITS - activePit - 1] > 0:
                    # Take all seeds from both pits
                    self.score[activePlayer] += self.board[activePlayer][activePit] + self.board[self.switch_side(activePlayer)][PITS - activePit - 1]
                    self.board[activePlayer][activePit] = self.board[self.switch_side(activePlayer)][PITS - activePit - 1] = 0
        return False

    def switch_side(self,activeBoardSide):
        if activeBoardSide == PLAYER_1:
            return PLAYER_2
        else: #PLAYER_2
            return PLAYER_1

    def rotate_board(self):
        # Rotate board
        tempBoard = self.board[PLAYER_2]
        self.board[PLAYER_2] = self.board[PLAYER_1]
        self.board[PLAYER_1] = tempBoard
        # Rotate score
        tempScore = self.score[PLAYER_2]
        self.score[PLAYER_2] = self.score[PLAYER_1]
        self.score[PLAYER_1] = tempScore

    # Check if game is over
    def check_winner(self):
        if self.score[PLAYER_1] > self.maxScore / 2:
            return PLAYER_1
        elif self.score[PLAYER_2] > self.maxScore / 2:
            return PLAYER_2
        elif self.score[PLAYER_1] == self.score[PLAYER_2] ==  self.maxScore / 2:
            return 'DRAW'

        return None

    def is_board_valid(self):
        return self.score[PLAYER_1] + self.score[PLAYER_2] + sum(self.board[PLAYER_1]) + sum(self.board[PLAYER_2])  == self.maxScore

    def evaluate_position(self):
        return self.board.score[PLAYER_2] - self.board.score[PLAYER_1]