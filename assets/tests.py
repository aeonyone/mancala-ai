from .constants import *
from assets.board import Board
from assets.ai import AI
from assets.game import Game

class Tests:
    def __init__(self) -> None:
       pass   

    def isMinimaxValid(self):
        model = AI('minimax')
        
        ## Run tests
        # Depth 1
        
        board = Board({HUMAN : [0, 0, 0, 0, 0, 0], COMPUTER : [1, 1, 1, 1, 1, 1]})
        game = Game('Computer', board, model)
        game.executeTurn()
    def isAlphabetaValid(self):
        pass