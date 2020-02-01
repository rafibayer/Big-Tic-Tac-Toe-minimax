import numpy as np
import copy

X = 1
O = 2

class TTTState:

    def __init__(self, old=None, size=3):
        if old is not None:
            self.board = copy.deepcopy(old.board)
            self.whose_turn = old.whose_turn
            self.size = old.size
        else:
            if size < 3:
                raise ValueError("Board size must be at least 3x3!")
            self.board = np.zeros((size,size))
            self.whose_turn = X
            self.size = size

    
    def __str__(self):
        res = ""
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == X:
                    res += "X "
                elif self.board[r][c] == O:
                    res += "O "
                else:
                    res += "_ "
            res += "\n"

        return res

    def __eq__(self, s2):
        return np.all(np.equal(self.board, s2.board)) and self.whose_turn == s2.whose_turn

    def __hash__(self):
        return hash(str(self) + str(self.whose_turn))

    def win(self):

        for i in range(self.size):
            # rows
            row = self.board[i,:]
            player_counts = {X: np.count_nonzero(row == X), O: np.count_nonzero(row == O)}
            if player_counts[X] == self.size:
                return "X"
            elif player_counts[O] == self.size:
                return "O"

            col = self.board[:,i]
            player_counts = {X: np.count_nonzero(col == X), O: np.count_nonzero(col == O)}
            if player_counts[X] == self.size:
                return "X"
            elif player_counts[O] == self.size:
                return "O"

            diag = np.diag(self.board)
            player_counts = {X: np.count_nonzero(diag == X), O: np.count_nonzero(diag == O)}
            if player_counts[X] == self.size:
                return "X"
            elif player_counts[O] == self.size:
                return "O"

            reverse_diag = np.diag(np.fliplr(self.board))
            player_counts = {X: np.count_nonzero(reverse_diag == X), O: np.count_nonzero(reverse_diag == O)}
            if player_counts[X] == self.size:
                return "X"
            elif player_counts[O] == self.size:
                return "O"

        # check for any open spaces
        if np.isin(element = 0, test_elements = self.board):
            return False

        return "D"


    


