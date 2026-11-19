# MINESWEEPER
#### Video Demo:  <URL HERE>
#### Description: This project is a recreation of minesweeper in python using tkinter to display the Gui. The project opens with a window prompting the user to input the number of rows, columns and mines they would like on the board. When the user is happy with their setup, they can press the go button at the bottom of the window to begin playing. Upon clicking this button, the widgets are destroyed and new ones are created displaying the board, number of flags and a restart button.

#### The user may now click on one of the tiles on the board to uncover it. When the user does this, the program checks every tile around it to see if it is a mine. If it is, it will increase the number on the tile by one. Once the program is done with this check the tile will be uncovered and the number will be visible. If this number is zero, the program will automatically uncover all the tiles around it that are also zero; this mechanic is called autofill.

#### If the user feels that there is a mine on a specific tile, they can place a flag by right-clicking to mark the tile. If the user right-clicks the tile again the flag will be removed. The user can only place as many flags as their are mines. If the user attempts to place another flag and they have ran out of flags to place, nothing will happen.
