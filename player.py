import math
import random
import time


class MCTS_Node:

    def __init__(self, parent=None):
        self.parent = parent
        self.choices = {}
        self.rave_visits = 0
        self.rave_wins = 0
        self.visits = 0
        self.wins = 0

    def best_move(self):
        max_score = max(map(lambda node: node.score, self.choices.values()))
        moves = [move for move in self.choices.keys() if self.choices[move].score == max_score]
        return random.choice(moves)

    @property
    def score(self, rave_v=25):
        alpha = (rave_v - self.visits) / rave_v if self.visits < rave_v else 0
        uct_score = (self.wins / self.visits + 2 * math.log(self.parent.visits) / self.visits) if self.visits else 1
        return alpha * (self.rave_wins / self.rave_visits) + (1 - alpha) * uct_score


class MCTS_UCT_AMAF_RAVE:

    def __init__(self, player_id):
        self.mcts_node = MCTS_Node()
        self.player_id = player_id

    def play(self, board, timeout=45):
        for move in self.mcts_node.choices.keys():
            if board.board[move[0]][move[1]]:
                self.mcts_node = self.mcts_node.choices[move]
                self.mcts_node.parent = None

        start = time.monotonic()
        while time.monotonic() - start < timeout * 0.9:
            self.single_search(board)

        next_move = self.mcts_node.best_move()
        self.mcts_node = self.mcts_node.choices[next_move]
        self.mcts_node.parent = None
        return next_move

    def single_search(self, board):
        moves = []
        board = board.clone()
        player_id = self.player_id
        mcts_node = self.mcts_node

        possible_moves = board.get_possible_moves()
        while not (board.check_connection(1) or board.check_connection(2)):
            if len(mcts_node.choices) == len(possible_moves):
                next_move = mcts_node.best_move()
                possible_moves.remove(next_move)
                moves.append(next_move)
                mcts_node = mcts_node.choices[next_move]
                board.place_piece(next_move[0], next_move[1], player_id)
                player_id = 3 - player_id

            else:
                populated = mcts_node.choices.keys()
                next_move = random.choice([move for move in board.get_possible_moves() if move not in populated])
                possible_moves.remove(next_move)
                moves.append(next_move)
                mcts_node.choices[next_move] = MCTS_Node(mcts_node)
                mcts_node = mcts_node.choices[next_move]
                board.place_piece(next_move[0], next_move[1], player_id)
                player_id = 3 - player_id
                break

        random.shuffle(possible_moves)
        while not (board.check_connection(1) or board.check_connection(2)):
            next_move = possible_moves.pop()
            moves.append(next_move)

            if next_move not in mcts_node.choices:
                mcts_node.choices[next_move] = MCTS_Node(mcts_node)

            mcts_node = mcts_node.choices[next_move]
            board.place_piece(next_move[0], next_move[1], player_id)
            player_id = 3 - player_id

        self.update_rave(moves, self.backup(mcts_node))

    @staticmethod
    def backup(mcts_node, flip=True):
        while mcts_node is not None:
            mcts_node.wins += flip
            mcts_node.visits += 1
            mcts_node = mcts_node.parent
            flip = not flip
        return flip

    def update_rave(self, moves, flip):
        mcts_node = self.mcts_node
        for index, next_move in enumerate(moves):
            for move in moves[index:]:
                if move not in mcts_node.choices:
                    mcts_node.choices[move] = MCTS_Node(mcts_node)

                mcts_node.choices[move].rave_wins += flip
                mcts_node.choices[move].rave_visits += 1

            mcts_node = mcts_node.choices[next_move]
            flip = not flip
