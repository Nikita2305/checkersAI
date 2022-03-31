from checkers.board import Board
from functools import reduce

class Player:
    
    def __init__(self, player_id):
        self.player_id = player_id
        self.board = Board()

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

    def process_score(self):
        if (self.depth == 0):
            self.score = self.estimator(self.board, self.host_id)
            return
        for move in self.board.get_possible_moves():
            self.sons.append(BoardTreeNode(self.board.create_new_board_from_move(move), self.host_id, self.depth - 1, self.estimator, move))
            self.sons[-1].process_score()
        core_func = (max if self.board.player_turn == self.host_id else min)
        self.score = None
        for son in self.sons:
            if (self.score == None):
                self.score = son.score
            else:
                self.score = core_func(self.score, son.score)

    def choose_best_move(self):
        best_node = None
        for son in self.sons:
            if (best_node == None or son.score > best_node.score):
                best_node = son
        return best_node.move


class BasicMinimaxPlayer(Player):
    
    def __init__(self, player_id, depth, optimize):
        self.depth = depth
        self.optimize = optimize
        super().__init__(player_id) 

    def choose_move(self):
        root = BoardTreeNode(self.board, self.player_id, self.depth, self.get_grade)
        root.process_score()
        return root.choose_best_move()
        
    def get_grade(self, board, player):
        raise RuntimeError("Not implemented")
    

class EasyPlayer(BasicMinimaxPlayer):
   
    def __init__(self, player_id):
        super().__init__(player_id, 3, True)  
 
    def get_grade(self, board, player):
        return 
        
class HardPlayer(BasicMinimaxPlayer):
   
    def __init__(self, player_id):
        super().__init__(player_id, 2, False)
 
    def get_grade(self, board, player):
        return 0