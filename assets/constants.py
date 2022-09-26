# GAME SETTINGS
PITS = 6 # Number of pits in each player board side
SEEDS = 4 # Number of seeds in each pit

AI_DEPTH = 7 # Depth of AI model in turns
AI_MODEL = 'minimax' # Choice of AI model. Currently only minimax is viable

WHO_STARTS_GAME = 'Human' # Valid values ['Human', 'Computer', 'Random']
BOARD_STARTING_STATE =  None # {HUMAN : [0, 0, 0, 0, 0, 0], COMPUTER : [0, 0, 0, 0, 0, 0]}

# DO NOT MODIFY
LIST_LEN = PITS - 1 # Do not modify
HUMAN = 'Human'
COMPUTER = 'Computer'
RANDOM = 'Random'
