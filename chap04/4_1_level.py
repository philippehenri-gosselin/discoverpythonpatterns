import math
import os

import pygame
import tmx
from pygame import Rect
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE, SRCALPHA
from pygame.surface import Surface

os.environ['SDL_VIDEO_CENTERED'] = '1'


###############################################################################
#                               Game State                                    #
###############################################################################

class GameItem:
    def __init__(self, state, position, tile):
        self.state = state
        self.alive = True
        self.position = position
        self.tile = tile
        self.orientation = 0


class Unit(GameItem):
    def __init__(self, state, position, tile):
        super().__init__(state, position, tile)
        self.weaponTarget = (0, 0)
        self.lastBulletEpoch = -100


class Bullet(GameItem):
    def __init__(self, state, unit):
        super().__init__(state, unit.position, (2, 1))
        self.unit = unit
        self.startPosition = unit.position
        self.endPosition = unit.weaponTarget


class GameState:
    def __init__(self):
        self.epoch = 0
        self.worldSize = (1, 1)
        self.ground = [[(0, 0)]]
        self.walls = [[(0, 0)]]
        self.units = [[(0, 0)]]
        self.bullets = []
        self.bulletSpeed = 0.1
        self.bulletRange = 4
        self.bulletDelay = 10
        self.observers = []

    def isInside(self, position):
        return 0 <= position[0] < self.worldSize[0] \
               and 0 <= position[1] < self.worldSize[1]

    def findUnit(self, position):
        for unit in self.units:
            if int(unit.position[0]) == int(position[0]) \
                    and int(unit.position[1]) == int(position[1]):
                return unit
        return None

    def findLiveUnit(self, position):
        unit = self.findUnit(position)
        if unit is None or not unit.alive:
            return None
        return unit

    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyUnitDestroyed(self, unit):
        for observer in self.observers:
            observer.unitDestroyed(unit)


class IGameStateObserver():
    def unitDestroyed(self, unit):
        pass


###############################################################################
#                                Commands                                     #
###############################################################################

class Command:
    def run(self):
        raise NotImplementedError()


class MoveCommand(Command):
    def __init__(self, state, unit, moveVector):
        self.state = state
        self.unit = unit
        self.moveVector = moveVector

    def run(self):
        if not self.unit.alive:
            return

        # Update unit orientation
        moveVector = self.moveVector
        if moveVector[0] < 0:
            self.unit.orientation = 90
        elif moveVector[0] > 0:
            self.unit.orientation = -90
        if moveVector[1] < 0:
            self.unit.orientation = 0
        elif moveVector[1] > 0:
            self.unit.orientation = 180

        # Update unit position
        newPos = (
            self.unit.position[0] + moveVector[0],
            self.unit.position[1] + moveVector[1]
        )
        if not (0 <= newPos[0] < self.state.worldSize[0]) \
                or not (0 <= newPos[1] < self.state.worldSize[0]):
            return
        if self.state.walls[newPos[1]][newPos[0]] is not None:
            return
        for unit in self.state.units:
            if newPos == unit.position:
                return
        self.unit.position = newPos


class TargetCommand(Command):
    def __init__(self, state, unit, target):
        self.state = state
        self.unit = unit
        self.target = target

    def run(self):
        self.unit.weaponTarget = self.target


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
        state.bullets.append(Bullet(state, unit))


def vectorAdd(a, b, w=None):
    if w is None:
        return a[0] + b[0], a[1] + b[1]
    return a[0] + w * b[0], a[1] + w * b[1]


def vectorSub(a, b):
    return a[0] - b[0], a[1] - b[1]


def vectorNorm(a):
    return math.sqrt(a[0]**2 + a[1]**2)


def vectorNormalize(a):
    norm = vectorNorm(a)
    if norm < 1e-4:
        return 0, 0
    return a[0] / norm, a[1] / norm


def vectorDist(a, b):
    diff = vectorSub(a, b)
    return vectorNorm(diff)


class MoveBulletCommand(Command):
    def __init__(self, state, bullet):
        self.state = state
        self.bullet = bullet

    def run(self):
        bullet = self.bullet
        state = self.state
        direction = vectorSub(bullet.endPosition, bullet.startPosition)
        direction = vectorNormalize(direction)
        newPos = vectorAdd(bullet.position, direction, state.bulletSpeed)
        # If the bullet goes outside the world, destroy it
        if not state.isInside(newPos):
            bullet.alive = False
            return
        # If the bullet goes towards the target cell, destroy it
        if ((direction[0] >= 0 and newPos[0] >= bullet.endPosition[0])
            or (direction[0] < 0 and newPos[0] <= bullet.endPosition[0])) \
                and ((direction[1] >= 0 and newPos[1] >= bullet.endPosition[1])
                     or (direction[1] < 0 and newPos[1] <= bullet.endPosition[1])):
            bullet.alive = False
            return
        # If the bullet is outside the allowed range, destroy it
        if vectorDist(newPos, bullet.startPosition) > state.bulletRange:
            bullet.alive = False
            return
        # If the bullet hits a unit, destroy the bullet and the unit
        newCenterPos = vectorAdd(newPos, (0.5, 0.5))
        unit = state.findLiveUnit(newCenterPos)
        if unit is not None and unit != bullet.unit:
            bullet.alive = False
            unit.alive = False
            state.notifyUnitDestroyed(unit)
            return
        # Nothing happens, continue bullet trajectory
        bullet.position = newPos


