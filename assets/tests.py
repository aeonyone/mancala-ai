from .constants import *
from assets.board import Board
from assets.model import Model
from assets.game import Game

class Tests:
    def __init__(self) -> None:
       pass   

    def runTest(self, board, model, depth):
        model = Model(model, depth)
        board = Board(board)
        return Game('Computer', board, model).selectPit()


    def isModelValid(self, model):
        ## Define cases
        case = [
            # Depth 1
            [{PLAYER_1 : [0, 0, 0, 0, 0, 0], PLAYER_2 : [1, 1, 1, 1, 1, 1]}, 1, [6]], # Scoring preference
            [{PLAYER_1 : [0, 1, 0, 0, 0, 0], PLAYER_2 : [1, 0, 0, 1, 0, 1]}, 1, [4]], # Capture preference
            [{PLAYER_1 : [0, 2, 0, 0, 1, 0], PLAYER_2 : [1, 0, 0, 1, 0, 1]}, 1, [4]], # Larger capture preference
            # Depth 2
            [{PLAYER_1 : [0, 2, 0, 0, 1, 0], PLAYER_2 : [1, 0, 0, 1, 0, 1]}, 2, [6]], # Prefer scoring before capture
            [{PLAYER_1 : [0, 2, 0, 0, 1, 0], PLAYER_2 : [1, 0, 0, 1, 0, 0]}, 2, [1]], # Prefers score advantage over larger score
            [{PLAYER_1 : [0, 5, 0, 2, 0, 0], PLAYER_2 : [9, 1, 0, 1, 0, 0]}, 2, [2]],  # Prevents attack
            # Depth 3
            [{PLAYER_1 : [1, 0, 1, 1, 0, 0], PLAYER_2 : [3, 0, 1, 0, 2, 1]}, 3, [6]],  # Escapes attack
            [{PLAYER_1 : [0, 0, 0, 1, 0, 1], PLAYER_2 : [0, 5, 4, 0, 0, 1]}, 3, [3,6]],  # Chains moves
            [{PLAYER_1 : [0, 4, 3, 0, 0, 0], PLAYER_2 : [0, 1, 0, 0, 1, 4]}, 3, [2,5]],  # Denies oponnent chain
            [{PLAYER_1 : [0, 4, 3, 0, 0, 0], PLAYER_2 : [1, 0, 2, 0, 1, 0]}, 3, [1]],  # Defends
            # Depth 4
            [{PLAYER_1 : [0, 0, 4, 2, 0, 0], PLAYER_2 : [4, 1, 0, 0, 0, 1]}, 4, [6]],  # 
            [{PLAYER_1 : [0, 0, 4, 1, 2, 8], PLAYER_2 : [0, 3, 1, 0, 5, 0]}, 4, [5]],  # 
            [{PLAYER_1 : [2, 4, 4, 0, 0, 0], PLAYER_2 : [6, 4, 4, 0, 1, 0]}, 4, [1]],  # 
            [{PLAYER_1 : [1, 4, 0, 4, 0, 0], PLAYER_2 : [5, 5, 4, 4, 4, 4]}, 4, [3]],  # 
        ]

        ## Run tests
        isSuccess = True
        for i in range(len(case)):
            if self.runTest(case[i][0], model, case[i][1]) in case[i][2]:
                print('Depth ' + str(case[i][1]) + ' case ' + str(i) + ' SUCCESS')
            else:
                print('Depth ' + str(case[i][1]) + ' case ' + str(i) + ' FAIL')
                isSuccess = False

        if isSuccess:
            print('Tests passed')
            return True
        else:
            print('Some tests failed')
            return False




