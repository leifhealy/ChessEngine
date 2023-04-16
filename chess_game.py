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

        I think there is a bug with this, but I will come back to fix it later. 
        '''
        print_string = ''
        for rank in range(8): 
            for column in range(8):
                square_string = ''
                piece = self.board["Pieces"][rank][column]
                colour = self.board["Colours"][rank][column]

                if colour == 'B':
                    square_string = ' |<piece>| '
                elif colour =='W': 
                    square_string = '  <piece>  '
                
                square_string = square_string.replace('<piece>',piece)

                print_string = print_string + square_string

            print_string = print_string +'\n'

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

    def blocked_by_same_coloured_piece(self, move): 
        '''Returns true if there is a same coloured piece in the way of the move'''
        pass

        # return false if it is a knight

        # check a line between the two locations
        return False

    def is_move_legal(self, move): 
        '''
        This function returns true if a move is legal and false if not. In it's second return it gives the reason.
        '''
        reason = ''
        if self.no_piece_at_start_location(move): 
            reason = 'Illegal move: no piece at start location.'
            return True, reason
        
        if self.same_colour_piece_at_destination(self,move) :
            reason = 'Illegal move: cannot take own pieces.'
            return True, reason
        
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