class DeleteDestroyedCommand(Command):
    def __init__(self, itemList):
        self.itemList = itemList

    def run(self):
        newList = [item for item in self.itemList if item.alive]
        self.itemList[:] = newList


###############################################################################
#                                Rendering                                    #
###############################################################################

class Layer(IGameStateObserver):
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
    def __init__(self, ui, imageFile, gameState, array, surfaceFlags=pygame.SRCALPHA):
        super().__init__(ui, imageFile)
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


class UnitsLayer(Layer):
    def __init__(self, ui, imageFile, gameState, units):
        super().__init__(ui, imageFile)
        self.state = gameState
        self.units = units

    def render(self, surface):
        for unit in self.units:
            self.drawTile(surface, unit.position, unit.tile, unit.orientation)
            if not unit.alive:
                continue
            dirX = unit.weaponTarget[0] - unit.position[0]
            dirY = unit.weaponTarget[1] - unit.position[1]
            angle = math.atan2(-dirX, -dirY) * 180 / math.pi
            self.drawTile(surface, unit.position, (4, 1), angle)


class BulletsLayer(Layer):
    def __init__(self, ui, imageFile, gameState, bullets):
        super().__init__(ui, imageFile)
        self.gameState = gameState
        self.bullets = bullets

    def render(self, surface):
        for bullet in self.bullets:
            if bullet.alive:
                self.drawTile(surface, bullet.position, bullet.tile, bullet.orientation)


class ExplosionsLayer(Layer):
    def __init__(self, ui, imageFile):
        super().__init__(ui, imageFile)
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


###############################################################################
#                               Load level                                    #
###############################################################################

