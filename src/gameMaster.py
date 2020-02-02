

from TTTState import * # gamestate
from Player import * # human player
from TTTAgent import * # AI player

import time


STATS = True

player1 = TTTAgent(time_limit=1, maxply=4, use_memo=True) 
player2 = TTTAgent(time_limit=1, maxply=4, use_memo=True)
# player2 = Player()

X = 1
O = 2

# start a new game with player1 and player2
def run(player1, player2, start_state=None):
    if STATS:
        game_start = time.time()
    print("Welcome to Tic-Tac-Toe!")
    if start_state:
        game = start_state
    else:
        game_size = int(input("Game size: ")) # get the game board size
        
        if game_size == 3:
            win_score = 3
        elif game_size == 4:
            win_score = 4
        else:
            win_score = int(input(f"How many in a row to win? ({game_size-1},{game_size}): "))
            if win_score < game_size-1 or win_score > game_size:
                raise ValueError("Win score out of range, would result in unfair game")


        print(f"Creating a {game_size}x{game_size} board, {win_score} in a row to win...")

        game = TTTState(None, game_size, win_score) # make new game-state of size 

    X_turn = True # X's go first

    while not game.win(): 
        print(game)


        mover = player1 if X_turn else player2 # pick the moving agent
        mover_token = X if X_turn else O # pick the movers token number
        if isinstance(mover, TTTAgent):
                print(f"\t Agent eval: {mover.evaluate(game)}")


        if mover == player1:
            print(f"Player 1's turn ({getToken(mover_token)})")

        else:
            print(f"Player 2's turn ({getToken(mover_token)})")


        start_time = time.time()
        move = mover.move(game)

        if STATS:

            if isinstance(mover, TTTAgent):
                print(f"{getToken(mover_token)}'s states explored: {mover.explored}")
                print(f"{getToken(mover_token)}'s Alpha-Beta cutoffs: {mover.cutoffs}")

                end_time = time.time()

                print(f"Elapsed time: {round(end_time-start_time, 2)}s")
                print(f"Eval: {player1.evaluate(game)}")


        if not validMove(move, game):
            raise ValueError("Invalid move, player forfeits!")

        game.board[move[0]][move[1]] = mover_token
        game.whose_turn = TTTAgent.flipTurn(game.whose_turn)
        X_turn = not X_turn



    if STATS: 
        game_end = time.time()
        print(f"Total game time: {round(game_end-game_start, 2)}")

    print(game)
    winner = game.win()
    if winner == "D":
        print("Draw!")
    else:
        print(f"{winner} has won the game!")

    again = input("Play again? (y/n): ")
    if again == "y":
        run(player1, player2) 

def getToken(num):
    return "X" if num == X else "O"

def validMove(move, game):
    board_size = len(game.board)

    if len(move) != 2:
        print("Move should be row,col!")
        return False

    for p in move:
        if p < 0 or p >= board_size:
            print("Out of bounds!")
            return False

    if game.board[move[0]][move[1]] != 0:
        print("Spot already taken!")
        return False

    return True


X_to_win = TTTState(None, 5, 4)
X_to_win.board = np.array([
    [0, O, X, O, 0],
    [0, X, 0, O, X],
    [0, O, X, X, O],
    [X, 0, 0, O, X],
    [O, 0, 0, 0, 0]
])
X_to_win.whose_turn = X


if __name__ == "__main__":
    print("running")
    run(player1, player2, None)



        



