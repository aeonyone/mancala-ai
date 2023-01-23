import random
# import threading

from .constants import *
from assets.board import Board
from assets.model import Model

class Game:
    def __init__(self, whoStartsGame=None, board=None, model=None) -> None:
        self.whoStartsGame = WHO_STARTS_GAME if whoStartsGame is None else whoStartsGame
        self.activePlayer = self.assignFirstTurn()
        self.board = Board(BOARD_STARTING_STATE) if board is None else board
        self.model = Model(AI_MODEL) if board is None else model
        self.status = 'ONGOING'
        self.turnNr = 0
        self.turnMove = 0

    def assignFirstTurn(self):
        if self.whoStartsGame == RANDOM:
            if random.randint(0,1) == 0:
                return HUMAN
            else:
                return COMPUTER

        return self.whoStartsGame

    def prepareTurn(self, legalMoves):
        if not self.board.isBoardValid():
            print('ERROR: board not valid')
        print('turnNr: ' + str(self.turnNr), 'turnMove: ' + str(self.turnMove))
        self.board.drawBoard()

        if legalMoves == []:
            # I think this should not actually move beans to stores, just consider them as points
            self.status = self.board.allPitsToPlayersStores()
            return 

    def selectPit(self, legalMoves=None):
        if self.activePlayer == HUMAN:
            print('\nPlease input pit:', end = ' ')
            while(True):
                try:
                    return int(input())
                except ValueError:
                    print('Please input a number in ' + str(legalMoves))

        else: # COMPUTER TURN
            self.model._initTurn(self)
            selectedPit, value = self.model.bestTurn(self.model.algorithm, self.board, self.model.depth, True, self.model.negInf, self.model.posInf)
            print("\nComputer evaluates board to " + str(value))
            return selectedPit

    def executeTurn(self, selectedPit, legalMoves):
        # NB! Fix bug with not showing board before turn is made. This is actually threading bug somehow with sleep
        if self.activePlayer == COMPUTER:
            print('Computer chooses pit:' + str(selectedPit))

        if selectedPit in legalMoves:
            if selectedPit == 0:
                self.board.rotateBoard()
                self.changeTurn()
                return False

            elif not self.board.sowSeeds(self.activePlayer,selectedPit):
                self.changeTurn()
                return False

            else:
                # Check if game has winner
                if self.winner() == None:
                    print("\nOne more turn awarded to " + self.activePlayer)
                return True

        else:
            print('Selected pit is not a legal move')

    def changeTurn(self):
        if self.activePlayer == HUMAN:
            self.activePlayer = COMPUTER
        else:
            self.activePlayer = HUMAN
        self.turnNr += 1

    def winner(self):
        return self.board.winner()

    def userInput(self):
        # Do later
        while(True):
            print('Please input pit:')
            selectedPit = int(input())
            if selectedPit in self.board.generateLegalMoves():
                self.board.sowSeeds(selectedPit)
                break
            else:
                print('Selected pit is not a legal move')