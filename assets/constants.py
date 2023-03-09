# GAME SETTINGS
PITS = 6 # Number of pits in each player board side
SEEDS = 4 # Number of seeds in each pit


LIST_LEN = PITS - 1 # Do not modify
# Change to PLAYER_1 and PLAYER_2
PLAYER_1_TYPE = 'Human' # Valid values [Human, Computer]
PLAYER_1_NAME = 'Caro Kann' # Do not modify
PLAYER_2_TYPE = 'Computer' # Valid values [Human, Computer]
PLAYER_2_NAME = 'Randy' # Do not modify
RANDOM = 'Random' # Do not modify



AI_DEPTH = 6 # Depth of AI model in turns
AI_MODEL = 'minimax' # Choice of AI model. Currently only minimax is viable

WHO_STARTS_GAME = 'Player 1' # Valid values [PLAYER_1, PLAYER_2, 'Random']
BOARD_STARTING_STATE = None #{'Player 1' : [0, 0, 0, 1, 0, 1], 'Player 2' : [1, 1, 5, 1, 7, 0]}
RANDOM_AI = False # Returns random computer moves if True