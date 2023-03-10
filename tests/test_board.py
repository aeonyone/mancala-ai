import pytest
from copy import deepcopy
from assets.board import Board


class TestBoard:
    def init_board(self, board=None):
        return Board(board=board, player_1=True, player_2=False)

    def test_apply_move(self):
        # Invalid moves
        x = Board()
        with pytest.raises(ValueError):
            x.apply_move(True, 0)
            x.apply_move(True, 7)
            x.apply_move(True, "")
            x.apply_move(True, "a")
            x.apply_move(True, "1")
            x.apply_move(True, None)

        # Starting board
        sb = {True : [4, 4, 4, 4, 4, 4], False : [4, 4, 4, 4, 4, 4]}
        x = self.init_board(deepcopy(sb))
        extra_move = x.apply_move(True, 1)
        assert x.board == {True : [0, 5, 5, 5, 5, 4], False : [4, 4, 4, 4, 4, 4]}
        assert x.score == {True : 0, False : 0}
        assert extra_move == False
        x = self.init_board(deepcopy(sb))
        extra_move = x.apply_move(True, 2)
        assert x.board == {True : [4, 0, 5, 5, 5, 5], False : [4, 4, 4, 4, 4, 4]}
        assert x.score == {True : 0, False : 0}
        assert extra_move == False
        x = self.init_board(deepcopy(sb))
        extra_move = x.apply_move(True, 3)
        assert x.board == {True : [4, 4, 0, 5, 5, 5], False : [4, 4, 4, 4, 4, 4]}
        assert x.score == {True : 1, False : 0}
        assert extra_move == True
        x = self.init_board(deepcopy(sb))
        extra_move = x.apply_move(True, 4)
        assert x.board == {True : [4, 4, 4, 0, 5, 5], False : [5, 4, 4, 4, 4, 4]}
        assert x.score == {True : 1, False : 0}
        assert extra_move == False
        x = self.init_board(deepcopy(sb))
        extra_move = x.apply_move(True, 5)
        assert x.board == {True : [4, 4, 4, 4, 0, 5], False : [5, 5, 4, 4, 4, 4]}
        assert x.score == {True : 1, False : 0}
        assert extra_move == False
        x = self.init_board(deepcopy(sb))
        extra_move = x.apply_move(True, 6)
        assert x.board == {True : [4, 4, 4, 4, 4, 0], False : [5, 5, 5, 4, 4, 4]}
        assert x.score == {True : 1, False : 0}
        assert extra_move == False

        # Simple capture
        x = self.init_board({True : [1, 0, 0, 0, 0, 0], False : [0, 0, 0, 0, 1, 0]})
        extra_move = x.apply_move(True, 1)
        assert x.board == {True : [0, 0, 0, 0, 0, 0], False : [0, 0, 0, 0, 0, 0]}
        assert x.score == {True : 2, False : 0}
        assert extra_move == False
        x = self.init_board({True : [5, 0, 0, 0, 0, 0], False : [1, 0, 0, 0, 0, 0]})
        extra_move = x.apply_move(True, 1)
        assert x.board == {True : [0, 1, 1, 1, 1, 0], False : [0, 0, 0, 0, 0, 0]}
        assert x.score == {True : 2, False : 0}
        assert extra_move == False
        # Go around capture
        x = self.init_board({True : [0, 0, 0, 0, 0, 8], False : [0, 0, 0, 0, 0, 0]})
        extra_move = x.apply_move(True, 6)
        assert x.board == {True : [0, 0, 0, 0, 0, 0], False : [1, 1, 1, 1, 1, 0]}
        assert x.score == {True : 3, False : 0}
        assert extra_move == False
        # Go around without capture
        x = self.init_board({True : [1, 0, 0, 0, 0, 8], False : [0, 0, 0, 0, 0, 0]})
        extra_move = x.apply_move(True, 6)
        assert x.board == {True : [2, 0, 0, 0, 0, 0], False : [1, 1, 1, 1, 1, 1]}
        assert x.score == {True : 1, False : 0}
        assert extra_move == False
        # Full circle capture
        x = self.init_board({True : [0, 0, 0, 13, 0, 0], False : [0, 0, 0, 0, 0, 0]})
        extra_move = x.apply_move(True, 4)
        assert x.board == {True : [1, 1, 1, 0, 1, 1], False : [1, 1, 0, 1, 1, 1]}
        assert x.score == {True : 3, False : 0}

    def test_evaluate_position(self):
        pass

    def test_heuristic_value(self):
        # N == N test for single player
        x = self.init_board({True : [6, 5, 4, 3, 2, 1], False : [0, 0, 0, 0, 0, 0]})
        assert x.heuristic_value(True) - x.heuristic_value(False) == 11
        # N == N test for both players
        x = self.init_board({True : [6, 5, 4, 3, 2, 1], False : [6, 5, 4, 3, 2, 1]})
        assert x.heuristic_value(True) - x.heuristic_value(False) == 0
        # Test 1 pit clear
        x = self.init_board({True : [0, 0, 0, 0, 0, 1], False : [0, 0, 0, 0, 0, 0]})
        assert x.heuristic_value(True) - x.heuristic_value(False) == 1
        # Test 2 pits clear
        x = self.init_board({True : [0, 0, 0, 0, 2, 1], False : [0, 0, 0, 0, 0, 0]})
        assert x.heuristic_value(True) - x.heuristic_value(False) == 3
        # Test 3 pits clear
        x = self.init_board({True : [0, 0, 0, 3, 1, 1], False : [0, 0, 0, 0, 0, 0]})
        assert x.heuristic_value(True) - x.heuristic_value(False) == 5
        # Test that N - 1 pit clear logic is not doublecounted after N pit clear
        x = self.init_board({True : [0, 0, 4, 3, 1, 1], False : [0, 0, 0, 0, 0, 0]})
        assert x.heuristic_value(True) - x.heuristic_value(False) == 7
        # Test 4 pits clear
        x = self.init_board({True : [0, 0, 4, 2, 0, 1], False : [0, 0, 0, 0, 0, 0]})
        assert x.heuristic_value(True) - x.heuristic_value(False) == 7
        # Test 4 pits clear and N == N
        x = self.init_board({True : [0, 0, 4, 2, 0, 1], False : [0, 0, 4, 0, 0, 1]})
        assert x.heuristic_value(True) - x.heuristic_value(False) == 4