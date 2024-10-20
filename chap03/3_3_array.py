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
            [(5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (5, 1), (5, 1), (5, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1)],
            [(5, 1), (5, 1), (7, 1), (5, 1), (5, 1), (6, 2), (7, 1), (5, 1), (5, 1),
             (5, 1), (6, 1), (5, 1), (5, 1), (6, 4), (7, 2), (7, 2)],
            [(5, 1), (6, 1), (5, 1), (5, 1), (6, 1), (6, 2), (5, 1), (6, 1), (6, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (6, 1), (5, 1)],
            [(5, 1), (5, 1), (5, 1), (5, 1), (6, 1), (6, 2), (5, 1), (5, 1), (5, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (5, 1), (7, 1)],
            [(5, 1), (7, 1), (5, 1), (5, 1), (5, 1), (6, 5), (7, 2), (7, 2), (7, 2),
             (7, 2), (7, 2), (7, 2), (7, 2), (8, 5), (5, 1), (5, 1)],
            [(5, 1), (5, 1), (5, 1), (5, 1), (6, 1), (6, 2), (5, 1), (5, 1), (5, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (5, 1), (7, 1)],
            [(6, 1), (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (5, 1), (5, 1), (7, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (7, 1), (5, 1)],
            [(5, 1), (5, 1), (6, 4), (7, 2), (7, 2), (8, 4), (5, 1), (5, 1), (5, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (6, 2), (5, 1), (5, 1)],
            [(5, 1), (5, 1), (6, 2), (5, 1), (5, 1), (7, 1), (5, 1), (5, 1), (6, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (7, 4), (7, 2), (7, 2)],
            [(5, 1), (5, 1), (6, 2), (6, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1),
             (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1)]
        ]
        self.units = [
            Tank(self, (5, 4), (1, 0)),
            Tower(self, (10, 3), (0, 1)),
            Tower(self, (10, 5), (0, 1))
        ]

    def update(self, moveTankCommand):
        for unit in self.units:
            unit.move(moveTankCommand)


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
        self.unitsTileset = pygame.image.load("units.png")
        self.groundTileset = pygame.image.load("ground.png")

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

    def drawGround(self, surface, position, tile):
        spriteX = position[0] * self.tileWidth
        spriteY = position[1] * self.tileHeight
        tileX = tile[0] * self.tileWidth
        tileY = tile[1] * self.tileHeight
        tileRect = Rect(tileX, tileY, self.tileWidth, self.tileHeight)
        surface.blit(self.groundTileset, (spriteX, spriteY), tileRect)

    def drawUnit(self, surface, unit):
        spriteX = unit.position[0] * self.tileWidth
        spriteY = unit.position[1] * self.tileHeight
        # Base
        tileX = unit.tile[0] * self.tileWidth
        tileY = unit.tile[1] * self.tileHeight
        tileRect = Rect(tileX, tileY, self.tileWidth, self.tileHeight)
        surface.blit(self.unitsTileset, (spriteX, spriteY), tileRect)
        # Gun
        tileX = 4 * self.tileWidth
        tileY = 1 * self.tileHeight
        tileRect = Rect(tileX, tileY, self.tileWidth, self.tileHeight)
        surface.blit(self.unitsTileset, (spriteX, spriteY), tileRect)

    def renderWorld(self, surface):
        surface.fill((0, 64, 0))
        gameState = self.gameState

        # Ground
        for y in range(gameState.worldSize[1]):
            for x in range(gameState.worldSize[0]):
                self.drawGround(surface, (x, y), gameState.ground[y][x])

        # Units
        for unit in gameState.units:
            self.drawUnit(surface, unit)

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


