from checkers.board import Board
from functools import reduce
import random

def other_player_id(player):
    return 3 - player

class Player:
    
    def __init__(self):
        self.board = Board()

    def set_player_id(self, player_id):
        self.player_id = player_id

    def handle_move(self, move):
        self.board = self.board.create_new_board_from_move(move)

    def choose_move(self):
        raise RuntimeError("Not implemented")

class BoardTreeNode:

    def __init__(self, board, host_id, depth, estimator, move = None):
        self.board = board
        self.host_id = host_id
        self.depth = depth
        self.estimator = estimator
        self.move = move
        self.score = None
        self.sons = []

    def process_score(self, optimize=False, bound=None):
        if (self.depth == 0 or not self.board.get_possible_moves()):
            self.score = self.estimator(self.board)
            return
        core_func = (max if self.board.player_turn == self.host_id else min)
        self.score = None
        for move in self.board.get_possible_moves():
            self.sons.append(BoardTreeNode(self.board.create_new_board_from_move(move), self.host_id, self.depth - 1, self.estimator, move))
            self.sons[-1].process_score(optimize, self.score)
            if (self.score == None):
                self.score = self.sons[-1].score
            else:
                self.score = core_func(self.score, self.sons[-1].score)

            if (optimize and bound != None and core_func(bound, self.score) == self.score):
                return

    def choose_best_move(self):
        best_node = None
        for son in self.sons:
            if (best_node == None or son.score > best_node.score):
                best_node = son
        return best_node.move


class BasicMinimaxPlayer(Player):
    
    def __init__(self, depth, optimize=False):
        self.depth = depth
        self.optimize = optimize
        super().__init__() 

    def choose_move(self):
        root = BoardTreeNode(self.board, self.player_id, self.depth, self.get_grade)
        root.process_score(self.optimize)
        return root.choose_best_move()
    
    def easy_estimation(self, board, player):
        if (board.get_possible_moves()):
            raise RuntimeError("Not possible")
        return 1e9 * (1 if board.player_turn != player else -1)
        
    def get_grade(self, board):
        raise RuntimeError("Not implemented")
    

class EasyPlayer(BasicMinimaxPlayer):
   
    def __init__(self):
        super().__init__(2, optimize=False)  
 
    def estimate_player_pieces(self, board, player):
        cost = 0
        for piece in board.searcher.get_pieces_by_player(player):
            cost += 1000
        return cost

    def get_grade(self, board):
        try:
            return self.easy_estimation(board, self.player_id)
        except RuntimeError:
            pass 
        diff = self.estimate_player_pieces(board, self.player_id) - self.estimate_player_pieces(board, other_player_id(self.player_id))
        return diff
        
class HardPlayer(BasicMinimaxPlayer):
   
    def __init__(self):
        super().__init__(6, optimize=True)

    def estimate_player_pieces(self, board, player):
        cost = 0
        for piece in board.searcher.get_pieces_by_player(player):
            cost += (5000 if piece.king else 1000)
        return cost

    def get_grade(self, board):
        try:
            return self.easy_estimation(board, self.player_id)
        except RuntimeError:
            pass 
        diff = self.estimate_player_pieces(board, self.player_id) - self.estimate_player_pieces(board, other_player_id(self.player_id))
        return diff
