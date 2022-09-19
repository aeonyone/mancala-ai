from copy import deepcopy
import random
from .constants import *

# NB ! Implement shallow, e.g. 6 - 7 layers of investigative minimax, and then for best few branches go really deep
    # 20% / 80 % effort respectively

# NB! Make tests for model, alphabeta is definitely losing information in the pruning process
    # However, this loss is not apparent in shallow levels
class AI:
    def __init__(self, model) -> None:
        # Use default model if not otherwise specified
        if model == None:
            self.model = 'minimax'
        else:
            self.model = model
        self.posInf = 1000
        self.negInf = -1000

    def bestTurn(self, model, board, depth, maximizingPlayer, alpha, beta):
        if model == 'minimax':
            return self.minimax(board, depth, maximizingPlayer)
        elif model == 'alphabeta':
            return self.alphabeta(board, depth, maximizingPlayer, alpha, beta)
        else:
            return None

    # NB! Implement alpha-beta pruning
    def minimax(self, board, depth, maximizingPlayer):
        if depth == 0 or board.winner() != None:
            return board.evaluateBoard()

        if maximizingPlayer:
            value = self.negInf # float('-inf')
            scoreDict = {}
            for selectedPit in board.generateLegalMoves(COMPUTER, 0, 0): # Need to fix
                sideBranch = value
                # Replicate board
                tempBoard = deepcopy(board)
                while(True):
                    if not tempBoard.sowSeeds(COMPUTER, selectedPit):
                        break
                    else: # Additional move
                        sideBranch = self.minimax(tempBoard, depth - 1, True) # Launch new branch
                        break
                scoreDict[selectedPit] = max(sideBranch, self.minimax(tempBoard, depth - 1, False))
            
            # Maximum value at the position
            if scoreDict != {}: # If scoreDict is empty, it means that no turn can be made, e.g. in case when last pit is captured
                value = max(value, scoreDict[max(scoreDict, key=scoreDict.get)])
            # Return best turn at the root node
            if depth == AI_DEPTH:
                strongestMoves = []
                for i in scoreDict:
                    if scoreDict[i] == value:
                        strongestMoves.append(i)
                returnPit = random.choice(strongestMoves)
                return returnPit
            else: # If not at the root node
                return value

        else: # Minimizing player
            value = self.posInf # float('inf')
            scoreDict = {}
            for selectedPit in board.generateLegalMoves(HUMAN, 0, 0): # Need to fix
                sideBranch = value
                tempBoard = deepcopy(board)
                while(True):
                    if not tempBoard.sowSeeds(HUMAN, selectedPit):
                        break
                    else: # Additional move
                        sideBranch = self.minimax(tempBoard, depth - 1, False) # Launch new branch
                        break
                scoreDict[selectedPit] = min(sideBranch, self.minimax(tempBoard, depth - 1, True))
            
            # Maximum value at the position
            if scoreDict != {}: # If scoreDict is empty, it means that no turn can be made, e.g. in case when last pit is captured
                value = min(value, scoreDict[min(scoreDict, key=scoreDict.get)])
            
            # Return best turn at the root node
            if depth == AI_DEPTH:
                strongestMoves = []
                for i in scoreDict:
                    if scoreDict[i] == value:
                        strongestMoves.append(i)
                returnPit = random.choice(strongestMoves)
                return returnPit
            else: # If not at the root node
                return value

    # NB! alphabeta is bugged and choses first available turn
    def alphabeta(self, board, depth, maximizingPlayer, alpha, beta):
        if depth == 0 or board.winner() != None:
            return board.evaluateBoard()   

        if maximizingPlayer:
            value = self.negInf # float('-inf')
            scoreDict = {}
            for selectedPit in board.generateLegalMoves(COMPUTER, 0, 0): # Need to fix
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
            if depth == AI_DEPTH:
                strongestMoves = []
                for i in scoreDict:
                    if scoreDict[i] == value:
                        strongestMoves.append(i)
                returnPit = random.choice(strongestMoves)
                return returnPit
            else: # If not at the root node
                return value

        else: # Minimizing player
            value = self.posInf # float('inf')
            scoreDict = {}
            for selectedPit in board.generateLegalMoves(HUMAN, 0, 0): # Need to fix
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