import os
import pygame
from pygame import Rect

os.environ['SDL_VIDEO_CENTERED'] = '1'


class GameState:
    def __init__(self):
        self.worldWidth = 16
        self.worldHeight = 10
        self.tankX = 5
        self.tankY = 4
        self.tower1X = 10
        self.tower1Y = 3
        self.tower2X = 10
        self.tower2Y = 5

    def update(self, moveTankCommandX, moveTankCommandY):
        newTankX = self.tankX + moveTankCommandX
        newTankY = self.tankY + moveTankCommandY

        if 0 <= newTankX < self.worldWidth \
        and 0 <= newTankY < self.worldHeight \
        and not(newTankX == self.tower1X and newTankY == self.tower1Y) \
        and (newTankX != self.tower2X or newTankY != self.tower2Y):
            self.tankX = newTankX
            self.tankY = newTankY


class UserInterface():
    def __init__(self):
        pygame.init()

        # Game state
        self.gameState = GameState()

        # Rendering properties
        self.tileWidth = 64
        self.tileHeight = 64
        self.unitsTileset = pygame.image.load("units.png")

        # Window
        windowWidth = self.gameState.worldWidth * self.tileWidth
        windowHeight = self.gameState.worldHeight * self.tileHeight
        self.window = pygame.display.set_mode((windowWidth, windowHeight))
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
        self.gameState.update(self.moveTankCommandX, self.moveTankCommandY)

    def drawUnit(self, cellX, cellY, tileX, tileY):
        spriteX = cellX * self.tileWidth
        spriteY = cellY * self.tileHeight
        # Base
        tileX = tileX * self.tileWidth
        tileY = tileY * self.tileHeight
        tileRect = Rect(tileX, tileY, self.tileWidth, self.tileHeight)
        self.window.blit(self.unitsTileset, (spriteX, spriteY), tileRect)
        # Gun
        tileX = 4 * self.tileWidth
        tileY = 1 * self.tileHeight
        tileRect = Rect(tileX, tileY, self.tileWidth, self.tileHeight)
        self.window.blit(self.unitsTileset, (spriteX, spriteY), tileRect)

    def render(self):
        self.window.fill((0, 0, 0))

        gameState = self.gameState
        self.drawUnit(gameState.tower1X, gameState.tower1Y, 0, 1)
        self.drawUnit(gameState.tower2X, gameState.tower2Y, 0, 1)
        self.drawUnit(gameState.tankX, gameState.tankY, 1, 0)

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
