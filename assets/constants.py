# GAME SETTINGS
PITS = 6 # Number of pits in each player board side
SEEDS = 4 # Number of seeds in each pit

# DO NOT MODIFY BELOW
LIST_LEN = PITS - 1 # Do not modify
HUMAN = 'Human'
COMPUTER = 'Computer'
RANDOM = 'Random'
# DO NOT MODIFY ABOVE


AI_DEPTH = 9 # Depth of AI model in turns
AI_MODEL = 'alphabeta' # Choice of AI model. Currently only minimax is viable

WHO_STARTS_GAME = 'Computer' # Valid values ['Human', 'Computer', 'Random']
BOARD_STARTING_STATE =  None #{HUMAN : [4, 4, 0, 0, 5, 5], COMPUTER : [5, 5, 4, 4, 4, 4]}
