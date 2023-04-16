'''
This file is for unit testing code.
'''
import chess_game

def report_failure(): 
    print('TESTING FAILED: DEBUGING REQUIRED.')

if __name__ == '__main__':
    print('============== Running unit tests ===============')
    unit_test_number = 1
    
    # ===========================================================
    # Unit test 1: Initialise ChessGame
    try: 
        game_state = chess_game.ChessGame(throw_exceptions=True)
    except ValueError: 
        print('Failed while initialising game state. Unit test: Initialise ChessGame')

    # ===========================================================
    # Unit test 2: moving a pawn at the start of the game
    # to do: I think this should be in a try catch set up.
    unit_test_successful = False
    print('Inital state of the board is:')
    game_state.print_game_state_to_terminal()
    move = [[1,3],[3,3]]
    moved_successfully = game_state.move_piece(move)

    print('New state of the board is: ')
    game_state.print_game_state_to_terminal()
    rank, file = move[1]
    if game_state.board["Pieces"][rank][file] == 'Pa' and game_state.board["Colours"][rank][file] == 'W' and moved_successfully : 
        unit_test_successful = True

    if unit_test_successful: print('Unit test 2 successful.')

    # ===========================================================
    # Unit test 3: move white kings pawn forward by two places
    unit_test_successful = False
    move = [[6,4],[4,4]]
    moved_successfully = game_state.move_piece(move)

    print('Moving the white kings pawn.')
    print('New state of the board is: ')
    game_state.print_game_state_to_terminal()

    # ===========================================================
    # Unit test 4: try to move the black queen through the black pawn
    move = [[0,3],[4,3]]

    print('Attempting to move a queen vertically through a pawn...')
    game_state.throw_exceptions = False
    move_result = game_state.move_piece(move)
    if move_result == -1: 
        print('Game state returned -1 for illegal move. Which is correct.')
        print('New board positions are:')
        game_state.print_game_state_to_terminal()
    else: 
        print('Game state did not return -1 indicating illegal move. This is in correct!!!')
        print('New board positions: ')
        game_state.print_game_state_to_terminal()
        report_failure()
    

    

    # ===========================================================
    # Unit test N: try to move a pawn backwards
