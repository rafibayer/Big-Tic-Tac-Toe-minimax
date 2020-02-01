

X = 1
O = 2

class TTTState:

    def __init__(self, old=None, size=3):
        if old is not None:
            self.board = [r[:] for r in old.board]
            self.whose_turn = old.whose_turn
            self.size = old.size
        else:
            if size < 3:
                raise ValueError("Board size must be at least 3x3!")
            self.board = [[0]*size for _ in range(size)]
            self.whose_turn = X
            self.size = size

    
    def __str__(self):
        res = ""
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[r][c] == X:
                    res += "X "
                elif self.board[r][c] == O:
                    res += "O "
                else:
                    res += "_ "
            res += "\n"

        return res

    def __eq__(self, s2):
        return self.board == s2.board and self.whose_turn == s2.whose_turn

    def __hash__(self):
        return hash(str(self) + str(self.whose_turn))

    def win(self):
        board_size = len(self.board)

        for r in self.board:
            if r.count(X) == board_size:
                return "X"
            elif r.count(O) == board_size:
                return "O"

        for i in range(board_size):
            col = [r[i] for r in self.board]
            if col.count(X) == board_size:
                return "X"
            elif col.count(O) == board_size:
                return "O"


        d1 = [] # forward diag
        d2 = [] # backward diag
        for i in range(board_size):
            for j in range(board_size):
                if i == j:
                    d1.append(self.board[i][j])
                    d2.append(self.board[i][board_size-j-1])

        if d1.count(X) == board_size:
            return "X"
        elif d2.count(O) == board_size:
            return "O" 

        # check for any open spaces
        for r in self.board:
            for c in r:
                if c == 0:
                    return False

        return "D"


            


