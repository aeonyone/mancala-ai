from assets.game import Game
from assets.player import Player
from assets.constants import *


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