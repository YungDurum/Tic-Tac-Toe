import itertools
import random
import copy

class TicTacToe():
    """
    A class to represent a Tic-Tac-Toe game.

    Attributes:
        players (dict): A dictionary mapping player numbers to their symbols.
        EMPTY: A constant representing an empty cell on the board.
        height (int): The height of the Tic-Tac-Toe board.
        width (int): The width of the Tic-Tac-Toe board.
        state (list): A 2D list representing the current state of the board.
        potential_moves (list): A list of possible actions (empty cells) on the board.
        turn (int): The current turn number (0 for player X, 1 for player O).
        starter (int): The player who starts the game (0 or 1).
        anywin (int): A flag to indicate if there is a winner (0 for no winner, 1 for X, 2 for O).
        score (dict): A dictionary to keep track of scores for both players.
    """


    def __init__(self, height = 3, width = 3):
        self.players = { 0:"X", 1: "O" }
        self.EMPTY = None
        self.height = height
        self.width = width
        self.state = [[self.EMPTY] * width for _ in range(height)]
        self.potential_moves= self.possible_actions(self.state)
        self.turn = 0
        self.starter = 0 #initialized with 1 so X starts otherwise the reset in gamerunner cause "O" to start
        self.anywin = 0
        self.score = {"X": 0,"O": 0}
        self.games_played = 0
        
    def next_round(self):
        """
        This will reset the board and will shift the turn to the next player.
        """
        self.state = [[self.EMPTY] * self.width for _ in range(self.height)]
        self.potential_moves= self.possible_actions(self.state)
        self.turn = (self.starter + 1) % 2
        self.starter = (self.starter + 1) % 2

    @classmethod
    def possible_actions(cls,board):
        """
        This is a class method meaning it is also accesible from outside an instance. This is done because it is also being used in the tttAI class.
        """
        pot_moves = set()
        for i, row in enumerate(board):
            for j, element in enumerate(row):
                if element == None:
                    pot_moves.add((i, j))

        return pot_moves
    
    def whoplays(self):
        """
        Returns who is playing depending on who started and how many turns have been played
        """
        if self.turn == self.starter:
            return self.players[self.starter]
        
        else:
            return self.players[self.turn]
        
    def move(self, action):
        """
        Makes a move by checking if the move is possible if its possible the move can me made and the board will be updated
        """
        if action in self.potential_moves:
            self.state[action[0]][action[1]]= self.whoplays()
            self.turn = (self.turn + 1) % 2
            self.potential_moves = self.possible_actions(self.state)
            return True
        return False
 
    def winner(self,board):
        """
        This function checks the board for any winning lines in case it finds
        a winning line it will return the player that has one (so X or O)
        """
        possible_lines = dict()

        possible_lines["row0"] = set()
        possible_lines["row1"] = set()
        possible_lines["row2"] = set()
        possible_lines["column0"] = set()
        possible_lines["column1"] = set()
        possible_lines["column2"] = set()
        possible_lines["diagonal1"] = set()
        possible_lines["diagonal2"] = set()

        for i in range(3):
            for j in range(3):
                if i == 0:
                    possible_lines["row0"].add(board[i][j])
                elif i == 1:
                    possible_lines["row1"].add(board[i][j])
                elif i == 2:
                    possible_lines["row2"].add(board[i][j])

                if j == 0:
                    possible_lines["column0"].add(board[i][j])
                elif j == 1:
                    possible_lines["column1"].add(board[i][j])
                elif j == 2:
                    possible_lines["column2"].add(board[i][j])

                if i == j:
                    possible_lines["diagonal1"].add(board[i][j])
                if i+j == 2:
                    possible_lines["diagonal2"].add(board[i][j])

        for key, value in possible_lines.items():
            if len(value) == 1 and next(iter(value)) is not None: 
                return value.pop()

        return None

    def end(self,board):
        """
        Check if the game has ended. 
        First: it checks for a winner if there is a winner it updates the score.
        Next: it checks for a draw
        """
        winner = self.winner(board)
        if winner:

            self.score[winner] += 1
            return "WIN"

        for row in board:
            for element in row:
                if element == None:
                    return False
  
        return "DRAW"

class tttAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        key = (print(row) for row in state)
        key = (tuple(tuple(row) for row in state), action)

        value = self.q.get(key, 0)

        return value

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        new_q = old_q + self.alpha * (reward + future_rewards - old_q)
        if state is not None:
            state = tuple(tuple(row) for row in state)
        
        self.q[(tuple(state), action)] = new_q

    def best_future_reward(self, board):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        possible_actions = TicTacToe.possible_actions(board)
        if not possible_actions:
            return 0
        max_q_value = -10000
        for action in possible_actions:
            q_value = self.get_q_value(board, action)
            if max_q_value < q_value:
                max_q_value = q_value
        return max_q_value

    def choose_action(self, board, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        possible_actions = TicTacToe.possible_actions(board)
        best_value = -100000
        best_action = None

        if epsilon:
            ran_num = random.random()
            if ran_num <= self.epsilon:
                return random.choice(list(possible_actions))
        else:
            for action in possible_actions:
                value = self.get_q_value(board, action)
                if value > best_value:
                    best_value = value
                    best_action = action
            return best_action
    
def train(n):

    player = tttAI()

    # Play n games
    for i in range(n):
        game = TicTacToe()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = copy.deepcopy(game.state)
            action = player.choose_action(game.state)

            # Keep track of last state and action
            last[game.turn]["state"] = state
            last[game.turn]["action"] = action

            # Make move
            game.move(action)
            new_state = copy.deepcopy(game.state)

            # When game is over, update Q values with rewards
            end = game.end(new_state)
            if end=="WIN":
                player.update(state, action, new_state, 1)
                player.update(
                    last[game.turn]["state"],
                    last[game.turn]["action"],
                    new_state,
                    -1
                )
                break
            
            elif end == "DRAW":
                player.update(state, action, new_state, 0)
                player.update(
                    last[game.turn]["state"],
                    last[game.turn]["action"],
                    new_state,
                    0)
                break
                
            # If game is continuing, no rewards yet
            elif last[game.turn]["state"] is not None:
                player.update(
                    last[game.turn]["state"],
                    last[game.turn]["action"],
                    new_state,
                    0
                )

    # Return the trained AI
    return player

AIplayer = train(1000)

if __name__ == "__main__":
    player = train(10000)
    test = TicTacToe()
    while True:
        if test.player == 1:
            best_action = player.choose_action(test.state)
            test.move(best_action)
        else:
            test.move((int(input("First Index")),int(input("Second Index"))))
        
        print(test.state)

    

