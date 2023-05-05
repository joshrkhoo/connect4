"""
FIT1045: Sem 1 2023 Assignment 1
"""
import random
import os


def clear_screen():
    """
    Clears the terminal for Windows and Linux/MacOS.

    :return: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def print_rules():
    """
    Prints the rules of the game.

    :return: None
    """
    print("================= Rules =================")
    print("Connect 4 is a two-player game where the")
    print("objective is to get four of your pieces")
    print("in a row either horizontally, vertically")
    print("or diagonally. The game is played on a")
    print("6x7 grid. The first player to get four")
    print("pieces in a row wins the game. If the")
    print("grid is filled and no player has won,")
    print("the game is a draw.")
    print("=========================================")


def validate_input(prompt, valid_inputs):
    """
    Repeatedly ask user for input until they enter an input
    within a set valid of options.

    :param prompt: The prompt to display to the user, string.
    :param valid_inputs: The range of values to accept, list
    :return: The user's input, string.
    """

    # user_input is assigned to an input with the prompt string inside it
    user_input = input(prompt)
    # while whatever the user inputs is not in the list do the following
    while user_input not in valid_inputs:
        # print this string
        print("Invalid input, please try again.")
        # re ask for input from the user
        user_input = input(prompt)
    # return the user_input
    return user_input


def create_board():
    """
    Returns a 2D list of 6 rows and 7 columns to represent
    the game board. Default cell value is 0.

    :return: A 2D list of 6x7 dimensions.
    """

    # Assign variable 'row_num' to integer value of 6 (for 6 rows)
    row_num = 6
    # Assign variable of 'col_num' to integer value of 7
    col_num = 7

    # This will be the list for the board
    new_board = []

    # Iterates through range of row_num which is 6 (0-5)
    for row_index in range(row_num):
        # Assigning row to a list of 7 slots of 0s
        row = [0] * col_num

        # Append row to new_board 6 times 
        new_board.append(row)
    return new_board


def print_board(board):
    """
    Prints the game board to the console.

    :param board: The game board, 2D list of 6x7 dimensions.
    :return: None
    """
    # Assigning variables
    board_string = ""
    header = "========== Connect4 ========="
    players = "Player 1: X       Player 2: O"
    line_break = ""
    column_numbers = "  1   2   3   4   5   6   7"
    horizontal_line = " --- --- --- --- --- --- ---"
    footer = "============================="
    # \n = newline
    board_string = "\n".join([header, players, line_break, column_numbers, horizontal_line])

    # iterate through rows in the 2D array
    for row in board:

        # adds a | for every row (left most box only: column 0)
        board_string += "\n|"

        # Iterate through numbers in the row: 3 options (0, 1, 2)
        for num in row:
            # print(num)

            # Assign display character to the function: get_display_char(num)
            # Parameter of get_display_char(): num
            display_char = get_display_char(num)

            # Adds an f string to board_string
            # f string uses f at the beginning followed by quotation marks plus curly braces with expressions inside 
            # which are replaced with their assigned values
            # in this case the characters to be displayed: (" ", O, X)
            board_string += f" {display_char} |"

        # Add horizontal line for each row
        board_string += ("\n" + horizontal_line)
    # Add footer
    board_string += ("\n" + footer)
    # Prints the board_string at their positions
    print(board_string)


def get_display_char(num):
    """
    Gets display character for a number on the board
    :param num: The player's number

    :return: The player's token character to be displayed
    """
    # If the num in a slot equals 0 return an empty string
    if num == 0:
        return " "
    # Return "X" if a slot in in the board equals 1 otherwise return "0"
    return "X" if num == 1 else "O"


def drop_piece(board, player, column):
    """
    Drops a piece into the game board in the given column.
    Please note that this function expects the column index
    to start at 1.

    :param board: The game board, 2D list of 6x7 dimensions.
    :param player: The player who is dropping the piece, int.
    :param column: The index of column to drop the piece into, int.
    :return: True if piece was successfully dropped, False if not.
    """
    row_index_to_check = 5  # start checking from bottom-most row, check bottom-up
    col_index_to_check = column - 1  # index of first column is 0, while player input is 1
    while row_index_to_check >= 0:
        slot_to_check = board[row_index_to_check][col_index_to_check]
        if slot_to_check == 0:
            # Assign the slot to the specified player if slot is empty (0)
            board[row_index_to_check][col_index_to_check] = player
            return True
        row_index_to_check -= 1
    return False  # If all columns are full


def execute_player_turn(player, board):
    """
    Prompts user for a legal move given the current game board
    and executes the move.

    :return: Column that the piece was dropped into, int.
    """

    # Initialize the drop to unsuccessful
    drop_successful = False

    # While the drop is not successful do this...
    while not drop_successful:

        # Column choice is assigned function validate input, prompting the specific player
        validated_col_option = validate_input(
            f'Player {player}, please enter the column you would like to drop your piece into: ',
            ['1', '2', '3', '4', '5', '6', '7'])

        # Reassign drop_successful to drop_piece()
        drop_successful = drop_piece(board, player, int(validated_col_option))

        # If the drop is successful then return that column, else print(...)
        if drop_successful:
            return validated_col_option
        print('That column is full, please try again.')


def end_of_game(board):
    """
    Checks if the game has ended with a winner
    or a draw.

    :param board: The game board, 2D list of 6 rows x 7 columns.
    :return: 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins, 3 if draw.
    """

    # check if player has won
    # Assigning the variable player_has_won to the function get_winning_player (invoking the function)
    player_has_won = get_winning_player(
        board)  # this is either 0, 1 or 2 (0: no winner, 1: Player 1 won, 2: Player 2 won)

    # If player_has_won returned a 1 or 2 return that number (winning player)
    if player_has_won != 0:
        return player_has_won

    # board is full
    if board_is_full(board):
        return 3

    # game is not over
    return 0


def board_is_full(board) -> bool:
    """
    Checks if the board is full

    :param board: The game board, 2D list of 6 rows x 7 columns.
    :return: true if full else false
    """

    """
    check every number slot in board
    if any slot has a 0 then return false
    if no slot is 0 return True
    """

    # Iterate through rows
    for row in board:
        # Iterate through each number in each row
        for num in row:
            # If any number in each row is a 0 (empty) return False (game is not over),
            # otherwise if no number is 0 then return True (game is over: Draw)
            if num == 0:
                return False
    return True


def get_winning_player(board) -> int:
    """
    Checks if there is a winning player

    :param board: The game board, 2D list of 6 rows x 7 columns.
    :return: 0 if no winner, 1 if player 1 wins, 2 if player 2 wins
    """
   

    # Checking for horizontal win
    for row in board:

        # we subtract 3 from the length of the row as we only need to check 4 adjacent slots
        # For example if we look at a row: [0, 0, 0, 0, 0, 0, 0]
        # if we start at i=0, the first 4 slots will be checked: (0,1,2,3)
        # if we then go to i=1, indexes 1,2,3,4 will be checked
        # continuing this cycle we want to stop when we cant check 4 slots,
        # (i.e when i= 4, 5, 6) otherwise out of range error will occur
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == 1:
                return 1
            elif row[i] == row[i + 1] == row[i + 2] == row[i + 3] == 2:
                return 2

    # Checking for vertical win 
    # this will be the range of the first row, as board[0] is row 1
    # so we are iterating through the range of 7 (0 to 6)
    for i in range(len(board[0])):

        # Remember that length of board is the number of rows in the board. (board is a list of lists)
        # subtract 3 is same reason for testing horizontally 
        for j in range(len(board) - 3):
            # print(len(board)): will output 6 for 6 rows

            # index 'j' increments for each test as we are moving down 1 row for every j+1 (testing vertically)
            if board[j][i] == board[j + 1][i] == board[j + 2][i] == board[j + 3][i] == 1:
                return 1
            elif board[j][i] == board[j + 1][i] == board[j + 2][i] == board[j + 3][i] == 2:
                return 2

    # Checking diagonal wins
    # subtract 3 from length of board as only need to iterate to 3rd row
    # at rows 4-6, and go diagonally down to the right there are only 3, 2, and 1 blocks adjacent (so cannot be any wins here)
    for i in range(len(board) - 3):

        # 7 elements in each row. last element where there can be a win diagonally to the right is at board[0][3], i.e element 4
        # from elements 5-7, check diagonally down to the right, there are only 3, 2 and 1 blocks respectively adjacent
        for j in range(len(board[0]) - 3):

            """
            these 'for loops' have created a rectangular frame to scan through: 4 to the right and 3 down 
            in the board starting at [0][0] (as a range for where diagonals can be checked from)
            - the same will be done for checking diagonals from right to left
            """

            # right to left diagonal win

            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == 1:
                return 1
            elif board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == 2:
                return 2

            # left to right diagonal win
            # -j as we want to start from right side (i.e board[0][6])
            # if j = 0, then -j = -0
            # if j = 1, then -j = -1
            # so on
            # i remains the same as adding 1 to the index will still go down a row

            if board[i][-j - 1] == board[i + 1][-j - 2] == board[i + 2][-j - 3] == board[i + 3][-j - 4] == 1:
                return 1
            elif board[i][-j - 1] == board[i + 1][-j - 2] == board[i + 2][-j - 3] == board[i + 3][-j - 4] == 2:
                return 2

    # Return 0 (no winner yet): this is outside each 'for loop' (let loops iterate first, if no winner found then only return 0)
    return 0


def local_2_player_game():
    """
    Runs a local 2 player game of Connect 4.

    :return: None
    """
    # invoking the function create_board()
    board = create_board()

    # initial player is assigned 1
    current_player = 1
    # There is no previous column choice to tell players
    prev_col_choice = None

    while True:
        clear_screen()
        # execute the turn
        print_board(board)

        # if there was a previous move (turn 1 has no previous move), then print that out
        if prev_col_choice:
            # '2 if current_player==1 else 1' only switches player inside print function
            print(f'Player {2 if current_player == 1 else 1} has dropped in {prev_col_choice}')

        prev_col_choice = execute_player_turn(current_player, board)

        check_winner = end_of_game(board)
        if check_winner == 1:
            clear_screen()
            print_board(board)
            print("Player 1 wins")
            break
        elif check_winner == 2:
            clear_screen()
            print_board(board)
            print("Player 2 wins")
            break
        elif check_winner == 3:
            clear_screen()
            print_board(board)
            print("Draw")
            break

        # change the Player
        current_player = 2 if current_player == 1 else 1


def main():
    """
    Defines the main application loop.
    User chooses a type of game to play or to exit.

    :return: None
    """
    menu_string = """=============== Main Menu ===============
