import math

from .TiledLayer import TiledLayer


class ExplosionsLayer(TiledLayer):
    def __init__(self, theme, imageFile):
        super().__init__(theme, imageFile)
        self.explosions = []
        self.maxFrameIndex = 27

    def add(self, position):
        self.explosions.append({
            'position': position,
            'frameIndex': 0
        })

    def unitDestroyed(self, unit):
        self.add(unit.position)

    def render(self, surface):
        for explosion in self.explosions:
            frameIndex = math.floor(explosion['frameIndex'])
            self.drawTile(surface, explosion['position'], (frameIndex, 4))
            explosion['frameIndex'] += 0.5
        self.explosions = [
            explosion for explosion in self.explosions
            if explosion['frameIndex'] < self.maxFrameIndex
        ]