class LevelLoader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.state = GameState()

    def decodeLayerHeader(self, tileMap, layer):
        if not isinstance(layer, tmx.Layer):
            raise RuntimeError("Error in {}: invalid layer type".format(self.fileName))
        if len(layer.tiles) != tileMap.width * tileMap.height:
            raise RuntimeError("Error in {}: invalid tiles count".format(self.fileName))

        # Guess which tileset is used by this layer
        gid = None
        for tile in layer.tiles:
            if tile.gid != 0:
                gid = tile.gid
                break
        if gid is None:
            if len(tileMap.tilesets) == 0:
                raise RuntimeError("Error in {}: no tilesets".format(self.fileName))
            tileset = tileMap.tilesets[0]
        else:
            tileset = None
            for t in tileMap.tilesets:
                if gid >= t.firstgid and gid < t.firstgid + t.tilecount:
                    tileset = t
                    break
            if tileset is None:
                raise RuntimeError("Error in {}: no corresponding tileset".format(self.fileName))

        # Check the tileset
        if tileset.columns <= 0:
            raise RuntimeError("Error in {}: invalid columns count".format(self.fileName))
        if tileset.image.data is not None:
            raise RuntimeError("Error in {}: embedded tileset image is not supported".format(self.fileName))

        return tileset

    def decodeArrayLayer(self, tileMap, layer):
        tileset = self.decodeLayerHeader(tileMap, layer)

        array = [None] * tileMap.height
        for y in range(tileMap.height):
            array[y] = [None] * tileMap.width
            for x in range(tileMap.width):
                tile = layer.tiles[x + y * tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError("Error in {}: invalid tile id".format(self.fileName))
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                array[y][x] = (tileX, tileY)

        return tileset, array

    def decodeUnitsLayer(self, state, tileMap, layer):
        tileset = self.decodeLayerHeader(tileMap, layer)

        units = []
        for y in range(tileMap.height):
            for x in range(tileMap.width):
                tile = layer.tiles[x + y * tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError("Error in {}: invalid tile id".format(self.fileName))
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                unit = Unit(state, (x, y), (tileX, tileY))
                units.append(unit)

        return tileset, units

    def run(self):
        # Load map
        if not os.path.exists(self.fileName):
            raise RuntimeError("No file {}".format(self.fileName))
        tileMap = tmx.TileMap.load(self.fileName)

        # Check main properties
        if tileMap.orientation != "orthogonal":
            raise RuntimeError("Error in {}: invalid orientation".format(self.fileName))

        if len(tileMap.layers) != 5:
            raise RuntimeError("Error in {}: 5 layers are expected".format(self.fileName))

        # World size
        self.state = state = GameState()
        state.worldSize = (tileMap.width, tileMap.height)

        # Ground layer
        tileset, array = self.decodeArrayLayer(tileMap, tileMap.layers[0])
        self.tileSize = tileSize = (tileset.tilewidth, tileset.tileheight)
        state.ground[:] = array
        self.groundTileset = tileset.image.source

        # Walls layer
        tileset, array = self.decodeArrayLayer(tileMap, tileMap.layers[1])
        if tileset.tilewidth != tileSize[0] or tileset.tileheight != tileSize[0]:
            raise RuntimeError("Error in {}: tile sizes must be the same in all layers".format(self.fileName))
        state.walls[:] = array
        self.wallsTileset = tileset.image.source

        # Units layer
        tanksTileset, tanks = self.decodeUnitsLayer(state, tileMap, tileMap.layers[2])
        towersTileset, towers = self.decodeUnitsLayer(state, tileMap, tileMap.layers[3])
        if tanksTileset != towersTileset:
            raise RuntimeError("Error in {}: tanks and towers tilesets must be the same".format(self.fileName))
        if tanksTileset.tilewidth != tileSize[0] or tanksTileset.tileheight != tileSize[1]:
            raise RuntimeError("Error in {}: tile sizes must be the same in all layers".format(self.fileName))
        state.units[:] = tanks + towers
        self.unitsTileset = tanksTileset.image.source

        # Bullets and explosions layers
        tileset, array = self.decodeArrayLayer(tileMap, tileMap.layers[4])
        if tileset.tilewidth != tileSize[0] or tileset.tileheight != tileSize[1]:
            raise RuntimeError("Error in {}: tile sizes must be the same in all layers".format(self.fileName))
        self.bulletsTileset = tileset.image.source
        self.explosionsTileset = tileset.image.source


###############################################################################
#                             User Interface                                  #
###############################################################################

class UserInterface:
    def __init__(self, fileName):
        pygame.init()
        self.window = None

        # Load level and init interface
        self.loadLevel(fileName)

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def loadLevel(self, fileName):
        loader = LevelLoader(fileName)
        loader.run()
        
        # Update properties
        self.gameState = state = loader.state
        self.tileWidth = loader.tileSize[0]
        self.tileHeight = loader.tileSize[1]
        self.renderWidth = state.worldSize[0] * self.tileWidth
        self.renderHeight = state.worldSize[1] * self.tileHeight
        self.rescaledX = 0
        self.rescaledY = 0
        self.rescaledScaleX = 1.0
        self.rescaledScaleY = 1.0

        # Layers
        self.layers = [
            ArrayLayer(self, loader.groundTileset, state, state.ground, 0),
            ArrayLayer(self, loader.wallsTileset, state, state.walls),
            UnitsLayer(self, loader.unitsTileset, state, state.units),
            BulletsLayer(self, loader.bulletsTileset, state, state.bullets),
            ExplosionsLayer(self, loader.explosionsTileset)
        ]
        for layer in self.layers:
            self.gameState.addObserver(layer)

        # Window
        if self.window is None:
            windowWidth = 1024
            windowHeight = (windowWidth * self.renderHeight) // self.renderWidth
            self.window = pygame.display.set_mode((windowWidth, windowHeight), HWSURFACE | DOUBLEBUF | RESIZABLE)
            pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
            pygame.display.set_icon(pygame.image.load("icon.png"))

        # Controls
        self.playerUnit = self.gameState.units[0]
        self.commands = []
        
    def processInput(self):
        # Keyboard controls the moves of the player's unit
        moveX = 0
        moveY = 0
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    moveX = 1
                elif event.key == pygame.K_LEFT:
                    moveX = -1
                elif event.key == pygame.K_DOWN:
                    moveY = 1
                elif event.key == pygame.K_UP:
                    moveY = -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseClicked = True

        gameState = self.gameState
        playerUnit = self.playerUnit
        if moveX != 0 or moveY != 0:
            command = MoveCommand(
                gameState, playerUnit, (moveX, moveY)
            )
            self.commands.append(command)

        # Mouse controls the target of the player's unit
        mousePos = pygame.mouse.get_pos()
        mouseX = (mousePos[0] - self.rescaledX) / self.rescaledScaleX
        mouseY = (mousePos[1] - self.rescaledY) / self.rescaledScaleY
        targetCell = (
            mouseX / self.tileWidth - 0.5,
            mouseY / self.tileHeight - 0.5
        )
        command = TargetCommand(gameState, playerUnit, targetCell)
        self.commands.append(command)

        # Other units always target the player's unit
        for unit in gameState.units:
            if unit != playerUnit:
                command = TargetCommand(gameState, unit, playerUnit.position)
                self.commands.append(command)
                distance = vectorDist(unit.position, playerUnit.position)
                if distance <= gameState.bulletRange:
                    self.commands.append(
                        ShootCommand(gameState, unit)
                    )

        # Shoot if left mouse was clicked
        if mouseClicked:
            self.commands.append(
                ShootCommand(gameState, playerUnit)
            )

        # Bullets automatic movement
        for bullet in gameState.bullets:
            self.commands.append(
                MoveBulletCommand(gameState, bullet)
            )

        # Delete any destroyed bullet
        self.commands.append(
            DeleteDestroyedCommand(gameState.bullets)
        )

    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()
        self.gameState.epoch += 1

    def renderWorld(self, surface):
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


userInterface = UserInterface("Level 2.tmx")
userInterface.run()

pygame.quit()
