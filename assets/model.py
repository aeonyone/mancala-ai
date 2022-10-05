from copy import deepcopy
import random
from .constants import *

# NB ! Implement shallow, e.g. 6 - 7 layers of investigative minimax, and then for best few branches go really deep
    # 20% / 80 % effort respectively

# NB ! Test what is best way to sort legal moves (e.g. by size or by position), to improve pruning 

# Maybe game.self should be passed in the model, it would simplify a lot?
# Fix bug where "TypeError: cannot unpack non-iterable int object" if computer must make turn, but can't
# Fix bug where game does not end, if player cannot make turn
# Need to generalize actions between both minimax and alphabeta models

# NB! Make tests for model, alphabeta is definitely losing information in the pruning process
    # However, this loss is not apparent in shallow levels
class Model:
    def __init__(self, algorithm=None, depth=None) -> None:
        # Use default model if not otherwise specified
        self.algorithm = 'minimax' if algorithm is None else algorithm
        self.depth = AI_DEPTH if depth is None else depth
        self.posInf = 1000
        self.negInf = -1000

    def _initTurn(self, game):
        self.turnNr = game.turnNr
        self.turnMove = game.turnMove

    def _exitTurn(self):
        self.turnNr = 0
        self.turnMove = 0

    def bestTurn(self, algorithm, board, depth, maximizingPlayer, alpha, beta):
        if algorithm == 'minimax':
            return self.minimax(board, depth, maximizingPlayer)
        elif algorithm == 'alphabeta':
            return self.alphabeta(board, depth, maximizingPlayer, alpha, beta)
        else:
            return None
    
    def minimax(self, board, depth, maximizingPlayer):
        if depth == 0 or board.winner() != None:
            # NB! Should set values to inf if model finds winning solution
            return board.evaluateBoard()

        if maximizingPlayer:
            value = self.negInf # float('-inf')
            scoreDict = {}
            for selectedPit in board.generateLegalMoves(COMPUTER, self.turnNr, self.turnMove):
                sideBranch = value
                # Replicate board
                tempBoard = deepcopy(board)
                while(True):
                    if selectedPit == 0:
                        tempBoard.rotateBoard()
                        break
                    elif not tempBoard.sowSeeds(COMPUTER, selectedPit):
                        break
                    else: # Additional move
                        sideBranch = self.minimax(tempBoard, depth - 1, True) # Launch new branch
                        break
                scoreDict[selectedPit] = max(sideBranch, self.minimax(tempBoard, depth - 1, False))
            
            # Maximum value at the position
            if scoreDict != {}: # If scoreDict is empty, it means that no turn can be made, e.g. in case when last pit is captured
                value = max(value, scoreDict[max(scoreDict, key=scoreDict.get)])
            # Return best turn at the root node
            if depth == self.depth:
                strongestMoves = []
                for i in scoreDict:
                    if scoreDict[i] == value:
                        strongestMoves.append(i)
                returnPit = random.choice(strongestMoves)
                return returnPit, value
            else: # If not at the root node
                return value

        else: # Minimizing player
            value = self.posInf # float('inf')
            scoreDict = {}
            legalMoves = board.generateLegalMoves(HUMAN, 0, 0)
            if self.turnNr == 0 and depth >= self.depth - 2: # Force computer to consider player switching board after Conputer first turn
                legalMoves.append(0)
            for selectedPit in legalMoves:
                sideBranch = value
                tempBoard = deepcopy(board)
                while(True):
                    if selectedPit == 0:
                        tempBoard.rotateBoard()
                        break
                    elif not tempBoard.sowSeeds(HUMAN, selectedPit):
                        break
                    else: # Additional move
                        sideBranch = self.minimax(tempBoard, depth - 1, False) # Launch new branch
                        break
                scoreDict[selectedPit] = min(sideBranch, self.minimax(tempBoard, depth - 1, True))
            
            # Maximum value at the position
            if scoreDict != {}: # If scoreDict is empty, it means that no turn can be made, e.g. in case when last pit is captured
                value = min(value, scoreDict[min(scoreDict, key=scoreDict.get)])
            
            # NB! This likely should be removed, because minimizing player (Human) will not be at the root node 
            # Return best turn at the root node
            if depth == self.depth:
                strongestMoves = []
                for i in scoreDict:
                    if scoreDict[i] == value:
                        strongestMoves.append(i)
                returnPit = random.choice(strongestMoves)
                return returnPit
            else: # If not at the root node
                return value

    # NB! alphabeta move generates 0 seeds in hand bug at position {HUMAN : [4, 4, 0, 0, 5, 5], COMPUTER : [5, 5, 4, 4, 4, 4]}
    def alphabeta(self, board, depth, maximizingPlayer, alpha, beta):
        if depth == 0 or board.winner() != None:
            return board.evaluateBoard()   

        if maximizingPlayer:
            value = self.negInf # float('-inf')
            scoreDict = {}
            legalMoves = board.generateLegalMoves(COMPUTER, self.turnNr, self.turnMove)
            for selectedPit in legalMoves:
                sideBranch = value
                # Replicate board
                tempBoard = deepcopy(board)
                while(True):
                    if not tempBoard.sowSeeds(COMPUTER, selectedPit):
                        break
                    else: # Additional move
                        sideBranch = self.alphabeta(tempBoard, depth - 1, True, alpha, beta) # Launch new branch
                        break
                scoreDict[selectedPit] = max(sideBranch, self.alphabeta(tempBoard, depth - 1, False, alpha, beta))
                alpha = max(alpha, scoreDict[selectedPit])
                # Pruning
                if beta <= alpha:
                    break
            
            # Maximum value at the position
            if scoreDict != {}: # If scoreDict is empty, it means that no turn can be made, e.g. in case when last pit is captured
                value = max(value, scoreDict[max(scoreDict, key=scoreDict.get)])

            # Return best turn at the root node
            if depth == self.depth:
                strongestMoves = []
                for i in scoreDict:
                    if scoreDict[i] == value:
                        strongestMoves.append(i)
                returnPit = random.choice(strongestMoves)
                return returnPit, value
            else: # If not at the root node
                return value

        else: # Minimizing player
            value = self.posInf # float('inf')
            scoreDict = {}
            legalMoves = board.generateLegalMoves(HUMAN, 0, 0)
            if self.turnNr == 0 and depth >= self.depth - 2: # Force computer to consider player switching board after Conputer first turn
                legalMoves.append(0)
            for selectedPit in legalMoves:
                sideBranch = value
                tempBoard = deepcopy(board)
                while(True):
                    if not tempBoard.sowSeeds(HUMAN, selectedPit):
                        break
                    else: # Additional move
                        sideBranch = self.alphabeta(tempBoard, depth - 1, False, alpha, beta) # Launch new branch
                        break
                scoreDict[selectedPit] = min(sideBranch, self.alphabeta(tempBoard, depth - 1, True, alpha, beta))
                beta = min(beta, scoreDict[selectedPit])
                # Pruning
                if beta <= alpha:
                    break
                
            # Maximum value at the position
            if scoreDict != {}: # If scoreDict is empty, it means that no turn can be made, e.g. in case when last pit is captured
                value = min(value, scoreDict[min(scoreDict, key=scoreDict.get)])

            return value