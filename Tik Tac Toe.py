import random

def display_board(board): # displays the board
    print("  |   |  ")
    print(board[7]+" | "+board[8]+" | "+board[9])
    print("  |   |  ")
    print("----------")
    print("  |   |  ")
    print(board[4]+" | "+board[5]+" | "+board[6])
    print("  |   |  ")
    print("----------")
    print("  |   |  ")
    print(board[1]+" | "+board[2]+" | "+board[3])
    print("  |   |  ")
    print("\n\n___________________________________________________\n\n")
    
def player_input(): # Who is X or O and creates the marker
    marker = ''
    while not (marker == 'X' or marker == 'O'):
        marker = input('Player 1: Do you want to be X or O?\nEnter HERE: ').upper()

    if marker == 'X':
        return ('X', 'O')
    else:
        return ('O', 'X')
    
def place_marker(board, marker, position): # Places marker on the board
    board[position] = marker

def win_check(board, mark): # checks all possible combinations to see if someone has won
    return ((board[7] == mark and board[8] == mark and board[9] == mark) or # across the top
        (board[4] == mark and board[5] == mark and board[6] == mark) or # across the middle
        (board[1] == mark and board[2] == mark and board[3] == mark) or # across the bottom
        (board[7] == mark and board[4] == mark and board[1] == mark) or # down the left side
        (board[8] == mark and board[5] == mark and board[2] == mark) or # down the middle
        (board[9] == mark and board[6] == mark and board[3] == mark) or # down the right side
        (board[7] == mark and board[5] == mark and board[3] == mark) or # diagonal
        (board[9] == mark and board[5] == mark and board[1] == mark)) # diagonal

def choose_first(): # Determines which player goes first
    if random.randint(0,1) == 0:
        return "Player 1"
    else:
        return "Player 2"
    
def space_check(board, position): # Checks if a position on the board is taken or not (returns true if space is available)
    return board[position] != 'X' and board[position] != 'O'

def full_board_space_check(board):
    for i in range(1,10):
        if space_check(board, i):
            return False
        
    return True

def player_choice(board): # Asks the player for a position to place their marker
    position = 0
    while True:
        try:
            position = int(input('Choose a position from 1-9: '))
            if position in range(1,10) and space_check(board, position):
                return position
            else:
                print("Position not available or out of range.")
        except ValueError:
            print("Please enter a number between 1 and 9.")

def replay(): # Asks the player if they want to play again
    choice = input('Do you want to play again? Enter Y or N: ').upper()
    return choice == 'Y'

#start
board = ['#','1','2','3','4','5','6','7','8','9',]
test_board = ['#','1','X','3','4','5','6','7','8','9',]

print("\nWELCOME TO TIC TAC TOE!\n")
while True:
    board = ['#','1','2','3','4','5','6','7','8','9',]
    player1_marker, player2_marker = player_input() # gets the markers for the players

    turn = choose_first() # determines which player goes first
    print(turn + ' will go first.')

    play_game = input('Are you ready to play? Enter Y or N: ').upper()

    if play_game == 'Y':
        game_on = True
    else:
        game_on = False

    while game_on:
        if turn == 'Player 1':
            display_board(board)
            position = player_choice(board)# asks player 1 for a position
            place_marker(board, player1_marker, position)

            if win_check(board, player1_marker):#checks if player 1 has won
                display_board(board)
                print('Player 1 has won!')
                game_on = False
            else:
                if full_board_space_check(board): # checks if the board is full
                    display_board(board)
                    print("It's a draw!")
                    game_on = False
                else:
                    turn = 'Player 2'
        else:
            display_board(board)
            position = player_choice(board)# asks player 1 for a position
            place_marker(board, player2_marker, position)

            if win_check(board, player2_marker):#checks if player 2 has won
                display_board(board)
                print('Player 2 has won!')
                game_on = False
            else:
                if full_board_space_check(board): # checks if the board is full
                    display_board(board)
                    print("It's a draw!")
                    game_on = False
                else:
                    turn = 'Player 1'

    if not replay(): #breaks the loop if the player does not want to play again
        print("Thanks for playing!")
        break