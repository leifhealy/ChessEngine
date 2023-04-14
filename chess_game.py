'''
To do description
'''
import dirk
import leif

class ChessGame : 
    '''
    To do description
    '''
    def __init__(self): 
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
                                ['W','W','W','W','W','W','W','W'],
                                ['W','W','W','W','W','W','W','W']]

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
        Print a basic assci representation of the game to the terminal
        '''
        pass