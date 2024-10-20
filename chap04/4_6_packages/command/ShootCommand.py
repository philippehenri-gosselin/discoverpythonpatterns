from state.Bullet import Bullet
from .Command import Command


class ShootCommand(Command):
    def __init__(self, state, unit):
        self.state = state
        self.unit = unit

    def run(self):
        unit = self.unit
        if not unit.alive:
            return
        state = self.state
        if state.epoch - unit.lastBulletEpoch < state.bulletDelay:
            return
        unit.lastBulletEpoch = state.epoch
        state.bullets.append(Bullet(unit))
        state.notifyBulletFired(self.unit)
