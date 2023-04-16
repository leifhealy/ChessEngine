'''
To do description

# To dos: 
- add checks
-- add to is move illegal a check whether it puts the player in check
-- add something at the end of a move that finds if a move it illegal
- add checkmate
- add castling
- add pawn promotion
- add en passant
- refactor pawn is move legal to be more readable - similar to 'move_obeys_knight_movement_rules'
- refactor this_move_puts_me_in_check - it is not very readable with all those nested loops.
-- I think when you come to checking for checks lines of sight will be more abstracted so it might pay to return here
   once that code is written.
-- another issue is that you are using lists for vectors. It would be better to use numpy array

Optimisation: 
- mannually track the kings each time they are moved instead of searching the board again to find their location each move
-- this is required to check for checks and mates each time someone moves

'''
import dirk
import leif

class ChessGame : 
    '''
    To do description
    '''
    def __init__(self, throw_exceptions): 
        self.board = {}
        self.board["Pieces"] = [['Ca','Kn','Bi','Qu','Ki','Bi','Kt','Ca'],
                                ['Pa','Pa','Pa','Pa','Pa','Pa','Pa','Pa'],
                                [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
                                [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
                                [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
                                [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
                                ['Pa','Pa','Pa','Pa','Pa','Pa','Pa','Pa'],
                                ['Ca','Kn','Bi','Qu','Ki','Bi','Kt','Ca']]
        
        self.board["Colours"]= [['B','B','B','B','B','B','B','B'],
                                ['B','B','B','B','B','B','B','B'],
                                [ '', '', '', '', '', '', '', ''],
                                [ '', '', '', '', '', '', '', ''],
                                [ '', '', '', '', '', '', '', ''],
                                [ '', '', '', '', '', '', '', ''],
                                ['W','W','W','W','W','W','W','W'],
                                ['W','W','W','W','W','W','W','W']]
        
        self.throw_exceptions =  throw_exceptions

        self.player_whose_turn_it_is = 'W'
        
        self.material_scores = {}
        self.material_scores['W'] = 8 + 4*3 + 5*2 + 9
        self.material_scores['B'] = self.material_scores['W']

        self.update_sparse_representation()

    def relative_position_from_move(self, move): 
        ''' Calculated the change in position vector from a move array '''
        relative_position = [move[1][0] - move[0][0],move[1][1]-move[0][1]]
        return relative_position

    def update_sparse_representation(self): 
        '''
        Creates a list of where all the pieces are at the start of the game
        '''
        self.sparse_representation = []
        for rank in range(8): 
            for column in range(8): 
                piece_type = self.board["Pieces"]
                if piece_type == '' : 
                    continue
                
                piece_colour = self.board["Colours"]

                self.sparse_representation.append([piece_type,piece_colour])

    def print_game_state_to_terminal(self): 
        '''
        Print a basic assci representation of the game to the terminal.
        '''
        print_string = '      f0   f1   f2   f3   f4   f5   f6   f7\n'
        print_string = print_string + '    -----------------------------------------\n'
        for rank in range(8): 
            print_string = print_string + ' r' + str(rank) + ' '
            for column in range(8):
                square_string = ''
                piece = self.board["Pieces"][rank][column]
                colour = self.board["Colours"][rank][column]

                if colour == 'B':
                    square_string =   '|:<>:'
                elif colour =='W': 
                    square_string =   '| <> '
                else: square_string = '|    '
                
                square_string = square_string.replace('<>',piece)

                print_string = print_string + square_string

            print_string = print_string +'|\n'
            print_string = print_string + '    -----------------------------------------\n'

        print(print_string)
    
    def handle_error(self, error_message): 
        if self.throw_exceptions: 
            raise ValueError(error_message)

    def no_piece_at_start_location(self,move): 
        '''Returns true when there is no piece at the starting location of a move'''
        rank, file = move[0]
        piece_colour = self.board["Colours"][rank][file]

        if piece_colour == '': 
            self.handle_error('Error: while checking if move is illegal no piece was found at the starting location.')
            return True
    
    def update_material_scores(self): 
        self.material_scores['W'] = 0.0
        self.material_scores['B'] = 0.0

        self.update_sparse_representation()

        for piece_type, piece_colour in self.sparse_representation: 
            if piece_type == 'Pa': value = 1.0
            elif piece_type == 'Ca': value = 5.0
            elif piece_type == 'Kn': value = 3.0
            elif piece_type == 'Bi': value = 3.0
            elif piece_type == 'Qu': value = 9.0
            elif piece_type == 'Ki': value = 0.0
            else : value = 0.0

            self.material_scores[piece_colour] = self.material_scores[piece_colour] + value

    def same_colour_piece_at_destination(self, move): 
        '''
        Returns true if there is a same coloured piece at that destination.
        Inputs: 
        move = [[start_rank, start_column],[final_rank, final_column]]
        '''
        rank, file = move[0]
        piece_colour = self.board["Colours"][rank][file]

        rank, file = move[1]
        colour_at_destination = self.board["Colours"][rank][file]

        if piece_colour == colour_at_destination: 
            error_string = '[colour]'
            if piece_colour == 'W' : error_string = 'white'
            if piece_colour == 'B' : error_string = 'black'
            self.handle_error('ERROR: tried to move {} piece onto another {} piece.'.format(error_string,error_string))
            return True

        return False

    '''To do: the following three functions re-use quite a lot of code. Can you abstract them to reduce repeatition?
        I think you can possibly just use the diagonal movement function for all three - need to check. '''
    def hozizontal_movement_is_blocked(self, start_file, final_file, rank): 
        '''
        Retruns true if a purely horizontal movement is blocked. Assumes movement is larger than 1 position. 
        
        Inputs: 
        start_file = file of the piece at the start,
        final_file = file of the piece at the end,
        rank = the rank to be checked. 
        '''
        files_to_check = range(start_file, final_file)
        for file in files_to_check: 
            if file == start_file: continue # ignore itself when checking for interupting pieces
            piece = self.board["Pieces"][rank][file]
            
            if not piece == '':
                self.handle_error("Illegal move: tried to move a piece through another piece (excluding knights)")
                return True
        return False
        
    def vertical_movement_is_blocked(self, start_rank, final_rank, file): 
        '''
        Returns true if a purely vertical movement is blocked by another piece. Assumes movement is larger than 1 postion. 

        Inputs: 
        start_rank = the rank of the piece to be moved
        final_rank = the rank that the piece is to be moved to
        file = the file that it will be moving along. 
        '''
        ranks_to_check = range(start_rank, final_rank)
        for rank in ranks_to_check: 
            if rank == start_rank: continue # ignore itself when checking for interupting pieces
            piece = self.board["Pieces"][rank][file]
            
            if not piece == '':
                self.handle_error("Illegal move: tried to move a piece through another piece (excluding knights)")
                return True
        return False

    def diagonal_movement_is_blocked(self, start_rank, final_rank, start_file, final_file): 
        '''
        Returns true if a purely vertical movement is blocked by another piece. Assumes movement is larger than 1 postion. 

        Inputs: 
        start_rank = the rank of the piece to be moved
        final_rank = the rank that the piece is to be moved to
        start_file = the file of the piece to be moved. 
        final_file = the file that the piece is to be moved to. 
        '''
        ranks_to_check = range(start_rank, final_rank)
        files_to_check = range(start_file, final_file)

        for rank, file in zip(ranks_to_check, files_to_check): 
            if rank == start_rank: continue
            piece = self.board["Pieces"][rank][file]

            if not piece == '': 
                self.handle_error("Illegal move: tried to move a piece through another piece (excluding knights)")
                return True
            return False

    def blocked_by_piece(self, move): 
        '''Returns true if there is a piece in the way of the move'''
        start_rank, start_file = move[0]
        piece = self.board["Pieces"][start_rank][start_file]

        if piece == 'Kn' : return False

        final_rank, final_file = move[1]
        rank_change = final_rank - start_rank
        file_change = final_file - start_file

        if abs(rank_change) <= 1 and abs(file_change) <= 1: return False

        # The movement will either be: 
        # A) a knight (which is already handled above by return false), or
        # B) only a step of size 1 (which is already handled above), or
        # C) any other piece making a purely horizontal, vertical or diagonal movement. 
        #       lets handle each direction turn for simplicity
        # horizontal
        if rank_change == 0: 
            if self.hozizontal_movement_is_blocked(start_file, final_file, start_rank):
                return True

        # vertical
        elif file_change == 0: 
            if self.vertical_movement_is_blocked(start_rank, final_rank, start_file): 
                return True

        # diagonal
        else: 
            if self.diagonal_movement_is_blocked(start_rank, final_rank, start_file, final_file): 
                return True

        return False

    def find_current_players_king(self): 
        ''' 
        Returns the position [rank, file] of the current players king 
        '''
        for rank in range(8): 
            for file in range(8): 
                if self.board["Colours"][rank][file] == self.player_whose_turn_it_is: 
                    if self.board["Pieces"][rank][file] == 'Ki': 
                        return [rank, file]
                    
    def this_move_puts_me_in_check(self, move): 
        ''' Returns true if the proposed move puts the player into check and false otherwise. '''
        current_players_king_position = self.find_current_players_king()
        piece_to_be_moved_start_position = move[0]
        king_to_piece_relative_position = [piece_to_be_moved_start_position[0] - current_players_king_position[0],
                                           piece_to_be_moved_start_position[1] - current_players_king_position[1]]

        if not king_to_piece_relative_position[0] == king_to_piece_relative_position[1]: 
            # then there is no straight lines of sight between the king and the piece anyway
            return False
        
        king_to_piece_relative_direction = [king_to_piece_relative_position[0]/abs(king_to_piece_relative_position[0]),
                                            king_to_piece_relative_position[1]/abs(king_to_piece_relative_position[1])]

        position = [current_players_king_position[0] + king_to_piece_relative_direction[0], 
                    current_players_king_position[1] + king_to_piece_relative_direction[1]]
        while position != piece_to_be_moved_start_position: 
            if self.there_is_a_piece_here(position): 
                return False # because there is a piece between the king and the piece being moved

        position = [piece_to_be_moved_start_position[0] + king_to_piece_relative_direction[0], 
                    piece_to_be_moved_start_position[1] + king_to_piece_relative_direction[1]]
        while self.position_is_on_the_board(position): 
            if self.there_is_a_piece_here(position): 
                rank, file = position
                piece = self.board["Pieces"][rank][file]
                colour = self.board["Colours"][rank][file]

                if colour == self.player_whose_turn_it_is: 
                    return False # becasue our pieces don't put us in check
                
                if piece == 'Qu' : return True
                elif piece == 'Ca': 
                    if king_to_piece_relative_direction[0] == king_to_piece_relative_direction[1]: 
                        return False # because this means it would be a diagonal line of sight
                    else : return True # because this would be a horizontal line of sight
                elif piece == 'Bi':
                    if king_to_piece_relative_direction[0] == king_to_piece_relative_direction[1]: 
                        return True # because this would be a diagonal line of sight
                    else : return False # because thi would be a horizontal line of sight.
        
    def position_is_on_the_board(self,position): 
        if position[0] < 0 or position[0] > 7: return False
        elif position[1] < 0 or position[1] > 7: return False
        else : return True

    def get_colour_full_name_from_letter(self, letter): 
        if letter == 'W': return 'white'
        if letter == 'B': return 'black'
        raise ValueError('Colour not found. This is likely due to a bug in the code.')

    def is_move_a_take(self, move): 
        ''' Returns true if move is a take and false otherwise '''
        final_rank = move[1][0]
        final_file = move[1][1]
        return not self.board['Pieces'][final_rank][final_file] == ''

    def is_move_legal(self, move): 
        '''
        This function returns true if a move is legal and false if not. In it's second return it gives the reason.
        '''
        reason = ''
        piece_to_move_rank = move[0][0]
        piece_to_move_file = move[0][1]
        piece_to_move_colour = self.board["Colours"][piece_to_move_rank][piece_to_move_file]

        if self.no_piece_at_start_location(move): 
            reason = 'Illegal move: no piece at start location.'
            return [False, reason]

        if not piece_to_move_colour == self.player_whose_turn_it_is: 
            colour_full_name = self.get_colour_full_name_from_letter(piece_to_move_colour)
            reason = 'Illegal move: tried to move a {} piece but it is {}\'s turn.'.format(colour_full_name, self.player_whose_turn_it_is)
            return [False, reason]

        if self.same_colour_piece_at_destination(move) :
            reason = 'Illegal move: cannot take own pieces.'
            return [False, reason]
        
        if self.blocked_by_piece(move): 
            reason = 'Illegal move: attempting to move piece through other piece (excludes knights)'
            return [False, reason]
        
        if self.this_move_puts_me_in_check(move): 
            reason = 'Illegal move: this move puts you in check'
            return [False, reason]

        rank,file = move[0]
        piece = self.board["Pieces"][rank][file]
        match piece:
            case 'Kn': 
                if not self.move_obeys_knight_movement_rules(move): 
                    reason = 'Illegal move: a knight cannot move like that'
                    return [False, reason]
                
            case 'Ca':
                relative_position = self.relative_posistion_from_move(move)
                move_obeys_castle_movement_rules = (relative_position[0] == 0 or relative_position[1]==0)

                if not move_obeys_castle_movement_rules: 
                    reason = 'Illegal move: a castle cannot move like that'
                    return [False, reason]
                
            case 'Bi':
                relative_position = self.relative_posistion_from_move(move)
                move_obeys_bishop_movement_rules = abs(relative_position[0]) == abs(relative_position[1])

                if not move_obeys_bishop_movement_rules: 
                    reason = 'Illegal move: a bishop cannot move like that'
                    return [False, reason]
                
            case 'Qu':
                relative_position = self.relative_posistion_from_move(move)
                move_obeys_queen_movement_rules = abs(relative_position[0]) == abs(relative_position[1]) or (relative_position[0] == 0 or relative_position[1]==0)
                
                if not move_obeys_queen_movement_rules: 
                    reason = 'Illegal move: a queen cannot move like that'
                    return [False, reason]
                
            case 'Ki':
                relative_position = self.relative_posistion_from_move(move)
                move_obeys_king_movement_rules = abs(relative_position[0]) <= 1 and abs(relative_position[1] <= 1)

                if not move_obeys_king_movement_rules: 
                    reason = 'Illegal move: a king cannot move like that'
                    return [False, reason]

            case 'Pa': 
                relative_position = self.relative_position_from_move(move)
                
                if piece_to_move_colour == 'B': 
                    forward_direction = -1
                    is_first_move = move[0][0] == 1
                elif piece_to_move_colour == 'W': 
                    forward_direction = 1
                    is_first_move = move[0][0] == 6
                
                if not relative_position[0] / abs(relative_position[0]) == forward_direction: 
                    reason = 'Illegal move: tried move a pawn backward'
                    return [False, reason]
                
                if not is_first_move: 
                    if not relative_position[0] <= 1: 
                        reason = 'Illegal move: tried to move a pawn by more than 1 place after it\'s already moved'
                        return [False,reason]
                else : 
                    if not relative_position[0] <= 2: 
                        reason = 'Illegal move: tried to move pawn by more than 2 places'
                        return [False, reason]

                move_is_a_take = self.is_move_a_take(move)
                if not move_is_a_take and relative_position[1] > 0: 
                    reason = 'Illegal move: tried to move a pawn horizontally without taking'
                    return [False, reason]
                
                if move_is_a_take and relative_position[1] > 1: 
                    reason = 'Illegal move: tried to move a pawn further than 1 square horizontally'
                    return [False, reason]
                    
                return [True, reason] 
                
            case '': 
                raise ValueError('Trying to move a piece that does not exist. This error should have been handled elsewhere as well.')
        
        return [True, reason]

    def move_obeys_knight_movement_rules(self, move):
        '''
        Checks if a move obeys knight movement rules. 
        '''
        move_obeys_knight_movement_rules = False
        relative_position = self.relative_posistion_from_move(move)

        allowed_relative_positions = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]

        for allowed_relative_position in allowed_relative_positions: 
            if relative_position == allowed_relative_position: 
                move_obeys_knight_movement_rules = True
        
        return move_obeys_knight_movement_rules

    def move_piece(self, move): 
        '''
        This function handles moving a piece to a new location. 'move' is a list of length two with the starting location 
        of the piece to be moved in the first entry and the final location in the second entry. 

        Returns True to indicate success and False to indicate failure. 
        '''
        move_is_legal, reason = self.is_move_legal(move)
        if not move_is_legal: 
            self.handle_error('Illegal move.')
    
            return [False, reason]
        
        move_is_taking_a_piece = self.is_move_a_take(move)

        rank, file = move[0]
        piece = self.board["Pieces"][rank][file]
        colour = self.board["Colours"][rank][file]

        self.board["Pieces"][rank][file] = ''
        self.board["Colours"][rank][file] = ''

        rank, file = move[1]
        self.board["Pieces"][rank][file] = piece
        self.board["Colours"][rank][file] = colour

        self.update_whose_turn_it_is()

        if move_is_taking_a_piece: 
            self.update_material_scores()

        return [True, '']

    def update_whose_turn_it_is(self):
        ''' Updates the whose turn is is flag '''
        if self.player_whose_turn_it_is == 'W': 
            self.player_whose_turn_it_is = 'B'
        elif self.player_whose_turn_it_is == 'B': 
            self.player_whose_turn_it_is = 'W'
        else: 
            raise ValueError('The player whose turn it is is not listed as either black or white. This indicates a bug.')

    def there_is_a_piece_here(self, position): 
        ''' Returns true if there is a piece at the position provied '''
        rank, file = position
        if self.board["Pieces"][rank][file] == '': 
            return False
        else : 
            return True

    def find_any_checks(): 
        pass 
        # To do

