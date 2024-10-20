import pygame

from .TiledLayer import TiledLayer


class ArrayLayer(TiledLayer):
    def __init__(self, theme, imageFile, gameState, array, surfaceFlags=pygame.SRCALPHA):
        super().__init__(theme, imageFile)
        self.state = gameState
        self.array = array
        self.surface = None
        self.surfaceFlags = surfaceFlags

    def render(self, surface):
        if self.surface is None:
            self.surface = pygame.Surface(surface.get_size(), flags=self.surfaceFlags)
            for y in range(self.state.worldSize[1]):
                for x in range(self.state.worldSize[0]):
                    tile = self.array[y][x]
                    if tile is not None:
                        self.drawTile(self.surface, (x, y), tile)
        surface.blit(self.surface, (0, 0))


