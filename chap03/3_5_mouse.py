import math
import os

import pygame
from pygame import Rect
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE, SRCALPHA
from pygame.surface import Surface

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Unit:
    def __init__(self, state, position, tile):
        self.state = state
        self.position = position
        self.tile = tile
        self.orientation = 0
        self.weaponTarget = (0, 0)

    def move(self, moveVector):
        raise NotImplementedError()

    def orientWeapon(self, target):
        raise NotImplementedError()


class Tank(Unit):
    def move(self, moveVector):
        # Update tank orientation
        if moveVector[0] < 0:
            self.orientation = 90
        elif moveVector[0] > 0:
            self.orientation = -90
        if moveVector[1] < 0:
            self.orientation = 0
        elif moveVector[1] > 0:
            self.orientation = 180

        # Update tank position
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

    def orientWeapon(self, target):
        self.weaponTarget = target


class Tower(Unit):
    def move(self, moveVector):
        pass

    def orientWeapon(self, target):
        self.weaponTarget = self.state.units[0].position


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

    def update(self, moveTankCommand, targetCommand):
        for unit in self.units:
            unit.move(moveTankCommand)
            unit.orientWeapon(targetCommand)


class Layer:
    def __init__(self, ui, imageFile):
        self.ui = ui
        self.tileset = pygame.image.load(imageFile)

    def drawTile(self, surface, position, tileCoords, angle=None):
        tileWidth = self.ui.tileWidth
        tileHeight = self.ui.tileHeight
        spriteX = position[0] * tileWidth
        spriteY = position[1] * tileHeight
        tileX = tileCoords[0] * tileWidth
        tileY = tileCoords[1] * tileHeight
        tileRect = Rect(tileX, tileY, tileWidth, tileHeight)

        if angle is None:
            surface.blit(self.tileset, (spriteX, spriteY), tileRect)
        else:
            tile = pygame.Surface((tileWidth, tileHeight), SRCALPHA)
            tile.blit(self.tileset, (0, 0), tileRect)
            rotatedTile = pygame.transform.rotate(tile, angle)
            spriteX -= (rotatedTile.get_width() - tile.get_width()) // 2
            spriteY -= (rotatedTile.get_height() - tile.get_height()) // 2
            surface.blit(rotatedTile, (spriteX, spriteY))

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
            self.drawTile(surface, unit.position, unit.tile, unit.orientation)
            dirX = unit.weaponTarget[0] - unit.position[0]
            dirY = unit.weaponTarget[1] - unit.position[1]
            angle = math.atan2(-dirX, -dirY) * 180 / math.pi
            self.drawTile(surface, unit.position, (4, 1), angle)


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
        self.rescaledX = 0
        self.rescaledY = 0
        self.rescaledScaleX = 1.0
        self.rescaledScaleY = 1.0

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
        self.moveTankCommand = (0, 0)
        self.targetCommand = (0, 0)

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        moveTankX = 0
        moveTankY = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    moveTankX = 1
                elif event.key == pygame.K_LEFT:
                    moveTankX = -1
                elif event.key == pygame.K_DOWN:
                    moveTankY = 1
                elif event.key == pygame.K_UP:
                    moveTankY = -1
        self.moveTankCommand = (moveTankX, moveTankY)

        # Mouse handling
        mousePos = pygame.mouse.get_pos()
        mouseX = (mousePos[0] - self.rescaledX) / self.rescaledScaleX
        mouseY = (mousePos[1] - self.rescaledY) / self.rescaledScaleY
        self.targetCommand = (
            mouseX / self.tileWidth - 0.5,
            mouseY / self.tileHeight - 0.5
        )

    def update(self):
        self.gameState.update(self.moveTankCommand, self.targetCommand)

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
            self.rescaledX = 0
            self.rescaledY = (windowHeight - rescaledHeight) // 2
        else:
            rescaledWidth = int(windowHeight * renderRatio)
            rescaledHeight = windowHeight
            self.rescaledX = (windowWidth - rescaledWidth) // 2
            self.rescaledY = 0

        # Scale the rendering to the window/screen size
        rescaledSurface = pygame.transform.scale(
            renderSurface, (rescaledWidth, rescaledHeight)
        )
        self.rescaledScaleX = rescaledSurface.get_width() / renderSurface.get_width()
        self.rescaledScaleY = rescaledSurface.get_height() / renderSurface.get_height()
        self.window.blit(rescaledSurface, (self.rescaledX, self.rescaledY))
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
