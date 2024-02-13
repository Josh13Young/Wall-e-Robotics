from common import main_wrapper, curse_print, ControlProcedure
from bot_control.PositionControl import PositionControlBot, Bot


if __name__ == "__main__":
    bot = Bot()
    posControlBot = PositionControlBot(bot, 300)
    curse_print("Moving in a square stop every 10sec")
    posControlBot.move_square_10(forward_dist=833, turn_amount=250)
