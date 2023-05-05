import random

# Global constants
VALID_ROWS = []
VALID_COLUMNS = []
VALID_PLAYERS = []
VALID_TOKEN_WINS = []
VALID_CPU_NUM = []
for i in range(4, 51):
    VALID_ROWS.append(str(i))
    VALID_COLUMNS.append(str(i))
for i in range(1, 6):
    VALID_PLAYERS.append(str(i))
    VALID_CPU_NUM.append(str(i))
for i in range(4, 11):
    VALID_TOKEN_WINS.append(str(i))

COLUMN_NUM = 0
ROW_NUM = 0
NUM_PLAYERS = 0
NUM_BOTS = 0
WINNING_LENGTH = 0


def print_rules():
    """
    Prints the rules of the game.

    :return: None
    """
    print("================= Rules =================")
    print("Local game: ")
    print("1. Make your connect 4 board")
    print("2. Choose number of human players")
    print("3. Choose number of tokens adjacent in order to win")
    print("4. Player 1 is assigned X and Player 2 is assigned O,")
    print("   if number of players is larger than 2 (CPU and or")
    print("   human) players will be assigned A, B, C...")

    print("\nCPU game:")
    print("1. Make your connect 4 board")
    print("2. Choose number of human players")
    print("3, Choose number of CPU players")
    print("4. Choose number of tokens adjacent in order to win")
    print("5. Player 1 is assigned X and Player 2 is assigned O,")
    print("   if number of players is larger than 2 (CPU and or")
    print("   human) players will be assigned A, B, C...")
    print("=========================================")


def get_user_inputs(prompt, valid_inputs):
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
    return int(user_input)


def create_board(row_num, column_num):
    """
    Returns a 2D list of lists that takes up to and including 50 rows and or columns
    the game board. Default cell value is 0.

    :param row_num: Number of rows to create.
    :param column_num: Number of columns to create.
    :return: A 2D list x * y dimensions
    """

    game_board = []

    for i in range(row_num):
        row = [0] * column_num
        game_board.append(row)
    return game_board


