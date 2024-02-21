from common import main_wrapper, ControlProcedure
from bot_control.PositionControl import PositionControlBot, Bot


if __name__ == "__main__":
    bot = Bot()
    posControlBot = PositionControlBot(bot, 200)
    posControlBot.move_square_10(forward_dist=833, turn_amount=270)
