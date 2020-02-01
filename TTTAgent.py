
from TTTState import *
import time

X = 1
O = 2

DEPTH_BUFFER = 0.25 # buffer in seconds to take off per depth level


class TTTAgent:

    def __init__(self, time_limit=0):
        self.maxply = 5 # max depth to search
        self.states_explored = 0 # number of states explored
        self.use_AB = True # whether or not to use Alpha-Beta pruning
        self.time_limit = time_limit # time limit in seconds (0 indicates no limit)

        self.explored = 0
        self.cutoffs = 0

    # static evaluation function for a state
    def evaluate(self, state):

        score = 0
        lines = []

        board_size = state.size

        # rows
        for r in state.board:
            lines.append(r)

        # cols
        for c in range(board_size):
            lines.append([r[c] for r in state.board])

        # diags
        d1 = [] # forward diag
        d2 = [] # backward diag
        for i in range(board_size):
            for j in range(board_size):
                if i == j:
                    d1.append(state.board[i][j])
                    d2.append(state.board[i][board_size-j-1])

        lines.append(d1)
        lines.append(d2)

        for line in lines:
            X_count = line.count(X)
            O_count = line.count(O)

            # X's
            if O_count == 0:
                if X_count == board_size: # X win
                    score += 100
                elif X_count == board_size-1: # 2X no O
                    score += 10
                elif X_count == board_size-2:
                    score += 1 

            # O's
            if X_count == 0:

                if O_count == board_size: # o Win
                    score -= 100
                elif O_count == board_size-1: # 2O no X
                    score -= 10
                elif O_count == board_size-2:
                    score -= 1

        return score

    # returns all potential moves for a given state
    def getMoves(self, state):

        moves = []

        for r in range(len(state.board)):
            for c in range(len(state.board)):

                # for each empty spot
                if state.board[r][c] == 0:
                    moves.append((r,c))

        return moves

    # returns the succesor state reached from state by taking move
    def getState(self, state, move):
        self.explored += 1

        r = move[0]
        c = move[1]
        
        new_state = TTTState(state) # copy current state
        new_state.board[r][c] = state.whose_turn # place the players marker
        new_state.whose_turn = TTTAgent.flipTurn(state.whose_turn) # # flip the new states turn

        return new_state

    # get all neighboring states to state
    def getNeighbors(self, state):
        moves = self.getMoves(state)
        return [self.getState(state, m) for m in moves]

    # picks the best move from state
    def move(self, state):
        potential_moves = self.getMoves(state)
        potential_states = [self.getState(state, move) for move in potential_moves]

        # if there is no time limit use maxply as limit
        if self.time_limit == 0:
            values = [self.minimax(s, self.maxply) for s in potential_states]

        # perform iterative deepening until time expires
        # (Note, can go over time but branching factor decreases rapidly in later game states)
        else:

            cur_depth = 1
            start_time = time.time()
            old_vals = [] # last iteration values
            values = [] # current iteration values
            done = False # exist early

            buffer = (cur_depth-1)**3 * DEPTH_BUFFER
            while time.time() + buffer < start_time + self.time_limit and not done:
                values = [self.minimax(s, cur_depth) for s in potential_states]
                
                if old_vals == values:
                    done = True
                old_vals = values

                cur_depth += 1



        if state.whose_turn == X:
            return potential_moves[TTTAgent.argmax(values)]
        else:
            return potential_moves[TTTAgent.argmin(values)]


    # performs a minimax search with max depth maxply
    # (uses Alpha-Beta pruning if use_AB is True)
    def minimax(self, state, plyLeft, alpha=-10e10, beta=10e10):
        if plyLeft == 0 or state.win(): # terminal
            return self.evaluate(state)

        neighbors = self.getNeighbors(state)


        # maximizing player
        if state.whose_turn == X:
            value = -10e10
            for n in neighbors:
                value = max(value, self.minimax(n, plyLeft-1, alpha, beta))

                # A-B
                if self.use_AB:
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        self.cutoffs += 1
                        break

            return value

        # minimizing player
        else:
            value = 10e10
            for n in neighbors:
                value = min(value, self.minimax(n, plyLeft-1, alpha, beta))

                # A-B
                if self.use_AB:
                    beta = min(beta, value)
                    if alpha >= beta:
                        self.cutoffs += 1
                        break

        return value



    # index of max element in l
    @staticmethod
    def argmax(l):
        return l.index(max(l))

    # index of min element in l
    @staticmethod
    def argmin(l):
        return l.index(min(l))


    # returns the other players turn marker
    @staticmethod
    def flipTurn(turn):
        if turn == X: return O
        else: return X