def print_board(board):
    """
    Prints the game board to the console.

    :param board: The game board, 2D list of x * y dimensions, 2D list of x * y dimensions
    :return: None
    """
    # Assigning variables
    board_string = ""
    header = ("===" * (COLUMN_NUM // 2) + " Connect4 " + "===" * (COLUMN_NUM // 2)) + "=="

    # displays key/value pair of human and robot player number, and their token character.
    players_num_and_token = ""
    for i in range(1, NUM_PLAYERS + NUM_BOTS + 1):
        if i <= NUM_PLAYERS:
            players_num_and_token += f"Player {i}: {get_display_char(i)} (Human)\n"
        else:
            players_num_and_token += f"Player {i}: {get_display_char(i)} (CPU)\n"

    column_nums = "  "
    for i in range(1, COLUMN_NUM + 1):
        if i < 9:
            column_nums += f"{i}   "
        else:
            column_nums += f"{i}  "  # reduce whitespace margin for column index >= 10
    horizontal_line = " ---" * COLUMN_NUM
    footer = "====" * COLUMN_NUM + "="
    # .join can only work on multiple variables if they are in a list
    # \n = newline
    board_string = "\n".join([header, players_num_and_token, column_nums, horizontal_line])

    # iterate through rows in the 2D array
    for row in board:

        # adds a | for every row (left most box only)
        board_string += "\n|"

        for num in row:
            display_char = get_display_char(num)
            board_string += f" {display_char} |"

        # Add horizontal line for each row
        board_string += ("\n" + horizontal_line)
    board_string += ("\n" + footer)
    print(board_string)


def get_display_char(num):
    """
    Gets display character for a number on the board

    :return: The player's token character to be displayed
    """
    char_list = [' ', 'X', 'O', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    return char_list[num]


def drop_piece(board, player, column: int):
    """
    Drops a piece into the game board in the given column.
    Please note that this function expects the column index
    to start at 1.

    :param board: The game board, 2D list of x * y dimensions
    :param player: The player who is dropping the piece, int.
    :param column: The index of column to drop the piece into, int.
    :return: True if piece was successfully dropped, False if not.
    """
    check_column = column - 1
    check_row = ROW_NUM - 1

    while check_row >= 0:
        check_slot = board[check_row][check_column]
        if check_slot == 0:
            board[check_row][check_column] = player
            return True
        # decrement check_row
        check_row -= 1
    return False


def execute_player_turn(player, board):
    """
    Prompts user for a legal move given the current game board
    and executes the move.

    :return: Column that the piece was dropped into, int.
    """
    # initial value of successful_drop
    successful_drop = False

    while successful_drop == False:

        # Column choice is assigned function validate input, prompting the specific player
        valid_inputs = []
        for i in range(COLUMN_NUM):
            valid_inputs.append(str(i + 1))

        column_choice = get_user_inputs(
            prompt=f'Player {player}, please enter the column you would like to drop your piece into: ',
            valid_inputs=valid_inputs)
        # Reassign successful_drop to drop_piece
        successful_drop = drop_piece(board, player, column_choice)
        # print(successful_drop)

        if successful_drop == True:
            return column_choice
        print("That column is full, please try again.")


def end_of_game(board):
    """
    Checks if the game has ended with a winner
    or a draw.

    :param board: The game board, 2D list of x * y dimensions.
    :return: 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins and so on... -1 if draw.
    """

    # player has won
    player_has_won = get_winning_player(board)
    if player_has_won != 0:
        return player_has_won

    # board is full
    if board_is_full(board):
        return -1

    # game is not over
    return 0


def board_is_full(board) -> bool:
    """
    Checks if the board is full

    :param board: The game board, 2D list of x rows * y columns.
    :return: true if full else false
    """

    """
    check every number slot in board
    if any slot has a 0 then return false
    if no slot is 0 return True
    """

    # iterates through every number slot in the board
    for row in board:
        for num in row:
            if num == 0: # check if any slot in the board is assigned 0 (empty)
                return False
    return True  # if there aren't any empty slots left


def get_winning_player(board) -> int:
    """
    Checks if there is a winning player

    :param board: The game board, 2D list of any number of rows and columns up to 50
    :return: The number of the player who wins (stored_num)
    """
    # check horizontal
    # Iterate through each row in the board
    for row in board:
        # Iterate through range of whatever the row is (gotten by user) - winning length (token_win: user input)
        for i in range(len(row) - WINNING_LENGTH + 1):

            # store the number we are looking at here and initialise it with nothing stored 
            stored_num = None

            # Iterate through range(starting index of row, starting index + winning length)
            # We do this as we don't know how many indexes in the row we have to check. If we did we could hard code it like we did in task 6 for checking horizontal wins
            # So in this case we loop it
            for j in range(i, i + WINNING_LENGTH):
                # start at the first index in the row 
                current_num = row[j]

                # check if we have started storing
                # If there is no number stored in stored_num then store current_num
                if stored_num is None:
                    stored_num = current_num

                # If numbered stored is the same as the next number after it then continue checking
                elif stored_num == current_num and current_num != 0:
                    continue
                # if it is not a equal string of numbers or we find a zero, there is no winner here
                elif current_num != stored_num or current_num == 0:
                    stored_num = None
                    break
            # check if we have a winner (the whole row was the same when checking)
            if stored_num is not None:
                return stored_num

    # Check vertical
    for i in range(COLUMN_NUM):
        for j in range(ROW_NUM - WINNING_LENGTH + 1):
            stored_num = None
            for k in range(j, j + WINNING_LENGTH):

                current_num = board[k][i]

                # check if we have started storing
                # If there is no number stored in stored_num then store current_num
                if stored_num is None:
                    stored_num = current_num

                # If numbered stored is the same as the next number after it then continue checking
                elif stored_num == current_num and current_num != 0:
                    continue
                # if it is not a equal string of numbers or we find a zero, there is no winner here
                elif current_num != stored_num or current_num == 0:
                    stored_num = None
                    break
            # check if we have a winner (the whole row was the same when checking)
            if stored_num is not None:
                return stored_num

    # Check diagonal left to right
    for i in range(ROW_NUM - WINNING_LENGTH + 1):
        for j in range(COLUMN_NUM - WINNING_LENGTH + 1):
            stored_num = None
            for k in range(WINNING_LENGTH):
                current_num = board[i + k][j + k]

                # check if we have started storing
                # If there is no number stored in stored_num then store current_num
                if stored_num is None:
                    stored_num = current_num

                # If numbered stored is the same as the next number after it then continue checking
                elif stored_num == current_num and current_num != 0:
                    continue
                # if it is not a equal string of numbers or we find a zero, there is no winner here
                elif current_num != stored_num or current_num == 0:
                    stored_num = None
                    break
            # check if we have a winner (the whole row was the same when checking)
            if stored_num is not None:
                return stored_num

    # Check diagonal right to left
    for i in range(ROW_NUM - WINNING_LENGTH + 1):
        for j in range(COLUMN_NUM - WINNING_LENGTH + 1):
            stored_num = None
            for k in range(WINNING_LENGTH):
                current_num = board[i + k][-j - k - 1]

                # check if we have started storing
                # If there is no number stored in stored_num then store current_num
                if stored_num is None:
                    stored_num = current_num

                # If numbered stored is the same as the next number after it then continue checking
                elif stored_num == current_num and current_num != 0:
                    continue
                # if it is not a equal string of numbers or we find a zero, there is no winner here
                elif current_num != stored_num or current_num == 0:
                    stored_num = None
                    break
            # check if we have a winner (the whole row was the same when checking)
            if stored_num is not None:
                return stored_num

    return 0


def clear_screen():
    """
    Clears the terminal for Windows and Linux/MacOS.

    :return: None
    """
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def cpu_player_easy(board, player):
    """
    Executes a move for the CPU on easy difficulty. This function 
    plays a randomly selected column.

    :param board: The game board, 2D list of x * y dimensions
    :param player: The player whose turn it is
    :return: Column that the piece was dropped into, int.
    """

    # Initially cpu has not dropped a piece
    cpu_has_dropped = False
    # While cpu has not dropped
    while not cpu_has_dropped:
        # Choose a random column 
        ran_int = random.randint(1, ROW_NUM)
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
    cloned_board = create_board(ROW_NUM, COLUMN_NUM)
    # for each item in the param board, copy over to cloned board

    # for each row
    for i in range(ROW_NUM):
        # for each value in each row
        for j in range(COLUMN_NUM):
            # cloning the values in each slot in real board to cloned board (mimicking the real board to check wins)
            cloned_board[i][j] = board[i][j]
    return cloned_board

    # return the cloned board


def get_winning_place(board, player):
    """
    This function checks for an immediate win and plays that move if possible
    This function will take precedence over get_blocking_piece()
   
    :param board: The game board, 2D list of x * y dimensions
    :param player: The player whose turn it is, integer value of 1,2,3,...5
    :return: Column of the winning place or none if there is no winning place
    """
    # for each col
    # clone the board
    # drop the piece into the cloned board
    # if this wins the game, drop the piece into the real board and return the column

    for j in range(COLUMN_NUM):
        # print(j)
        cloned_board = clone_board(board)
        cpu_drop = drop_piece(cloned_board, player, j)
        if cpu_drop:
            if get_winning_player(cloned_board) == player:
                drop_piece(board, player, j)
                return j

    # There is no winning place
    return None


def get_blocking_place(board, player):
    """
    This function checks if the opponent (human player) is about to win and blocks it
    If the opponent has multiple ways of winning this function will block the first one it sees    
    Please note  this function accepts player in favour if the block, then switches to the opponent to simulate their win


    :param board: The game board, 2D list of x * y dimensions
    :param player: The player whose turn it is
    :return: The column of the blocking place or none if there is no win to block
    """

    # for each col
    # clone the board
    # drop the piece into the cloned board
    # if this piece blocks a win in the clone board
    # it will then be dropped into the real board in order to block the opponents piece in real time
    # if there is no win to block then return None and continue playing

    # check opponent block
    for j in range(COLUMN_NUM):
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

        :param board: The game board, 2D list of x * y dimensions
    :param player: The player whose turn it is
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
        return winning_place

    # check for blocking
    blocking_place = get_blocking_place(board, player)
    if blocking_place:
        return blocking_place

    return cpu_player_easy(board, player)


def cpu_player_hard(board, player):
    """
    Executes a move for the CPU on hard difficulty.
    This function creates a copy of the board to simulate moves.

    Algorithm:
        1. Check for winning move and go there if there is
        2. Check for blocking move and go there if there is
        3. Place somewhere in the middle
        4. Place randomly

        :param board: The game board, 2D list of x * y dimensions
    :param player: The player whose turn it is
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
    for i in range(ROW_NUM // 2 + 1):
        # +1
        # this will try drop into columns 3-6
        col = ROW_NUM // 2 + i
        if drop_piece(board, player, col):
            return col

        # -1
        # this will try to drop into columns 3-0
        col = ROW_NUM // 2 - i
        if drop_piece(board, player, col):
            return col

    # place randomly
    return cpu_player_easy(board, player)


def get_cpu_difficulty() -> int:
    """
    Gets the difficulty of the CPU
    Asks the user what difficulty they would like to play against

    :return int: 1 = easy, 2 = medium, 3 = hard
    use get_user_input
    """

    # Asking user to choose the cpu difficulty level of easy, medium or hard 
    # In order to do so we invoke the valid_input() function 
    user_input = int(get_user_inputs(prompt="Please select a difficulty (1: Easy, 2: Medium, 3; Hard): ",
                                     valid_inputs=["1", "2", "3"]))
    return user_input


def local_game():
    """
    Runs a local game of Connect 4.

    :return: None
    """
    global COLUMN_NUM
    global ROW_NUM
    global NUM_PLAYERS
    global NUM_BOTS
    global WINNING_LENGTH

    COLUMN_NUM = get_user_inputs(prompt="Enter a number of columns for the gameboard (4-50): ", valid_inputs=VALID_ROWS)
    ROW_NUM = get_user_inputs(prompt="Enter a number of rows for the gameboard (4-50):  ", valid_inputs=VALID_COLUMNS)
    NUM_PLAYERS = get_user_inputs(prompt="Enter a number of human players (1-5): ", valid_inputs=VALID_PLAYERS)
    WINNING_LENGTH = get_user_inputs(prompt="Enter the number of tokens adjacent for a player to win (4-10): ",
                                     valid_inputs=VALID_TOKEN_WINS)

    board = create_board(ROW_NUM, COLUMN_NUM)
    total_player_num = int(NUM_PLAYERS)

    # initial player is assigned 1
    current_player = 1
    # There is no previous column choice to tell players
    prev_col_choice = None

    while True:
        clear_screen()
        # execute the turn
        print_board(board)

        # if there was a previous move (turn 1 has no previous move), then print that out
        # if prev_col_choice:
        #     last_player = (current_player % total_player_num) -1
        #     print(f"Player {last_player} has dropped in {prev_col_choice}")

        if prev_col_choice:
            if current_player == 1:
                last_player = total_player_num
            else:
                last_player = current_player - 1
            print(f"Player {last_player} has dropped in {prev_col_choice}")

        prev_col_choice = execute_player_turn(current_player, board)

        # invokes end_of_game() function to check if there is a winner or not, and if there is a winner who is it
        check_winner = end_of_game(board)

        # check not continue
        if check_winner != 0:
            # draw
            if check_winner == -1:
                clear_screen()
                print_board(board)
                print("Draw")
                break

            # player wins
            clear_screen()
            print_board(board)
            print(f"Player {check_winner} wins")
            break

        current_player = (current_player % total_player_num) + 1


def game():
    """
    Runs a game of Connect 4 against the computer with one or more human players

    :return: None
    """
    global COLUMN_NUM
    global ROW_NUM
    global NUM_PLAYERS
    global NUM_BOTS
    global WINNING_LENGTH

    COLUMN_NUM = get_user_inputs(prompt="Enter a number of columns for the gameboard (4-50): ", valid_inputs=VALID_ROWS)
    ROW_NUM = get_user_inputs(prompt="Enter a number of rows for the gameboard (4-50):  ", valid_inputs=VALID_COLUMNS)
    NUM_PLAYERS = get_user_inputs(prompt="Enter a number of human players (1-5): ", valid_inputs=VALID_PLAYERS)
    NUM_BOTS = get_user_inputs(prompt="Enter a number of bot players (2-5): ", valid_inputs=VALID_PLAYERS)
    WINNING_LENGTH = get_user_inputs(prompt="Enter the number of tokens adjacent for a player to win (4-10): ",
                                     valid_inputs=VALID_TOKEN_WINS)

    board = create_board(ROW_NUM, COLUMN_NUM)
    # initial player is assigned 1
    current_player = 1
    # There is no previous column choice to tell players
    prev_col_choice = None
    total_player_num = NUM_PLAYERS + NUM_BOTS
    # get cpu difficulty (1 = easy, 2 = med, 3 = hard)
    cpu_difficulty: int = get_cpu_difficulty()

    while True:
        clear_screen()
        # execute the turn
        print_board(board)

        # if there was a previous move (turn 1 has no previous move), then print that out
        if prev_col_choice:
            if current_player == 1:
                last_player = total_player_num
            else:
                last_player = current_player - 1
            print(f"Player {last_player} has dropped in {prev_col_choice}")

        # start of switch case to execute player's turn, or cpu player's turn based on difficulty selected
        if current_player <= NUM_PLAYERS:
            prev_col_choice = execute_player_turn(current_player, board)
        elif current_player > NUM_PLAYERS:
            # this is the cpu turn

            # Easy difficulty
            if cpu_difficulty == 1:
                prev_col_choice = cpu_player_easy(board, current_player)

            # Medium difficulty
            if cpu_difficulty == 2:
                prev_col_choice = cpu_player_medium(board, current_player)

            # Hard difficulty
            if cpu_difficulty == 3:
                prev_col_choice = cpu_player_hard(board, current_player)

        # invokes end_of_game() function to check if there is a winner or not, and if there is a winner who is it  
        check_winner = end_of_game(board)
        if check_winner != 0:  # check not continue
            # draw
            if check_winner == -1:
                clear_screen()
                print_board(board)
                print("Draw")
                break

            # player wins
            clear_screen()
            print_board(board)
            print(f"Player {check_winner} wins")
            break

        current_player = (current_player % total_player_num) + 1


def main():
    """
    Defines the main application loop.
    User chooses a type of game to play or to exit.

    :return: None
    """
    menu_string = """=============== Main Menu ===============
Welcome to Connect 4!
1. View Rules
2. Play a cpu game
3. Play a local game
4. Exit
=========================================
Enter a number: """

    clear_screen()
    while True:

        # Ask user for an option (1-4) as stated in the menu string above
        user_input = get_user_inputs(
            prompt=menu_string,
            valid_inputs=["1", "2", "3", "4"]
        )
        # Print rules
        if user_input == 1:
            clear_screen()
            print_rules()
        # Plays game with bots and humans
        if user_input == 2:
            return game()
        # Plays local game
        if user_input == 3:
            return local_game()
            # Quits game
        if user_input == 4:
            print("You have exited the game")
            return


if __name__ == "__main__":
    main()
