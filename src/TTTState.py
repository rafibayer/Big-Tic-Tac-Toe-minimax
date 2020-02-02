import numpy as np
import copy

X = 1
O = 2

class TTTState:

    def __init__(self, old=None, size=3, win_score=None):
        if old is not None:
            self.board = copy.deepcopy(old.board)
            self.whose_turn = old.whose_turn
            self.size = old.size
            self.win_score = old.win_score

        else:
            if size < 3:
                raise ValueError("Board size must be at least 3x3!")
           
            self.board = np.zeros((size,size))
            self.whose_turn = X
            self.size = size
            self.win_score = win_score if win_score is not None else size

          
            if win_score > size:
                raise ValueError("win_score must be <= size")

    
    def __str__(self):
        res = "  " + "".join(str(list(range(1,self.size+1))).split(","))[1:-1]
        res += "\n"
        for r in range(self.size):
            res += str(r+1) + " "
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

    # checks the board for a winning state
    #   returns "X" if player X wins
    #   returns "O" if player O wins
    #   returns "D" if the game is a draw
    #   returns False if the game has no concluded
    def win(self):

        lines = self.extract_lines()

        for l in lines:
            player_counts = {X: np.count_nonzero(l == X), O: np.count_nonzero(l == O)}
            if player_counts[X] == self.win_score:
                return "X"
            elif player_counts[O] == self.win_score:
                return "O"

        if np.any(np.where(self.board == 0)):
            return False

        return "D"


    # get a list of all lines on the board long enough
    # to achieve a win
    # includes partial rows, partial columns, 
    # and partial diagonals, including those above and below the main diagonals
    def extract_lines(self):
        lines = []

        # for each row/col
        for rc in range(self.size):
            # for each win_score length section
            for i in range(0, self.size-self.win_score+1):

                # rows
                row = self.board[rc, i:i+self.win_score]
                if len(row) <= 2:
                    print(row)
                lines.append(row)
                

                # cols
                col = self.board[i:i+self.win_score, rc]
                if len(col) <= 2:
                    print(col)
                lines.append(col)

        # check all diags long enough to contain a winning score
        for i in range(-self.size + self.win_score, self.size-self.win_score+1):

            # get the full diags
            full_diag = np.diag(self.board, i)
            full_reverse_diag = np.diag(np.fliplr(self.board), i)

            for diag in [full_diag, full_reverse_diag]:

                if len(diag) == self.win_score:
                    lines.append(diag)
                else:
                    for j in range(0, len(diag)-self.win_score+1):
                        lines.append(diag[j:j+self.win_score])
           

            

        return lines


# b = [
#     [1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12],
#     [13, 14, 15, 16]
# ]

# b2 = [
#     [1, 2,3],
#     [4, 5,6],
#     [7,8,9]
# ]

# for r in b2:
#     for i in range(0, len(r)-3+1, 1):
#         #print(r[i:i+3])
#         pass

# b2 = np.array(b2)
# for i in range(-3+3,3-3+1):
#     print(np.diag(b2, i))


# TODO: missing some lines (reverse diags?)
if __name__ == "__main__":
    b = TTTState(None, 5, 4)
    print(b)






    


