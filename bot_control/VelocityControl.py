"""
The LEGO motors have PID control for velocity built in,
  so velocity control on our end just becomes "set the velocity"
"""

from bot_control.Bot import Bot, ControlBot


class VelocityControlBot(ControlBot):
    def __init__(self, bot: Bot, default_dps: int):
        super().__init__(bot)
        self.default_dps = default_dps

    def _set_velocity_dps(self, velocity_dps: int) -> "VelocityControlBot":
        self.bot.set_left_velocity_dps(velocity_dps)
        self.bot.set_right_velocity_dps(velocity_dps)
        return self

    def go_forwards(self, velocity_dps=None) -> "VelocityControlBot":
        dps = velocity_dps if velocity_dps != None else self.default_dps
        return self._set_velocity_dps(dps)

    def go_backwards(self, velocity_dps=None) -> "VelocityControlBot":
        dps = velocity_dps if velocity_dps != None else self.default_dps
        return self._set_velocity_dps(-dps)
