'''
This file is for unit testing code.
'''

import chess_game

if __name__ == '__main__':
    game_state = chess_game.ChessGame(throw_exceptions=True)

    # Test moving a piece
    print('Inital state of the board')
    game_state.print_game_state_to_terminal()
    move = [[4,2],[4,4]]
    game_state.move_piece(move)
    game_state.print_game_state_to_terminal()