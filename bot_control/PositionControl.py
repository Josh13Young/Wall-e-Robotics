import time
import math

from bot_control.Bot import Bot, ControlBot


class PositionControlBot(ControlBot):
    def __init__(self, bot: Bot, base_move_dist: int = 800, turn_amount: int = 250):
        super().__init__(bot)
        self.base_move_dist = base_move_dist
        self.turn_amount = turn_amount

    def _move(
        self, right_displacement: int, left_displacement: int
    ) -> "PositionControlBot":
        self.wait_for_movement_completion()

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

        # Draws square graph
        line1 = (0, 0, 0, 500)
        line2 = (500, 500, 500, 0)
        line3 = (0, 500, 500, 500)
        line4 = (0, 0, 500, 0)
        print("drawLine:" + str(line1))
        print("drawLine:" + str(line2))
        print("drawLine:" + str(line3))
        print("drawLine:" + str(line4))


        particles = [(0, 0, 0) for _ in range(100)]
        weights = [1 / len(particles) for _ in range(len(particles))]
        ten_cm = forward_dist / 4

        for _ in range(4):
            for _ in range(4):
                self.move_forward(ten_cm)
                time.sleep(1)
                for particle in particles:
                    e = random.gauss(0, 0.04)
                    f = random.gauss(0, 0.06)
                    theta = particle[2]
                    particle[0] += (ten_cm + e) * math.cos(theta)
                    particle[1] += (ten_cm + e) * math.sin(theta)
                    particle[2] += f
                print("drawParticles:" + str(particles))
            self.turn_left(turn_amount)
            for particle in particles:
                g = random.gauss(0, 0.03)
                particle[2] += turn_amount + g
            print("drawParticles:" + str(particles))
            time.sleep(1)
        return self
