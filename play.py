'''
This script is to test out the chess engine by playing it.

# To do: 
- update the while loop to something meaningful so you don't just have exit out.

'''
import chess_game
if __name__ == '__main__':
    print('Starting new chess game: ')

    game_state = chess_game.ChessGame(throw_exceptions=False)

    while True: 
        print('Here is the current state of the game: ')
        game_state.print_game_state_to_terminal()

        print('')
        move_starting_rank = input('Which piece would you like to move (rank):')
        move_to_rank = input('Where would you like to move it (rank): ')
        move_starting_file = input('Which piece would you like to move (file):')
        move_to_file = input('Where would you like to move it (file): ')

        try : 
            move_starting_rank = int(move_starting_rank)
            move_starting_file = int(move_starting_file)
            move_to_file = int(move_to_file)
            move_to_rank = int(move_to_rank)
        except : 
            print('Could not parse input. Please try again.')
            continue

        move = [[move_starting_rank, move_starting_file],[move_to_rank, move_to_file]]

        moved_successfully, message = game_state.move_piece(move)

        if not moved_successfully: 
            print(message)






