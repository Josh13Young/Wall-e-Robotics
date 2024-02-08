import brickpi3
import graph
import random

from abc import ABC
import time


class Bot:
    def __init__(self):
        self.BP = brickpi3.BrickPi3()
        self.motorR = self.BP.PORT_C
        self.motorL = self.BP.PORT_B

    def set_left_power(self, power: int):
        self.BP.set_motor_power(self.motorL, power)

    def set_right_power(self, power: int):
        self.BP.set_motor_power(self.motorR, power)

    def set_left_position(self, position: int):
        self.BP.set_motor_position(self.motorL, position)

    def set_right_position(self, position: int):
        self.BP.set_motor_position(self.motorR, position)

    def get_right_position(self) -> int:
        return self.BP.get_motor_encoder(self.motorR)

    def get_left_position(self) -> int:
        return self.BP.get_motor_encoder(self.motorL)


class ControlBot(ABC):
    def __init__(self, bot: Bot):
        self.bot = bot

    def stop(self):
        self.bot.set_left_power(0)
        self.bot.set_right_power(0)


class PowerControlBot(ControlBot):
    def __init__(self, bot: Bot, speed):
        super().__init__(bot)
        self.speed = speed

    def _set_speeds(self, speed_left: int, speed_right: int) -> "PowerControlBot":
        self.bot.set_left_power(speed_left)
        self.bot.set_right_power(speed_right)
        return self

    def move_forward(self) -> "PowerControlBot":
        return self._set_speeds(self.speed, self.speed)

    def move_backward(self) -> "PowerControlBot":
        return self._set_speeds(-self.speed, -self.speed)

    def turn_right(self) -> "PowerControlBot":
        return self._set_speeds(self.speed, -self.speed)

    def turn_left(self) -> "PowerControlBot":
        return self._set_speeds(-self.speed, self.speed)

    def move_forward_right(self) -> "PowerControlBot":
        return self._set_speeds(self.speed, self.speed / 2)

    def move_forward_left(self) -> "PowerControlBot":
        return self._set_speeds(self.speed / 2, self.speed)

    def move_back_right(self) -> "PowerControlBot":
        return self._set_speeds(-self.speed, -self.speed / 2)

    def move_back_left(self) -> "PowerControlBot":
        return self._set_speeds(-self.speed / 2, self.speed)

    def stop(self) -> "PowerControlBot":
        return self._set_speeds(0, 0)


class PositionControlBot(ControlBot):
    def __init__(self, bot: Bot, base_move_dist: int = 800, turn_amount: int = 250):
        super().__init__(bot)
        self.base_move_dist = base_move_dist
        self.turn_amount = turn_amount

    def _move(
        self, right_displacement: int, left_displacement: int
    ) -> "PositionControlBot":
        curr_r = self.bot.get_left_position()
        curr_l = self.bot.get_right_position()
        self.bot.set_left_position(curr_l + left_displacement)
        self.bot.set_right_position(curr_r + right_displacement)
        return self

    def move_forward(self, distance= None) -> "PositionControlBot":
        if distance == None:
            distance = self.base_move_dist
        return self._move(distance, distance)

    def move_backward(self, distance= None) -> "PositionControlBot":
        if distance == None:
            distance = self.base_move_dist
        return self._move(-distance, -distance)

    def turn_left(self, amount= None) -> "PositionControlBot":
        if amount == None:
            amount = self.turn_amount
        return self._move(amount, -amount)

    def turn_right(self, amount= None) -> "PositionControlBot":
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
        graph.square_graph()
        particles = [(0, 0, 0) for _ in range(100)]
        weights = [1/len(particles) for _ in range(len(particles))]
        random.gauss(0, 0.05)

        for _ in range(4):
            for _ in range(4):
                self.move_forward(forward_dist/4)
                time.sleep(1)
                for i in range(100):
                    print ("drawParticles:" + str(particles))
            self.turn_left(turn_amount)
            time.sleep(1)
        return self
