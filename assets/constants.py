# GAME SETTINGS
PITS = 6 # Number of pits in each player board side
SEEDS = 4 # Number of seeds in each pit


LIST_LEN = PITS - 1 # Do not modify
# Change to PLAYER_1 and PLAYER_2
PLAYER_1 = 'Computer1' # Do not modify
PLAYER_2 = 'Computer2' # Do not modify
RANDOM = 'Random' # Do not modify



AI_DEPTH = 6 # Depth of AI model in turns
AI_MODEL = 'minimax' # Choice of AI model. Currently only minimax is viable

WHO_STARTS_GAME = 'Random' # Valid values [PLAYER_1, PLAYER_2, 'Random']
BOARD_STARTING_STATE =  None #{PLAYER_1 : [0, 0, 0, 1, 8, 0], PLAYER_2 : [0, 0, 0, 0, 0, 9]}
