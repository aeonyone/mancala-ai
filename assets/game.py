from assets.board import Board
import random
# import threading

from .constants import *
from assets.board import Board
from assets.ai import AI

class Game:
    def __init__(self, whoStartsGame, board, model) -> None:
        if whoStartsGame == None:
            self.whoStartsGame = HUMAN
        else:
            self.whoStartsGame = whoStartsGame
        self.activePlayer = self.assignFirstTurn()
        self.status = 'ONGOING'
        self.turnNr = 0
        # Init board based on passed board
        if board == None:
            self.board = Board(BOARD_STARTING_STATE)
        else:
            self.board = board
        # Init AI based on passed model
        if model == None:
            self.AI = AI(AI_MODEL)
        else:
            self.AI = model

    def assignFirstTurn(self):
        if self.whoStartsGame == RANDOM:
            if random.randint(0,1) == 0:
                return HUMAN
            else:
                return COMPUTER

        return self.whoStartsGame


    def executeTurn(self):
        # NB! Fix bug with not showing board before turn is made. This is actually threading bug somehow with sleep
        while(True):
            if not self.board.isBoardValid():
                print('ERROR: board not valid')
            self.board.drawBoard()
            turnMove = 0 
            legalMoves = self.board.generateLegalMoves(self.activePlayer,self.turnNr,turnMove)
            if legalMoves == []:
                # I think this should not actually move beans to stores, just consider them as points
                self.status = self.board.allPitsToPlayersStores()
                break

            elif self.activePlayer == HUMAN:
                print('\nPlease input pit:', end = ' ')
                while(True):
                    try:
                        selectedPit = int(input())
                        break
                    except ValueError:
                        print('Please input a number')
                if selectedPit in legalMoves:
                    if selectedPit == 0:
                        self.board.rotateBoard()
                        self.changeTurn()
                        break
                    elif not self.board.sowSeeds(self.activePlayer,selectedPit):
                        self.changeTurn()
                        break
                    else:
                        print("\nHave one more turn\n")
                        turnMove += 1 
                else:
                    print('Selected pit is not a legal move')
        
            else: # COMPUTER TURN

                # selectedPit = random.choice(legalMoves)
                # selectedPit = self.AI.minimax(self.board, AI_DEPTH, True)
                selectedPit = self.AI.bestTurn(self.AI.model, self.board, AI_DEPTH, True, self.AI.negInf, self.AI.posInf)
                print('\nComputer chooses pit:' + str(selectedPit))
                if selectedPit == 0:
                    self.board.rotateBoard()
                    self.changeTurn()
                    break
                elif not self.board.sowSeeds(self.activePlayer,selectedPit):
                    self.changeTurn()
                    break
                else:
                    # Check if game has winner
                    if self.winner() != None:
                        break
                    print("\nComputer goes again\n")
                    turnMove += 1

    def changeTurn(self):
        if self.activePlayer == HUMAN:
            self.activePlayer = COMPUTER
        else:
            self.activePlayer = HUMAN
        self.turnNr += 1

    def winner(self):
        return self.board.winner()

    def _init(self):
        pass

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