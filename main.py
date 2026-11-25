import numpy as np
board=np.zeros([3,3],dtype=int)
print(board)
def print_board(b):
    symbols = {0: " ", 1: "X", -1: "O"}

    for r in range(3):
        row = " | ".join(symbols[val] for val in b[r])
        print(" " + row)

        if r < 2:
            print("---+---+---")
print_board(board)
def counter(b):
    if 3 in np.sum(b,axis=1) or 3 in np.sum(b,axis=0):
        return "X"
    if -3 in np.sum(b,axis=1) or -3 in np.sum(b,axis=0):
        return "O"
    if  np.trace(b)==3 or np.trace(np.fliplr(b))==3:
        return "X"
    if  np.trace(b)==-3 or np.trace(np.fliplr(b))==-3:
        return "O"
    if not 0 in b:
        return "DRAW"
    return None
current=1
print("welcome to the tic tao game")

while True:
    if current==1:
        player='X'
    else:
        player='O'
    try:
        row=int(input(f"{player}-enter the row(0,1,2)"))
        col=int(input(f"{player}-enter the column(0,1,2)"))
    except Exception as err:
        print(err)
        continue
    if row<0 or row>2 or col<0 or col>2:
        print("Enter valid number for row and column")
    if board[row,col]!=0:
        print("Cell is full !")
    board[row,col]=current
    result=counter(board)
    print_board(board)

    if result is not None:
        if result=='DRAW':
            print("oops its a draw.")
        else:
            print(f"{result}wins")
        break
    if current==1:
        current=-1
    else:
        current=1
   

