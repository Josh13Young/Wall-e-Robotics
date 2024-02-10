import time

from bot_control.Bot import Bot, ControlBot


class PositionControlBot(ControlBot):
    def __init__(
        self,
        bot: Bot,
        base_move_dist: int = 800,
        turn_amount: int = 250,
        motor_limit: int = 50,
    ):
        super().__init__(bot)
        self.base_move_dist = base_move_dist
        self.turn_amount = turn_amount
        self.bot.set_motor_limits(motor_limit)

    def _move(
        self, right_displacement: int, left_displacement: int
    ) -> "PositionControlBot":
        # loop while we're still moving
        dps_l = self.bot.get_left_velocity_dps()
        dps_r = self.bot.get_right_velocity_dps()
        while dps_l != 0 or dps_r != 0:
            time.sleep(0.1)
            dps_l = self.bot.get_left_velocity_dps()
            dps_r = self.bot.get_right_velocity_dps()

        curr_l = self.bot.get_left_position()
        curr_r = self.bot.get_right_position()
        self.bot.set_left_position(curr_l + left_displacement)
        self.bot.set_right_position(curr_r + right_displacement)
        return self

    def move_forward(self, distance=None) -> "PositionControlBot":
        if distance == None:
            distance = self.base_move_dist
        return self._move(distance, distance)

    def move_backward(self, distance=None) -> "PositionControlBot":
        if distance == None:
            distance = self.base_move_dist
        return self._move(-distance, -distance)

    def turn_left(self, amount=None) -> "PositionControlBot":
        if amount == None:
            amount = self.turn_amount
        return self._move(amount, -amount)

    def turn_right(self, amount=None) -> "PositionControlBot":
        if amount == None:
            amount = self.turn_amount
        return self._move(-amount, amount)

    def move_square(self, forward_dist=833, turn_amount=256) -> "PositionControlBot":
        for _ in range(4):
            self.move_forward(forward_dist)
            time.sleep(1.5)
            self.turn_left(turn_amount)
            time.sleep(1)
        return self

    def move_square_10(self, forward_dist=833, turn_amount=256) -> "PositionControlBot":
        # graph.square_graph()
        particles = [(0, 0, 0) for _ in range(100)]
        weights = [1 / len(particles) for _ in range(len(particles))]
        # random.gauss(0, 0.05)

        for _ in range(4):
            for _ in range(4):
                self.move_forward(forward_dist / 4)
                time.sleep(1)
                for i in range(100):
                    print("drawParticles:" + str(particles))
            self.turn_left(turn_amount)
            time.sleep(1)
        return self
