from utilities import place_random, print_board
import copy

DEV_MODE = False

def win(game_board):
    for row in game_board:
        for i in row:
            if i == 2048:
                return True
    return False

def up(game_board):
    for i in range(4):
        for x in range(i, 4):
            if i != x:
                val = game_board[i][x]
                game_board[i][x] = game_board[x][i]
                game_board[x][i] = val
    left(game_board)
    for i in range(4):
        for x in range(i, 4):
            if i != x:
                val = game_board[i][x]
                game_board[i][x] = game_board[x][i]
                game_board[x][i] = val
    return game_board
    
def down(game_board):
    for i in range(4):
        for x in range(i, 4):
            if i != x:
                val = game_board[i][x]
                game_board[i][x] = game_board[x][i]
                game_board[x][i] = val
    right(game_board)
    for i in range(4):
        for x in range(i, 4):
            if i != x:
                val = game_board[i][x]
                game_board[i][x] = game_board[x][i]
                game_board[x][i] = val
    

    

def right(game_board):
    for row in game_board:
        row.reverse()
        for y in range(3):
            for x in range(3, 0, -1):
                if row[x-1] == 0:
                    row[x-1] = row[x]
                    row[x] = 0
        for i in range(3): #merge
            if row[i] == row[i+1]:
                row[i] = row[i] + row[i+1]
                row[i+1] = 0
        for x in range(3, 0, -1): #shift 
            if row[x-1] == 0:
                row[x-1] = row[x]
                row[x] = 0    
        row.reverse()
    return game_board
    


def left(game_board):
    for row in game_board:
        for y in range(3):
            for x in range(3, 0, -1):
                if row[x-1] == 0:
                    row[x-1] = row[x]
                    row[x] = 0
        for i in range(3): #merge
            if row[i] == row[i+1]:
                row[i] = row[i] + row[i+1]
                row[i+1] = 0
        for x in range(3, 0, -1): #shift 
                if row[x-1] == 0:
                    row[x-1] = row[x]
                    row[x] = 0    
    return game_board   
        
    



def main(game_board: [[int, ], ]) -> [[int, ], ]:
    """
    2048 main function, runs a game of 2048 in the console.

    Uses the following keys:
    w - shift up
    a - shift left
    s - shift down
    d - shift right
    q - ends the game and returns control of the console
    :param game_board: a 4x4 2D list of integers representing a game of 2048
    :return: returns the ending game board
    """
    # Initialize board's first cell

    # You are not required to implement develop mode, but it is encouraged to do so.
    # Develop mode allows you to input the location of the next piece that will be
    # placed on the board, rather than attempting to debug your code with random
    # input values.
    if DEV_MODE:
        # This line of code handles the input of the develop mode.
        column, row, value = (int(i) for i in input("column,row,value:").split(','))

        # OPTIONAL: place the piece in the corresponding cell on the game board
        game_board[row][column] = value 
    else:
        values = place_random(game_board) #{row: 0, column: 0, value: 2}
        #store the dictionary values
        game_board[values['row']][values['column']] = values['value']
        

    # Initialize game state trackers

    # Game Loop
    user = False
    while True:
        board = copy.deepcopy(game_board)
        if user:
            user_input = input('Enter w, a, s, d, or q')
            if user_input not in ('w', 'a', 's', 'd', 'q'):
                while user_input not in ('w', 'a', 's', 'd', 'q'):
                    user_input = input('Please enter valid keys. Enter w, a, s, d, or q')
            if user_input == 'q':
                print('Goodbye')
                break
            elif user_input == 'w':
                game_board = up(game_board)
            elif user_input == 'a':
                game_board = left(game_board)
            elif user_input == 's':
                game_board = down(game_board)
            elif user_input == 'd':
                game_board = right(game_board)
            if game_board == board:
                while game_board == board:
                    user_input = input('Please try again. Enter w, a, s, d, or q')
                    if user_input not in ('w', 'a', 's', 'd', 'q'):
                        while user_input not in ('w', 'a', 's', 'd', 'q'):
                            user_input = input('Please enter valid keys. Enter w, a, s, d, or q')
                    if user_input == 'q':
                        print('Goodbye')
                        break
                    elif user_input == 'w':
                        game_board = up(game_board)
                    elif user_input == 'a':
                        game_board = left(game_board)
                    elif user_input == 's':
                        game_board = down(game_board)
                    elif user_input == 'd':
                        game_board = right(game_board)
            
            
            user = False
        else:
            values = place_random(game_board) #{row: 0, column: 0, value: 2}
            #store the dictionary values
            game_board[values['row']][values['column']] = values['value']
            if game_over(game_board):
                print('The game is over, you have no moves left')
                break
            print_board(game_board)
            user = True
            
            
            
                    
            
            
        # TODO: Reset user input variable

        # TODO: Take computer's turn
        # place a random piece on the board
        # check to see if the game is over using the game_over function

        # TODO: Show updated board using the print_board function

        # TODO: Take user's turn
        
        # Take input until the user's move is a valid key
        # if the user quits the game, print Goodbye and stop the Game Loop
        # Execute the user's move

        # Check if the user wins
    return game_board


def game_over(game_board: [[int, ], ]) -> bool:
    #check if the board is still same after each merge
    board1 = copy.deepcopy(game_board)
    board2 = copy.deepcopy(game_board)
    board1 = down(board1)
    if board1 == board2:
        board1 = up(board1)
        if board1 == board2:
            board1 = left(board1)
            if board1 == board2:
                board1 = right(board1)
                if board1 == board2:
                    return True 
    return False
    
        
    
    """
    Query the provided board's game state.

    :param game_board: a 4x4 2D list of integers representing a game of 2048
    :return: Boolean indicating if the game is over (True) or not (False)
    """
    # TODO: Loop over the board and determine if the game is over
    # TODO: Don't always return false


if __name__ == "__main__":
    main([[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]])
