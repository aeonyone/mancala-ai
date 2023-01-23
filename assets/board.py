from multiprocessing.dummy import active_children
from .constants import *

class Board:
    def __init__(self,board=None) -> None:
        # Init custom board or create default one
        if board == None:
            self.board = {HUMAN : [], COMPUTER : []}
            self.createBoard()
        else:
            self.board = board
        self.score = {HUMAN : 0, COMPUTER : 0}
        self.maxScore = PITS * SEEDS * 2
        
    def createBoard(self):
        for i in self.board:
            for j in range(PITS):
                self.board[i].append(SEEDS)

    def drawBoard(self):
        # NB! Fix the hardcoded oponnent and player keys
        playerBoard = self.board[HUMAN]
        opponentBoard = list(reversed(self.board[COMPUTER]))
        
        print(" ",opponentBoard) # Reverse opponent board
        print(self.score[COMPUTER], " " * 19, self.score[HUMAN]) # Stores
        print(" ", playerBoard)  # Player board

    def sowSeeds(self, activePlayer, pit):
        # NB! Use modulus to execute full circle and full board turns at once. Then only few operations are left to loops.
        # This can be made to work even if it goes 100 circles.
        # Use map function to increment list at once
        activePit = pit - 1 # Take note of the active pit and map it to the list
        seedsInHand = self.board[activePlayer][activePit] # Get seeds from pit
        self.board[activePlayer][activePit] = 0 # Set seeds in pit to 0
        activeBoardSide = activePlayer # Take note of the current board side
        while(True):
            if activePit == 6:
                activePit = 0
            else:
                activePit += 1

            # NB implement modules to solve the outcome of sowing
            if seedsInHand == 0: # To handle minimax bug
                print(activePlayer, self.board, 'ERROR: Seeds in hand == 0')
                break
            if seedsInHand > 1:
                if activePit < 6:
                    self.board[activeBoardSide][activePit] += 1 # Drop a seed in a pit
                    seedsInHand -= 1
                else: # activePit == 6
                    if activeBoardSide == activePlayer:
                        self.score[activePlayer] += 1 # Drop seed in active player store
                        seedsInHand -= 1
                        activeBoardSide = self.switchActiveBoardSide(activeBoardSide)
                        # Leave activePit as 6
                    else: # activeBoardSide != activePlayer
                        activeBoardSide = self.switchActiveBoardSide(activeBoardSide)
                        activePit = 0
                        self.board[activeBoardSide][activePit] += 1
                        seedsInHand -= 1
            # NB make function for capturing opponent store
            else: # seedsInHand == 1
                if activePit < 6:
                    if activeBoardSide == activePlayer:
                        if self.board[activeBoardSide][activePit] == 0:
                            if activePlayer == HUMAN and self.board[COMPUTER][LIST_LEN - activePit] > 0: # Check if there is anything to capture in the opponent pit
                                self.score[activePlayer] += 1 + self.board[COMPUTER][LIST_LEN - activePit] # Steal beans
                                self.board[COMPUTER][LIST_LEN - activePit] = 0 # Set opponent pit to 0
                            elif activePlayer == COMPUTER and self.board[HUMAN][LIST_LEN - activePit] > 0: 
                                self.score[activePlayer] += 1 + self.board[HUMAN][LIST_LEN - activePit] # Steal beans
                                self.board[HUMAN][LIST_LEN - activePit] = 0 # Set opponent pit to 0    
                            else: # If there are no seeds to capture
                                self.board[activeBoardSide][activePit] += 1
                            return False
                        else: # Pit not empty
                            self.board[activeBoardSide][activePit] += 1 # Drop a seed in a pit
                            return False
                    else: # activeBoardSide != activePlayer
                        self.board[activeBoardSide][activePit] += 1 # Drop a seed in a pit
                        return False
                else: # activePit == 6
                    if activeBoardSide == activePlayer:
                        self.score[activePlayer] += 1
                        return True
                    else: # Opponent board
                        activeBoardSide = self.switchActiveBoardSide(activeBoardSide)
                        activePit = 0
                        if activePlayer == HUMAN and self.board[activeBoardSide][activePit] == 0 and self.board[COMPUTER][LIST_LEN - activePit] > 0: # Check if there is anything to capture in the opponent pit
                            self.score[activePlayer] += 1 + self.board[COMPUTER][LIST_LEN - activePit] # Steal beans
                            self.board[COMPUTER][LIST_LEN - activePit] = 0 # Set opponent pit to 0
                        elif activePlayer == COMPUTER and self.board[activeBoardSide][activePit] == 0 and self.board[HUMAN][LIST_LEN - activePit] > 0: 
                            self.score[activePlayer] += 1 + self.board[HUMAN][LIST_LEN - activePit] # Steal beans
                            self.board[HUMAN][LIST_LEN - activePit] = 0 # Set opponent pit to 0    
                        else: # If there are no seeds to capture
                            self.board[activeBoardSide][activePit] += 1
                        return False

    def switchActiveBoardSide(self,activeBoardSide):
        if activeBoardSide == HUMAN:
            return COMPUTER
        else: #COMPUTER
            return HUMAN

    def generateLegalMoves(self,activePlayer,turnNr,turnMove):
        moves = []
        for pit, i in zip(self.board[activePlayer], range(1, 7)):
            if pit > 0:
                moves.append(i)
        if turnNr == 1 and turnMove == 0: # Allow to rotate board after first turn
            moves.append(0)
        return moves

    def allPitsToPlayersStores(self):
        self.score[HUMAN] += sum(self.board[HUMAN]) 
        self.score[COMPUTER] += sum(self.board[COMPUTER])
        self.board[HUMAN] = self.board[COMPUTER] = [0] * PITS
        return 'DONE'

    def rotateBoard(self):
        # Rotate board
        tempBoard = self.board[COMPUTER]
        self.board[COMPUTER] = self.board[HUMAN]
        self.board[HUMAN] = tempBoard
        # Rotate score
        tempScore = self.score[COMPUTER]
        self.score[COMPUTER] = self.score[HUMAN]
        self.score[HUMAN] = tempScore

    # Check if game is over
    def winner(self):
        if self.score[HUMAN] > self.maxScore / 2:
            return HUMAN
        elif self.score[COMPUTER] > self.maxScore / 2:
            return COMPUTER
        elif self.score[HUMAN] == self.score[COMPUTER] ==  self.maxScore / 2:
            return 'DRAW'

        return None

    def evaluateBoard(self):
        return self.score[COMPUTER] - self.score[HUMAN]


    def isBoardValid(self):
        return self.score[HUMAN] + self.score[COMPUTER] + sum(self.board[HUMAN]) + sum(self.board[COMPUTER])  == self.maxScore

    # def get