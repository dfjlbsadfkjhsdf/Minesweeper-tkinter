import random
from tkinter import *
from tkinter import ttk

mines = 15

board = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

for _ in range(mines):
    row = board[random.randint(0,9)]
    row[random.randint(0,9)] = 1

# WINDOW SETUP

root = Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()

# MINES TOUCHING TILE

def checkMines(cell):
    numberOfMines = 0
    column = cell.grid_info()['column']
    row = cell.grid_info()['row']
    tilesAroundCell = [
        board[row][column-1],
        board[row-1][column],
        board[row+1][column],
        board[row][column+1],
        board[row-1][column-1],
        board[row-1][column+1],
        board[row+1][column-1],
        board[row+1][column+1]
    ]
    for tile in tilesAroundCell:
        if tile == 1:
            numberOfMines += 1
    return numberOfMines

# UNCOVER TILES

def uncoverTiles(cell):
    for tile in reversed(frame.grid_slaves()):
        # up check
        if tile.grid_info()['row'] == cell.grid_info()['row'] - 1  and tile.grid_info()['column'] == cell.grid_info()['column']:
            up = tile
            try:
                number = checkMines(up)
            except:
                continue
            up.config(text=number)
            if number == 0:
                print('Zero mines above tile')
                pass # RE RUN FUNC WHEN ITS DONE
        
# CELL CLICKED

def cellClicked(cellCount, rowCount):
    for cell in reversed(frame.grid_slaves()):
        if cell.grid_info()['row'] == rowCount and cell.grid_info()['column'] == cellCount:
            number = checkMines(cell)
            cell.config(text=number)
            uncoverTiles(cell)

# BOARD SETUP

rowCount = 0
cellCount = 0
for row in board:
    for cell in row:
        if cell == 1:
            Button(frame, text="?", width=3, command=root.destroy).grid(column=cellCount, row=rowCount)
        else:
            Button(frame, text="?", width=3, command=lambda c = cellCount, r = rowCount: cellClicked(c, r)).grid(column=cellCount, row=rowCount)
        cellCount += 1
    rowCount += 1
    cellCount = 0

root.mainloop()
