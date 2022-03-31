from checkers_engine.players import HardPlayer, EasyPlayer
import traceback
import logging

logger = logging.getLogger("")
ITERATIONS = 5
for i in range(ITERATIONS):
    logger.warning(f"Starting new game.")
    players = [None, HardPlayer(1), EasyPlayer(2)] # 1-indexation
    player_index = 1

    while (True):
        current_board = players[player_index].board
        player_index = current_board.player_turn
        other_index = 3 - player_index
        if (not current_board.get_possible_moves()):
            logger.warning(f"End of game. Player{other_index} won!")
            break

        try:
            move = players[player_index].choose_move()
            players[player_index].handle_move(move)
            players[other_index].handle_move(move)
        except Exception as error:
            trace = ''.join(traceback.format_list(traceback.extract_tb(error.__traceback__)))
            logger.error(f"Move trouble. Player_index: {player_index}\n\nTrace:\n{trace}\n\nError: {error}")
            quit()
