from checkers_engine.players import HardPlayer, EasyPlayer
from checkers_engine.competition import Competition
import traceback
import logging

logger = logging.getLogger("")
ITERATIONS = 5
labels = ["Draw", "HardPlayer", "EasyPlayer"]
for i in range(ITERATIONS):
    try:
        logger.warning(f"Starting new game.")
        comp = Competition(HardPlayer(), EasyPlayer())
        winner = comp.process_game()
        logger.warning(f"End of game. Player={labels[winner]} won!")
    except Exception as error:
        trace = ''.join(traceback.format_list(traceback.extract_tb(error.__traceback__)))
        logger.error(f"Move trouble. Trace:\n{trace}\n\nError: {error}")
        quit()
