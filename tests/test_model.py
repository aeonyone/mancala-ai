class TestModel:
   # TODO
    def isModelValid(self, model):
        ## Define cases, [board, depth, expected]
        case = [
            # Depth 1
            [{True : [0, 0, 0, 0, 0, 0], False : [1, 1, 1, 1, 1, 1]}, 1, [6]], # Scoring preference
            [{True : [0, 1, 0, 0, 0, 0], False : [1, 0, 0, 1, 0, 1]}, 1, [4]], # Capture preference
            [{True : [0, 2, 0, 0, 1, 0], False : [1, 0, 0, 1, 0, 1]}, 1, [4]], # Larger capture preference
            # Depth 2
            [{True : [0, 2, 0, 0, 1, 0], False : [1, 0, 0, 1, 0, 1]}, 2, [6]], # Prefer scoring before capture
            [{True : [0, 2, 0, 0, 1, 0], False : [1, 0, 0, 1, 0, 0]}, 2, [1]], # Prefers score advantage over larger score
            [{True : [0, 5, 0, 2, 0, 0], False : [9, 1, 0, 1, 0, 0]}, 2, [2]],  # Prevents attack
            # Depth 3
            [{True : [1, 0, 1, 1, 0, 0], False : [3, 0, 1, 0, 2, 1]}, 3, [6]],  # Escapes attack
            [{True : [0, 0, 0, 1, 0, 1], False : [0, 5, 4, 0, 0, 1]}, 3, [3,6]],  # Chains moves
            [{True : [0, 4, 3, 0, 0, 0], False : [0, 1, 0, 0, 1, 4]}, 3, [2,5]],  # Denies oponnent chain
            [{True : [0, 4, 3, 0, 0, 0], False : [1, 0, 2, 0, 1, 0]}, 3, [1]],  # Defends
            # Depth 4
            [{True : [0, 0, 4, 2, 0, 0], False : [4, 1, 0, 0, 0, 1]}, 4, [6]],  # 
            [{True : [0, 0, 4, 1, 2, 8], False : [0, 3, 1, 0, 5, 0]}, 4, [5]],  # 
            [{True : [2, 4, 4, 0, 0, 0], False : [6, 4, 4, 0, 1, 0]}, 4, [1]],  # 
            [{True : [1, 4, 0, 4, 0, 0], False : [5, 5, 4, 4, 4, 4]}, 4, [3]],  # 
        ]
