from assets.game import Game
from assets.player import Player
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
    game = Game(
        player_1=Player(type=PLAYER_1_TYPE, name=PLAYER_1_NAME)
        , player_2=Player(type=PLAYER_2_TYPE, name=PLAYER_2_NAME)
        )

    # Run game
    while True:
        if game.execute_turn(): # If game is over
            break

    print(f"\nFinal board:")
    game.board.draw_board()
    # If no legal moves, move count pits to players stores
    if game.legal_moves == []:
        p1_score, p2_score = game.board.score[game.board.player_1] + sum(game.board.board[game.board.player_1]), game.board.score[game.board.player_2] + sum(game.board.board[game.board.player_2])
    else:
        p1_score, p2_score = game.board.score[game.board.player_1], game.board.score[game.board.player_2]
    
    print(f"\nSCORE:\n{game.board.player_1.name}: {p1_score}\n{game.board.player_2.name}: {p2_score}")
    # game.winner = game.board.check_winner()
    if p1_score > p2_score:
        game.winner = game.board.player_1.name
    elif p1_score < p2_score:
        game.winner = game.board.player_2.name
    else:
        game.winner = "DRAW"
        
    print(f"\nWinner is {game.winner}")


if __name__ == "__main__":
    main()