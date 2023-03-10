from copy import deepcopy
import random
from .constants import *
from assets.board import Board

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
        self.algorithm = AI_MODEL if algorithm is None else algorithm
        self.depth = AI_DEPTH if depth is None else depth
        self.posInf = 1000
        self.negInf = -1000


    def best_turn(self, board, active_player, passive_player, can_rotate, can_opponent_rotate):
        # Create node
        node = Board(
            board={True: board.board[active_player], False: board.board[passive_player]}
            , score={True: board.score[active_player], False: board.score[passive_player]}
            , player_1=True
            , player_2=False
        )
        self.can_rotate = can_rotate
        self.can_opponent_rotate = can_opponent_rotate
        
        if self.algorithm == 'minimax':
            return self.minimax(node, self.depth, True)
        elif self.algorithm == 'alphabeta':
            return self.alphabeta(node, self.depth, True) # Needs rework
        else:
            return None
    
    def minimax(self, node, depth, maximizing_player):
        # Terminal state
        if depth == 0:
            return node.evaluate_position(True, False) + node.heuristic_value(True) - node.heuristic_value(False)
        
        # Maximizer
        if maximizing_player:
            # Get and check legal moves
            legal_moves = node.get_legal_moves(True)
            if depth == self.depth and self.can_rotate:
                legal_moves.append(0)
            if legal_moves == []:
                return self.negInf
            scoring = {}
            # Search each child of node
            for pit in legal_moves:
                value = self.negInf
                sub_node = deepcopy(node)
                # Apply move
                while True:
                    if pit == 0:
                        sub_node.rotate_board()
                        break
                    elif not sub_node.apply_move(True, pit):
                        break
                    else: # Additional move
                        value = max(value, self.minimax(sub_node, depth - 1, True))
                
                # Record value for each pit
                scoring[pit] = max(value, self.minimax(sub_node, depth - 1, False))

            # Maximum value at the position
            value = max(value, scoring[max(scoring, key=scoring.get)])
            
            # Return best turn at the root node
            if depth == self.depth:
                # If opponent can rotate, position evaluations are opposite
                if self.can_opponent_rotate:
                    # Reverse scoring
                    scoring = {k: -v for k, v in scoring.items()}
                    # Choose value closest to 0
                    value = min(scoring.values(), key=lambda x:abs(x))
                    # Get all moves with the least negative value
                    best_moves = [k for k, v in scoring.items() if v == value]
                else:
                    # Append all moves with the maximum value
                    best_moves = [k for k, v in scoring.items() if v == value]
                pit = random.choice(best_moves)
                return pit, value
            else: # If not at the root node
                return value

        # Minimizer
        else:
            # Get and check legal moves
            legal_moves = node.get_legal_moves(False)
            if legal_moves == []:
                return self.posInf
            scoring = {}
            # Search each child of node
            for pit in legal_moves:
                value = self.posInf
                sub_node = deepcopy(node)
                # Apply move
                while True:
                    if not sub_node.apply_move(False, pit):
                        break
                    else: # Additional move
                        value = min(value, self.minimax(sub_node, depth - 1, False))
                # Get value and pit pairs
                scoring[pit] = min(value, self.minimax(sub_node, depth - 1, True))

            # Minimum value at the position
            value = min(value, scoring[min(scoring, key=scoring.get)])

            return value


    # NB! alphabeta move generates 0 seeds in hand bug at position {PLAYER_1 : [4, 4, 0, 0, 5, 5], PLAYER_2 : [5, 5, 4, 4, 4, 4]}
    def alphabeta(self, board, depth, maximizing_player, alpha, beta):
        if depth == 0 or board.check_winner() != None:
            pass
            # return board.eval_board()   

        if maximizing_player:
            value = self.negInf # float('-inf')
            scoreDict = {}
            get_legal_moves = board.get_legal_moves(PLAYER_2, self.turn, self.move)
            for pit in get_legal_moves:
                sideBranch = value
                # Replicate board
                temp_board = deepcopy(board)
                while(True):
                    if not temp_board.apply_move(PLAYER_2, pit):
                        break
                    else: # Additional move
                        sideBranch = self.alphabeta(temp_board, depth - 1, True, alpha, beta) # Launch new branch
                        break
                scoreDict[pit] = max(sideBranch, self.alphabeta(temp_board, depth - 1, False, alpha, beta))
                alpha = max(alpha, scoreDict[pit])
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
            get_legal_moves = board.get_legal_moves(PLAYER_1, 0, 0)
            if self.turn == 0 and depth >= self.depth - 2: # Force computer to consider player switching board after Conputer first turn
                get_legal_moves.append(0)
            for pit in get_legal_moves:
                sideBranch = value
                temp_board = deepcopy(board)
                while(True):
                    if not temp_board.apply_move(PLAYER_1, pit):
                        break
                    else: # Additional move
                        sideBranch = self.alphabeta(temp_board, depth - 1, False, alpha, beta) # Launch new branch
                        break
                scoreDict[pit] = min(sideBranch, self.alphabeta(temp_board, depth - 1, True, alpha, beta))
                beta = min(beta, scoreDict[pit])
                # Pruning
                if beta <= alpha:
                    break
                
            # Maximum value at the position
            if scoreDict != {}: # If scoreDict is empty, it means that no turn can be made, e.g. in case when last pit is captured
                value = min(value, scoreDict[min(scoreDict, key=scoreDict.get)])

            return value