from .TiledLayer import TiledLayer


class BulletsLayer(TiledLayer):
    def __init__(self, theme, imageFile, gameState, bullets):
        super().__init__(theme, imageFile)
        self.gameState = gameState
        self.bullets = bullets

    def render(self, surface):
        for bullet in self.bullets:
            if bullet.alive:
                self.drawTile(surface, bullet.position, bullet.tile, bullet.orientation)
