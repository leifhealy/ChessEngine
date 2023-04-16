'''
============================== CHESS ENGINE =======================================
This is the main script for running the competition. 

'''
import chess_game


if __name__ == '__main__':
    game_state = chess_game.ChessGame(throw_exceptions=True)

    game_state.print_game_state_to_terminal()

    pass







