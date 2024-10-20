import pygame

from .GameMode import GameMode
from command.DeleteDestroyedCommand import DeleteDestroyedCommand
from command.MoveBulletCommand import MoveBulletCommand
from command.MoveCommand import MoveCommand
from command.ShootCommand import ShootCommand
from command.TargetCommand import TargetCommand
from layer.ArrayLayer import ArrayLayer
from layer.BulletsLayer import BulletsLayer
from layer.ExplosionsLayer import ExplosionsLayer
from layer.SoundLayer import SoundLayer
from layer.UnitsLayer import UnitsLayer
from state.LevelLoader import LevelLoader
from tools.vector import vectorDist


class PlayGameMode(GameMode):
    def loadLevel(self, theme, fileName):
        self.theme = theme

        loader = LevelLoader(fileName)
        loader.run()

        # Update user interface properties
        self.gameState = state = loader.state
        self.tileSize = theme.tileSize
        self.renderWidth = state.worldSize[0] * self.tileSize[0]
        self.renderHeight = state.worldSize[1] * self.tileSize[1]

        # Layers
        self.layers = [
            ArrayLayer(theme, theme.groundTileset, state, state.ground, 0),
            ArrayLayer(theme, theme.wallsTileset, state, state.walls),
            UnitsLayer(theme, theme.unitsTileset, state, state.units),
            BulletsLayer(theme, theme.bulletsTileset, state, state.bullets),
            ExplosionsLayer(theme, theme.explosionsTileset),
            SoundLayer(theme)
        ]
        for layer in self.layers:
            self.gameState.addObserver(layer)

        # Controls
        self.playerUnit = self.gameState.units[0]
        self.commands = []
        self.gameOver = False

    def processInput(self, mouseX, mouseY):
        # Keyboard controls the moves of the player's unit
        moveX = 0
        moveY = 0
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested("main")
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

        # If the game is over, all commands creations are disabled
        if self.gameOver:
            return

        # Move the tank
        gameState = self.gameState
        playerUnit = self.playerUnit
        if moveX != 0 or moveY != 0:
            command = MoveCommand(
                gameState, playerUnit, (moveX, moveY)
            )
            self.commands.append(command)

        # Mouse controls the target of the player's unit
        targetCell = (
            mouseX / self.tileSize[0] - 0.5,
            mouseY / self.tileSize[1] - 0.5
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

        # Check game over
        if not self.playerUnit.alive:
            self.gameOver = True
            self.notifyGameLost()
        else:
            oneEnemyStillLives = False
            for unit in self.gameState.units:
                if unit == self.playerUnit:
                    continue
                if unit.alive:
                    oneEnemyStillLives = True
                    break
            if not oneEnemyStillLives:
                self.gameOver = True
                self.notifyGameWon()

    def render(self, surface):
        for layer in self.layers:
            layer.render(surface)
