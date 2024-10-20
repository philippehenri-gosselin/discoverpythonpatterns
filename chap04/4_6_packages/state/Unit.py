from .GameItem import GameItem


class Unit(GameItem):
    def __init__(self, position, tile):
        super().__init__(position, tile)
        self.weaponTarget = (0, 0)
        self.lastBulletEpoch = -100
