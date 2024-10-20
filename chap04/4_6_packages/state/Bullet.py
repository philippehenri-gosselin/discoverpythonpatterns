from .GameItem import GameItem


class Bullet(GameItem):
    def __init__(self, unit):
        super().__init__(unit.position, (2, 1))
        self.unit = unit
        self.startPosition = unit.position
        self.endPosition = unit.weaponTarget
