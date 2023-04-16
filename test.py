'''
This file is for unit testing code.
'''

import chess_game

if __name__ == '__main__':
    print('============== Running unit tests ===============')
    unit_test_number = 1
    
    # Unit test 1: Initialise ChessGame
    try: 
        game_state = chess_game.ChessGame(throw_exceptions=True)
    except ValueError: 
        print('Failed while initialising game state. Unit test: Initialise ChessGame')

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