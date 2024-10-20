import os

import pygame
from pygame import Rect
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Unit:
    def __init__(self, state, position, tile):
        self.state = state
        self.position = position
        self.tile = tile

    def move(self, moveVector):
        raise NotImplementedError()


class Tank(Unit):
    def move(self, moveVector):
        newPos = (
            self.position[0] + moveVector[0],
            self.position[1] + moveVector[1]
        )

        if not (0 <= newPos[0] < self.state.worldSize[0]) \
                or not (0 <= newPos[1] < self.state.worldSize[0]):
            return

        if self.state.walls[newPos[1]][newPos[0]] is not None:
            return

        for unit in self.state.units:
            if newPos == unit.position:
                return

        self.position = newPos


class Tower(Unit):
    def move(self, moveVector):
        pass


class GameState:
    def __init__(self):
        self.worldSize = (16, 10)
        self.ground = [
            [(5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (5, 1), (5, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1)],
            [(5, 1), (5, 1), (7, 1), (5, 1), (5, 1), (6, 2), (7, 1), (5, 1),
             (5, 1), (5, 1), (6, 4), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2)],
            [(5, 1), (6, 1), (5, 1), (5, 1), (6, 1), (6, 2), (5, 1), (6, 1),
             (6, 1), (5, 1), (6, 2), (7, 1), (5, 1), (5, 1), (5, 1), (5, 1)],
            [(5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (5, 1), (5, 1),
             (5, 1), (5, 1), (6, 2), (5, 1), (5, 1), (5, 1), (5, 1), (7, 1)],
            [(5, 1), (7, 1), (5, 1), (5, 1), (5, 1), (6, 5), (7, 2), (7, 2),
             (7, 2), (7, 2), (8, 5), (6, 1), (5, 1), (5, 1), (5, 1), (5, 1)],
            [(5, 1), (5, 1), (5, 1), (5, 1), (6, 1), (6, 2), (5, 1), (5, 1),
             (5, 1), (5, 1), (6, 2), (5, 1), (5, 1), (5, 1), (5, 1), (7, 1)],
            [(6, 1), (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (5, 1), (5, 1),
             (7, 1), (5, 1), (6, 2), (6, 1), (5, 1), (5, 1), (5, 1), (5, 1)],
            [(5, 1), (6, 4), (7, 2), (7, 2), (7, 2), (8, 4), (5, 1), (5, 1),
             (5, 1), (5, 1), (6, 2), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1)],
            [(5, 1), (6, 2), (5, 1), (5, 1), (5, 1), (7, 1), (5, 1), (5, 1),
             (6, 1), (5, 1), (7, 4), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2)],
            [(5, 1), (6, 2), (5, 1), (6, 1), (5, 1), (5, 1), (5, 1), (5, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1)]
        ]
        self.walls = [
            [None, None, None, None, None, None, None, None, None, (1, 3), (1, 1),
             (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)],
            [None, None, None, None, None, None, None, None, None, (2, 1), None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, (2, 1), None,
             None, (1, 3), (1, 1), (0, 3), None],
            [None, None, None, None, None, None, None, (1, 1), (1, 1), (3, 3),
             None, None, (2, 1), None, (2, 1), None],
            [None, None, None, None, None, None, None, None, None, None, None,
             None, (2, 1), None, (2, 1), None],
            [None, None, None, None, None, None, None, (1, 1), (1, 1), (0, 3),
             None, None, (2, 1), None, (2, 1), None],
            [None, None, None, None, None, None, None, None, None, (2, 1), None,
             None, (2, 1), None, (2, 1), None],
            [None, None, None, None, None, None, None, None, None, (2, 1), None,
             None, (2, 3), (1, 1), (3, 3), None],
            [None, None, None, None, None, None, None, None, None, (2, 1), None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, (2, 3), (1, 1),
             (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
        ]
        self.units = [
            Tank(self, (1, 9), (1, 0)),
            Tower(self, (6, 3), (0, 2)),
            Tower(self, (6, 5), (0, 2)),
            Tower(self, (13, 3), (0, 1)),
            Tower(self, (13, 6), (0, 1))
        ]

    def update(self, moveTankCommand):
        for unit in self.units:
            unit.move(moveTankCommand)


class Layer:
    def __init__(self, ui, imageFile):
        self.ui = ui
        self.tileset = pygame.image.load(imageFile)

    def drawTile(self, surface, position, tile):
        tileWidth = self.ui.tileWidth
        tileHeight = self.ui.tileHeight
        spriteX = position[0] * tileWidth
        spriteY = position[1] * tileHeight
        tileX = tile[0] * tileWidth
        tileY = tile[1] * tileHeight
        tileRect = Rect(tileX, tileY, tileWidth, tileHeight)
        surface.blit(self.tileset, (spriteX, spriteY), tileRect)

    def render(self, surface):
        raise NotImplementedError()


class ArrayLayer(Layer):
    def __init__(self, ui, imageFile, gameState, array):
        super().__init__(ui, imageFile)
        self.state = gameState
        self.array = array

    def render(self, surface):
        for y in range(self.state.worldSize[1]):
            for x in range(self.state.worldSize[0]):
                tile = self.array[y][x]
                if tile is not None:
                    self.drawTile(surface, (x, y), tile)


class UnitsLayer(Layer):
    def __init__(self, ui, imageFile, gameState, units):
        super().__init__(ui, imageFile)
        self.state = gameState
        self.units = units

    def render(self, surface):
        for unit in self.units:
            self.drawTile(surface, unit.position, unit.tile)
            self.drawTile(surface, unit.position, (4, 1))


class UserInterface():
    def __init__(self):
        pygame.init()

        # Game state
        self.gameState = GameState()

        # Rendering properties
        self.tileWidth = 64
        self.tileHeight = 64
        self.renderWidth = self.gameState.worldSize[0] * self.tileWidth
        self.renderHeight = self.gameState.worldSize[1] * self.tileHeight
        gameState = self.gameState
        self.layers = [
            ArrayLayer(self, "ground.png", gameState, gameState.ground),
            ArrayLayer(self, "walls.png", gameState, gameState.walls),
            UnitsLayer(self, "units.png", gameState, gameState.units)
        ]

        # Window
        windowWidth = 1024
        windowHeight = (windowWidth * self.renderHeight) // self.renderWidth
        self.window = pygame.display.set_mode((windowWidth, windowHeight), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.moveTankCommandX = 0
        self.moveTankCommandY = 0

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        self.moveTankCommandX = 0
        self.moveTankCommandY = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    self.moveTankCommandX = 1
                elif event.key == pygame.K_LEFT:
                    self.moveTankCommandX = -1
                elif event.key == pygame.K_DOWN:
                    self.moveTankCommandY = 1
                elif event.key == pygame.K_UP:
                    self.moveTankCommandY = -1

    def update(self):
        self.gameState.update(
            (self.moveTankCommandX, self.moveTankCommandY)
        )

    def renderWorld(self, surface):
        surface.fill((0, 64, 0))
        for layer in self.layers:
            layer.render(surface)

    def render(self):
        # Render scene in a surface
        renderWidth = self.renderWidth
        renderHeight = self.renderHeight
        renderSurface = Surface((renderWidth, renderHeight))
        self.renderWorld(renderSurface)

        # Scale rendering to window size
        windowWidth, windowHeight = self.window.get_size()
        renderRatio = renderWidth / renderHeight
        windowRatio = windowWidth / windowHeight
        if windowRatio <= renderRatio:
            rescaledWidth = windowWidth
            rescaledHeight = int(windowWidth / renderRatio)
            rescaledX = 0
            rescaledY = (windowHeight - rescaledHeight) // 2
        else:
            rescaledWidth = int(windowHeight * renderRatio)
            rescaledHeight = windowHeight
            rescaledX = (windowWidth - rescaledWidth) // 2
            rescaledY = 0

        # Scale the rendering to the window/screen size
        rescaledSurface = pygame.transform.scale(
            renderSurface, (rescaledWidth, rescaledHeight)
        )
        self.window.blit(rescaledSurface, (rescaledX, rescaledY))
        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)


userInterface = UserInterface()
userInterface.run()

pygame.quit()