Welcome to Connect 4!
1. View Rules
2. Play a local 2 player game
3. Play a game against the computer
4. Exit
=========================================
Enter a number: """

    clear_screen()
    while True:

        # Ask user for an option (1-4) as stated in the menu string above
        user_input = validate_input(
            prompt=menu_string,
            valid_inputs=["1", "2", "3", "4"]
        )
        # Print rules
        if user_input == "1":
            clear_screen()
            print_rules()
        # Plays local game
        if user_input == "2":
            return local_2_player_game()
        # Plays ai game
        if user_input == "3":
            return game_against_cpu()
        # Quits game
        if user_input == "4":
            print("You have exited the game")
            return


def cpu_player_easy(board, player):
    """
    Executes a move for the CPU on easy difficulty. This function 
    plays a randomly selected column.

    :param board: The game board, 2D list of 6x7 dimensions.
    :param player: The player whose turn it is, integer value of 1 or 2.
    :return: Column that the piece was dropped into, int.
    """

    # Initially cpu has not dropped a piece
    cpu_has_dropped = False
    # While cpu has not dropped
    while not cpu_has_dropped:
        # Choose a random column 
        ran_int = random.randint(1, 7)
        # Drop cpu piece into that column
        cpu_has_dropped = drop_piece(board, player, ran_int)
        # if drop_piece() returned True then return ran_int otherwise keep looping
        if cpu_has_dropped:
            return ran_int


def clone_board(board):
    """
    Creates a deep clone of the param board

    :param board: the board
    :return: cloned board
    """
    # create board of same number of rows and height
    cloned_board = create_board()
    # for each item in the param board, copy over to cloned board

    # for each row
    for i in range(len(board)):
        # for each value in each row
        for j in range(len(board[0])):
            # cloning the values in each slot in real board to cloned board (mimicking the real board to check wins)
            cloned_board[i][j] = board[i][j]
    return cloned_board

    # return the cloned board


def get_winning_place(board, player):
    """
    This function checks for an immediate win and plays that move if possible
    This function will take precedence over get_blocking_piece()
   
    :param board: The game board, 2D list of 6x7 dimensions.
    :param player: The player whose turn it is, integer value of 1 or 2.
    :return: Column of the winning place or none if there is no winning place
    """
    for j in range(len(board[0])):  # for each column
        cloned_board = clone_board(board)  # clone the board
        cpu_drop = drop_piece(cloned_board, player, j)  # drop the piece into the cloned board
        if cpu_drop:
            if get_winning_player(cloned_board) == player:  # if there is a win in the simulated instance
                drop_piece(board, player, j)  # drop the piece into the read board
                return j  # return the column of the winning place

    # There is no winning place
    return None


def get_blocking_place(board, player):
    """
    This function checks if the opponent (human player) is about to win and blocks it
    If the opponent has multiple ways of winning this function will block the first one it sees
    Please note  this function accepts player in favour if the block, then switches to the opponent to simulate their win

    :param board: The game board, 2D list of 6x7 dimensions.
    :param player: The player whose turn it is, integer value of 1 or 2.
    :return: The column of the blocking place or none if there is no win to bloc
    """

    # for each col
    # clone the board
    # drop the piece into the cloned board
    # if this piece blocks a win in the clone board
    # it will then be dropped into the real board in order to block the opponents piece in real time
    # if there is no win to block then return None and continue playing

    # check opponent block
    for j in range(len(board[0])):
        cloned_board = clone_board(board)
        opponent = 2 if player == 1 else 1
        player_win = drop_piece(cloned_board, opponent, j)
        if player_win:
            if get_winning_player(cloned_board) == opponent:
                drop_piece(board, player, j)
                return j
    return None


def cpu_player_medium(board, player):
    """
    Executes a move for the CPU on medium difficulty.
    It first checks for an immediate win and plays that move if possible. 
    If no immediate win is possible, it checks for an immediate win 
    for the opponent and blocks that move. If neither of these are 
    possible, it plays a random move.

    :param board: The game board, 2D list of 6x7 dimensions.
    :param player: The player whose turn it is, integer value of 1 or 2.
    :return: Column that the piece was dropped into, int.
    """

    """
    1. Play a move that results in immediate win
    2. Check if opponent can score immediate win
        block this 
    3. if none then play random drop
    """

    # check for a winning piece
    winning_place = get_winning_place(board, player)
    if winning_place:
        return winning_place  # winning place successfully placed

    # check for blocking
    blocking_place = get_blocking_place(board, player)
    if blocking_place:
        return blocking_place  # blocking place successfully placed

    return cpu_player_easy(board, player)


def cpu_player_hard(board, player):
    """
    Executes a move for the CPU on hard difficulty.
    This function creates a copy of the board to simulate moves.

    Algorithm:
        1. Check for immediate winning move and go there if there is
        2. Check for immediate blocking move and go there if there is
        3. Place somewhere in the middle
        4. Place randomly

    :param board: The game board, 2D list of 6x7 dimensions.
    :param player: The player whose turn it is, integer value of 1 or 2.
    :return: Column that the piece was dropped into, int.
    """
    # check for a winning piece
    winning_place = get_winning_place(board, player)
    if winning_place:
        return winning_place

    # check for blocking
    blocking_place = get_blocking_place(board, player)
    if blocking_place:
        return blocking_place

    # otherwise return random in middle
    # the index range is (3)
    for i in range(len(board[0]) // 2 + 1):
        # progressively +1, attempting to drop the token towards right end available columns
        # this will try drop into columns 3-6
        col = len(board[0]) // 2 + i
        if drop_piece(board, player, col):
            return col

        # progressively  -1, attempting to drop the token towards the left end available column
        # this will try to drop into columns 3-0
        col = len(board) // 2 - i
        if drop_piece(board, player, col):
            return col

    # place randomly
    return cpu_player_easy(board, player)


def get_cpu_difficulty() -> int:
    """
    Gets the difficulty of the CPU
    Asks the user what difficulty they would like to play against

    :return int: 1 = easy, 2 = medium, 3 = hard
    use validate_input
    """

    # Asking user to choose the cpu difficulty level of easy, medium or hard 
    # In order to do so we invoke the valid_input() function 
    user_input = int(validate_input(prompt="Please select a difficulty (1: Easy, 2: Medium, 3; Hard): ",
                                    valid_inputs=["1", "2", "3"]))
    return user_input


def game_against_cpu():
    """
    Runs a game of Connect 4 against the computer.
    Difficulty is selected based on user's input.

    :return: None
    """
    board = create_board()

    # initial player is assigned 1
    current_player = 1
    # There is no previous column choice to tell players
    prev_col_choice = None

    # get cpu difficulty (1 = easy, 2 = med, 3 = hard)
    cpu_difficulty: int = get_cpu_difficulty()

    while True:
        clear_screen()
        # start executing the turn
        print_board(board)

        # if there was a previous move (turn 1 has no previous move), then print that out
        if prev_col_choice:
            # '2 if current_player==1 else 1' will only switch player inside print function as current_player switched at bottom of function
            print(f'Player {2 if current_player == 1 else 1} has dropped in {prev_col_choice}')

        # start of switch case to execute player's turn, or cpu player's turn based on difficulty selected
        if current_player == 1:
            prev_col_choice = execute_player_turn(current_player, board)
        elif current_player == 2:
            # this is the cpu turn

            # Easy difficulty
            if cpu_difficulty == 1:
                prev_col_choice = cpu_player_easy(board, current_player) # save the column index dropped for use in the next iteration. Same applies to latter difficulties

            # Medium difficulty
            if cpu_difficulty == 2:
                prev_col_choice = cpu_player_medium(board, current_player)

            # Hard difficulty
            if cpu_difficulty == 3:
                prev_col_choice = cpu_player_hard(board, current_player)

        # invokes end_of_game() function to check if there is a winner or not, and if there is a winner who is it  
        check_winner = end_of_game(board)
        if check_winner == 1:
            clear_screen()
            print_board(board)
            print("Player 1 wins")
            break  # terminate this function, and return main() function, which exits the program. Same applies to later player wins.
        elif check_winner == 2:
            clear_screen()
            print_board(board)
            print("Player 2 wins")
            break
        elif check_winner == 3:
            clear_screen()
            print_board(board)
            print("Draw")
            break

        # change the Player
        current_player = 2 if current_player == 1 else 1


if __name__ == "__main__":
    main()
