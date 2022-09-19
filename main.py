from assets.game import Game
from assets.constants import *

# TODO:
    # Implement treading to paralellize e.g. AI evaluation at terminal node
    # Or parallelize all AI action, however then alphabeta would not work easily 
# Interesting points to consider:
    # 1.
        # Why does computer priorites capture over pitting 1 bean at pit 6 AND then immediately capture
        # Need to test, maybe it happens in scenarios where I cannot increment the pit 6
    # 2. 
        # Is odd minimax depth more aggresive due to max function at bottom of the tree
        # And the other way, is even mimimax depth more defensive
        # Can it be that odd minimax at depth N loses to even minimax at depth N - 1?
        # 
        #  

class HumanPlayer:
    def __init__(self) -> None:
        pass

    
    # Collect user input
    def collectInput(self):
        input = int(input)

    
    def isLegalMove(self):
        # Test if the pit is not empty
        pass
        # 

    def sow(self):

        # Check if move is legal
        while(True):
           
            # Test if the pit is not empty
             pass
        pass

# TBD
class AIPlayer:
    def __init__(self) -> None:
        pass



def main():
    # Init game with no custom board state or custom AI
    game = Game(WHO_STARTS_GAME, None, None)

    # Start game
    while(True):
        if game.winner() != None:
            print('\nFinal board:\n')
            game.board.drawBoard()
            print("\n Winner is " + game.winner() + "\n")
            break
        elif game.status != 'ONGOING':
            print("\n Game over!\n")
            break
        else:
            game.executeTurn()


if __name__ == '__main__':
    main()