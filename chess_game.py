'''
To do description
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

        self.create_sparse_representation()

    def create_sparse_representation(self): 
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
        print_string = '-----------------------------------------\n'
        for rank in range(8): 
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
            print_string = print_string + '-----------------------------------------\n'

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

    '''To do: the following three functions re-use quite a lot of code. Can you abstract them to reduce repeatition?'''
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

    def is_move_legal(self, move): 
        '''
        This function returns true if a move is legal and false if not. In it's second return it gives the reason.
        '''
        reason = ''
        if self.no_piece_at_start_location(move): 
            reason = 'Illegal move: no piece at start location.'
            return False, reason
        
        if self.same_colour_piece_at_destination(move) :
            reason = 'Illegal move: cannot take own pieces.'
            return False, reason
        
        if self.blocked_by_piece(move): 
            reason = 'Illegal move: attempting to move piece through other piece (excludes knights)'
            return False, reason
        
        rank,file = move[0]
        piece = self.board["Pieces"][rank][file]
        match piece:
            case 'Kn': 
                pass # to do
            case 'Bi':
                pass # to do
            case 'Qu':
                pass
            case 'Ki':
                pass
            case 'Ca':
                pass
            case 'Pa':
                pass
            case other: 
                pass # to do
        pass
        
        return True

    def move_piece(self, move): 
        '''
        This function handles moving a piece to a new location. 'move' is a list of length two with the starting location 
        of the piece to be moved in the first entry and the final location in the second entry. 

        Returns 1 to indicate success and -1 to indicate failure. 
        '''
        if not self.is_move_legal(move): 
            self.handle_error('Illegal move.')
            return -1
        
        rank, file = move[0]
        piece = self.board["Pieces"][rank][file]
        colour = self.board["Colours"][rank][file]

        self.board["Pieces"][rank][file] = ''
        self.board["Colours"][rank][file] = ''

        rank, file = move[1]
        self.board["Pieces"][rank][file] = piece
        self.board["Colours"][rank][file] = colour

        return 1


