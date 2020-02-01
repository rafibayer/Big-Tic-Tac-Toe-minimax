
import numpy as np
from TTTState import *
import time

X = 1
O = 2

DEPTH_BUFFER = 0.1 # buffer in seconds to take off per depth level
MIN_BUFFER_POWER = 25 # after gamesize 9 we start increasing the effetive buffer quickly


class TTTAgent:

    def __init__(self, time_limit=0, maxply=4, use_memo=False):
        if time_limit != 0 and maxply != 4:
            print("Warning, if time limit is not 0, maxply will be ignored")
        self.time_limit = time_limit # time limit in seconds (0 indicates no limit)
        self.maxply = maxply # max depth to search
        self.states_explored = 0 # number of states explored
        self.use_AB = True # whether or not to use Alpha-Beta pruning
        self.use_memo = use_memo

        self.explored = 0
        self.cutoffs = 0

        self.seen_states = dict() # memo of states already evaluated

    # static evaluation function for a state
    def evaluate(self, state):

        # check the memo for this state
        if self.use_memo and state in self.seen_states:
            return self.seen_states[state]

        # otherwise calculate static evaluation heuristic
        score = 0
        lines = []

        board_size = state.size

       

        for i in range(board_size):
            lines.append(state.board[i,:]) # rows
            lines.append(state.board[:,i]) # cols
        lines.append(np.diag(state.board))
        lines.append(np.diag(np.fliplr(state.board)))

        for line in lines:
            X_count = np.count_nonzero(line == X)
            O_count = np.count_nonzero(line == O)

            # X's
            if O_count == 0:
                if X_count == board_size: # X win
                    score += 200 * board_size
                    return score

                for i in range(board_size-1, 0, -1):
                    if X_count == i:
                        score += 10 * (i)

            # O's
            if X_count == 0:

                if O_count == board_size: # o Win
                    score -= 200 * board_size
                    return score

                for i in range(board_size-1, 0, -1):
                    if O_count == i:
                        score -= 10 * (i)


        # add this state to the memo
        if self.use_memo:
            self.seen_states[state] = score
        return score

    # returns all potential moves for a given state
    def getMoves(self, state):
        empty_spots = np.where(state.board == 0)
        return list(zip(empty_spots[0], empty_spots[1]))

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
        return [self.getState(state, m) for m in self.getMoves(state)]

    # picks the best move from state
    def move(self, state):
        potential_moves = self.getMoves(state)
        potential_states = self.getNeighbors(state)

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

            buffer = self.getBuffer(cur_depth, state.size) # time buffer scaling with depth and gamesize
            print(f"buffer: {buffer} at depth: {cur_depth}")
            while time.time() + buffer < start_time + self.time_limit and not done:

                buffer = self.getBuffer(cur_depth, state.size)
                print(f"buffer: {buffer} at depth: {cur_depth}")
                values = [self.minimax(s, cur_depth) for s in potential_states]
                
                if old_vals == values:
                    done = True
                old_vals = values

                cur_depth += 1



        if state.whose_turn == X:
            return potential_moves[np.argmax(values)]
        else:
            return potential_moves[np.argmin(values)]


    # performs a minimax search with max depth maxply
    # (uses Alpha-Beta pruning if use_AB is True)
    def minimax(self, state, plyLeft, alpha=-10e10, beta=10e10):
        if plyLeft == 0 or state.win(): # terminal
            return self.evaluate(state)

        neighbors = self.getNeighbors(state)
       
        # check the memo for this substate
        if self.use_memo:
            for n in neighbors:
                if n in self.seen_states:
                    return self.seen_states[n]

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

    def getBuffer(self, depth, game_size):
            return (depth)**(max(1, game_size - 9)) * DEPTH_BUFFER

    # returns the other players turn marker
    @staticmethod
    def flipTurn(turn):
        if turn == X: return O
        else: return X

   

