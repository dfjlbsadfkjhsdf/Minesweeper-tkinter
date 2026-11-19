import random
from tkinter import *
from tkinter import ttk

flagsLeft = None
flagCounter = 'Placeholder' # this is so I can edit the variable inside the place flags function without it breaking

root = Tk()
root.title('Minesweeper')
frame = ttk.Frame(root, padding=5)
frame.grid()

board = []

colours = {
    0 : '#ffffff',
    1 : '#2274bd',
    2 : '#2cbd22',
    3 : '#e81313',
    4 : '#361280',
    5 : '#fa9e0a',
    6 : "#0cce8d",
    7 : '#0a0000',
    8 : '#e8c5c5'
} 

def placeFlag(_, cellCount, rowCount):
    global flagsLeft
    global flagCounter

    
    for cell in reversed(frame.grid_slaves()):
        if cell.grid_info()['row'] == rowCount and cell.grid_info()['column'] == cellCount:
            if cell['text'] == '🚩':
                cell.config(text='?')
                flagsLeft += 1
            else:
                if cell['text'] != '?':
                    return
                if flagsLeft <= 0:
                    return
                cell.config(text='🚩')
                flagsLeft -= 1

    flagCounter.config(text=flagsLeft)
    return 'flag placed correctly'
    
def createBoard(rows, columns, mines):
    if not rows or not columns or not mines:
        rows = 10
        columns = 10
        mines = 10
    if int(rows) * int(columns) > 1000:
        Label(root, text='Too many rows/columns', fg=colours[3]).grid(row=5, column=0)
        return
    if int(mines) > int(rows) * int(columns):
        Label(root, text='Too many mines', fg=colours[3]).grid(row=5, column=0)
        return
    if int(rows) * int (columns) <= 0:
        Label(root, text='Too few rows/columns', fg=colours[3]).grid(row=5, column=0)
        return
    global boardRows
    global boardColumns
    global boardMines
    global flagCounter
    global flagsLeft

    boardRows = rows
    boardColumns = columns
    boardMines = mines

    rows = int(rows)
    columns = int(columns)
    mines = int(mines)

    global board
    board = []

    rowCount = 0
    cellCount = 0
    flagsLeft = mines

    for _ in range(rows):
        board.insert(-1,[])

    for row in board:
        for _ in range(columns):
            row.insert(-1, '0')

    for _ in range(mines):
        row = board[random.randint(0, (rows - 1))]
        row[random.randint(0, (columns - 1))] = 1

    for i in root.winfo_children():
        if i == frame:
            continue
        i.destroy()
    
    for row in board:
        for _ in row:
            btn = Button(frame, text="?", bg="#a8e742", width=3, command=lambda c = cellCount, r = rowCount: cellClicked(c, r))
            btn.bind('<Button-3>', lambda e = None, c = cellCount, r = rowCount: placeFlag(e,c,r))
            btn.grid(column=cellCount, row=rowCount)
            cellCount += 1
        rowCount += 1
        cellCount = 0

    Button(root, text="R", width=3, command=resetBoard).grid(column=0, row=1)
    flagCounter = Label(root, text=flagsLeft, width=6)
    flagCounter.grid(column=1, row=1)
    return 'Board created successfully'

def resetBoard():
    for button in frame.grid_slaves():
        button.destroy()
    createBoard(boardRows, boardColumns, boardMines)

def checkMines(cell):
    numberOfMines = 0
    column = cell.grid_info()['column']
    row = cell.grid_info()['row']
    tilesAroundCell = [
        'board[row][column-1]',   #left
        'board[row-1][column]',   #up
        'board[row+1][column]',   #down
        'board[row][column+1]',   #right
        'board[row-1][column-1]', #top left
        'board[row-1][column+1]', #top right
        'board[row+1][column-1]', #bottom left
        'board[row+1][column+1]'  #bottom right
    ]
    for i, v in enumerate(tilesAroundCell):
        try:
            tilesAroundCell[i] = eval(v)
            if tilesAroundCell[i] == 0:
                continue
            if ('column-1' in v and (column-1 < 0)) or ('row-1' in v and (row-1 < 0)):
                tilesAroundCell[i] = None
                continue
        except IndexError:
            tilesAroundCell[i] = None
    
    for tile in tilesAroundCell:
        if tile == 1:
            numberOfMines += 1
        elif tile == None:
            continue
    return numberOfMines
    
