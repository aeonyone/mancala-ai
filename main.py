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

def main():
    # Init game with no custom board state or custom AI
    game = Game()

    # Start game
    while(True):
        legalMoves = game.board.generateLegalMoves(game.activePlayer,game.turnNr,game.turnMove)
        game.prepareTurn(legalMoves)
        selectedPit = game.selectPit(legalMoves)
        if legalMoves != []:
            if game.executeTurn(selectedPit,legalMoves):
                game.turnMove += 1
            else: # If turn ends
                game.turnMove = 0

        if game.winner() != None:
            # NB! Bug if one side gets additional move, but is without seeds. The game does not end.
            print('\nFinal board:\n')
            game.board.drawBoard()
            print("\n Winner is " + game.winner() + "\n")
            break

        elif game.status != 'ONGOING':
            print("\n Game over!\n")
            break


if __name__ == '__main__':
    main()