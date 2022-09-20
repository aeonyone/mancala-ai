from assets.constants import *
from assets.board import Board
from assets.model import Model
from assets.game import Game
from assets.tests import Tests



#TODO
    # See what minimax says is best response to some position at depth n 5 up to 10 and then check if alphabeta gives the same response
def main():
    # tests = Tests()
    return Tests().isModelValid('alphabeta')


main()