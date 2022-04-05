class Competition:
    def __init__(self, player1, player2):
        player1.set_player_id(1)
        player2.set_player_id(2)
        self.players = [None, player1, player2]
        self.player_index = 1
        self.moves = []

    def draw_check(self):
        n = len(self.moves)
        max_eq = 3
        for r in range(1, 5):
            for i in range(0, max_eq):
                a = n - 4 * i - r
                b = n - r
                if (a < 0 or b < 0 or self.moves[a] != self.moves[b]):
                    return False
        return True
            

    def make_move(self):
        current_board = self.players[self.player_index].board
        self.player_index = current_board.player_turn
        other_index = 3 - self.player_index
        if (not current_board.get_possible_moves()):
            return other_index
        if (self.draw_check()):
            return 0
        move = self.players[self.player_index].choose_move()
        self.moves += [move]
        print(move)
        self.players[self.player_index].handle_move(move)
        self.players[other_index].handle_move(move)
        return None

    def process_game(self):
        while(True):
            winner = self.make_move()
            if (winner != None):
                return winner 
