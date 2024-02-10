from bot_control.Bot import Bot, ControlBot

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
