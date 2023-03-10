#### Description:
This is Mancala CLI game in active development.

The mancala games are a family of two-player turn-based strategy board games played with small stones, beans, or seeds and rows of holes or pits in the earth, a board or other playing surface. The objective is usually to capture all or some set of the opponent's pieces. This project implements a Kalah variant of game.


#### Configuration
To configure game, edit constants.py

#### Play
To play, execute following command in the directory. "-u" option is recommended to avoid buffering stdout streams and improve responsiveness.
```
py -u main.py
```
Select turn by inputting numbers 1 to 6. On the second turn it is also possible to input 0 to turn the board according to pie rule.