def uncoverTiles(row, col):
    try:
        for tile in reversed(frame.grid_slaves()):
            if tile.grid_info()['row'] == row and tile.grid_info()['column'] == col:
                if board[tile.grid_info()['row']][tile.grid_info()['column']] == 1:
                    return
                if tile['text'] == '🚩':
                    return
                number = checkMines(tile)
                if number == 0:
                    uncoverTiles(tile.grid_info()['row'], tile.grid_info()['column']-1)
                    uncoverTiles(tile.grid_info()['row']-1, tile.grid_info()['column'])
                    tile.config(text='', bg='#d6e285')
                    return
                tile.config(text=number, fg=colours[number], bg="#cedf60")
    except:
        return

def loseEvent():
    newWindow = Toplevel(root)
    newWindow.title('You Lose!')
    newWindow.geometry('200x250')
    Label(newWindow, text='You Lose!', font=40).pack(pady=15)
    Button(newWindow, text="Retry?", command=resetBoard).pack(pady=30)

def winEvent():
    newWindow = Toplevel(root)
    newWindow.title('You Win!')
    newWindow.geometry('200x250')
    Label(newWindow, text='You Win!', font=40).pack(pady=15)
    Button(newWindow, text="Retry?", command=resetBoard).pack(pady=30)
    return 'Win window successfully created'

def cellClicked(cellCount, rowCount):
    winning = True
    for cell in reversed(frame.grid_slaves()):
        if cell.grid_info()['row'] == rowCount and cell.grid_info()['column'] == cellCount:
            if cell['text'] != '?':
                return
            if board[cell.grid_info()['row']][cell.grid_info()['column']] == 1:
                loseEvent()
                return
            number = checkMines(cell)
            if number == 0:
                cell.config(text='', bg='#d6e285')
            else:
                cell.config(text=number, fg=colours[number], bg="#cedf60")
            uncoverTiles(cell.grid_info()['row'], cell.grid_info()['column']-1) # this is really ugly but I couldnt think of a better way to do it
            uncoverTiles(cell.grid_info()['row']-1, cell.grid_info()['column'])
            uncoverTiles(cell.grid_info()['row']+1, cell.grid_info()['column'])
            uncoverTiles(cell.grid_info()['row'], cell.grid_info()['column']+1)
            uncoverTiles(cell.grid_info()['row']-1, cell.grid_info()['column']-1)
            uncoverTiles(cell.grid_info()['row']-1, cell.grid_info()['column']+1)
            uncoverTiles(cell.grid_info()['row']+1, cell.grid_info()['column']-1)
            uncoverTiles(cell.grid_info()['row']+1, cell.grid_info()['column']+1)
        if board[cell.grid_info()['row']][cell.grid_info()['column']] == '0' and cell['text'] == '?':
            winning = False
    if winning == True:
        winEvent()
    return winning
    
def main():
    row = StringVar()
    column = StringVar()
    mine = StringVar()
    Label(root, text='Select board dimensions: ').grid(column=0, row=0) # title
    Entry(root, textvariable=row).grid(row=1, column=1) # row entry
    Entry(root, textvariable=column).grid(row=2, column=1) # column entry
    Entry(root, textvariable=mine).grid(row=3, column = 1) # mines entry
    Label(root, text='Rows: ').grid(row=1, column=0) # row label
    Label(root, text='Columns: ').grid(row=2, column=0) # column label
    Label(root, text='Mines: ').grid(row=3, column=0) # mines label
    Button(root, text='Go!', command=lambda: createBoard(row.get(), column.get(), mine.get())).grid(row=4, column=0) # go button
    return 'Main menu successfully created'

if __name__ == '__main__':
    main()
    root.mainloop()
