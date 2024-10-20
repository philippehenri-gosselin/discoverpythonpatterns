import pygame
from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface

from layer.Theme import Theme
from mode.IGameModeObserver import IGameModeObserver
from mode.MainMenuGameMode import MainMenuGameMode
from mode.MessageGameMode import MessageGameMode
from mode.PlayGameMode import PlayGameMode
from mode.PlayMenuGameMode import PlayMenuGameMode
from mode.ThemeMenuGameMode import ThemeMenuGameMode


class UserInterface(IGameModeObserver):
    def __init__(self, theme):
        pygame.init()

        # Rendering
        self.theme = theme
        self.renderWidth = theme.defaultWindowWidth
        self.renderHeight = theme.defaultWindowHeight
        self.rescaledX = 0
        self.rescaledY = 0
        self.rescaledScaleX = 1.0
        self.rescaledScaleY = 1.0

        # Window
        self.window = pygame.display.set_mode((self.renderWidth, self.renderHeight), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("../icon.png"))

        # Modes
        self.playGameMode = None
        self.overlayGameMode = MainMenuGameMode(theme)
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'

        # Music
        if theme.startMusic is not None:
            pygame.mixer.music.load(theme.startMusic)
            pygame.mixer.music.play(loops=-1)

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def gameWon(self):
        self.showMessage("Victory !")
        if self.theme.victoryMusic is not None:
            pygame.mixer.music.load(self.theme.victoryMusic)
            pygame.mixer.music.play(loops=-1)

    def gameLost(self):
        self.showMessage("GAME OVER")
        if self.theme.failMusic is not None:
            pygame.mixer.music.load(self.theme.failMusic)
            pygame.mixer.music.play(loops=-1)

    def loadLevelRequested(self, fileName):
        if self.playGameMode is None:
            self.playGameMode = PlayGameMode()
            self.playGameMode.addObserver(self)
        try:
            self.playGameMode.loadLevel(self.theme, fileName)
            self.renderWidth = self.playGameMode.renderWidth
            self.renderHeight = self.playGameMode.renderHeight
            self.playGameMode.update()
            self.currentActiveMode = 'Play'
        except Exception as ex:
            import traceback
            traceback.print_exc()
            self.playGameMode = None
            self.showMessage("Level loading failed :-(")

        if self.theme.playMusic is not None:
            pygame.mixer.music.load(self.theme.playMusic)
            pygame.mixer.music.play(loops=-1)

    def showGameRequested(self):
        if self.playGameMode is not None:
            self.currentActiveMode = 'Play'

    def showMenuRequested(self, menuName):
        if menuName == "play":
            self.overlayGameMode = PlayMenuGameMode(self.theme)
        elif menuName == "theme":
            self.overlayGameMode = ThemeMenuGameMode(self.theme)
        else:
            self.overlayGameMode = MainMenuGameMode(self.theme)
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'

    def showMessageRequested(self, message):
        self.showMessage(message)
        if self.theme.startMusic is not None:
            pygame.mixer.music.load(self.theme.startMusic)
            pygame.mixer.music.play(loops=-1)

    def showMessage(self, message):
        self.overlayGameMode = MessageGameMode(self.theme, message)
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'

    def changeThemeRequested(self, themeFile):
        try:
            theme = Theme(themeFile)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            self.showMessage(str(ex))
            return
        self.theme = theme
        self.renderWidth = theme.defaultWindowWidth
        self.renderHeight = theme.defaultWindowHeight
        self.playGameMode = None
        self.showMenuRequested("main")

    def quitRequested(self):
        self.running = False

    def run(self):
        while self.running:
            # Inputs and updates are exclusives
            mousePos = pygame.mouse.get_pos()
            mouseX = (mousePos[0] - self.rescaledX) / self.rescaledScaleX
            mouseY = (mousePos[1] - self.rescaledY) / self.rescaledScaleY
            if self.currentActiveMode == 'Overlay':
                self.overlayGameMode.processInput(mouseX, mouseY)
                self.overlayGameMode.update()
            elif self.playGameMode is not None:
                self.playGameMode.processInput(mouseX, mouseY)
                try:
                    self.playGameMode.update()
                except Exception as ex:
                    import traceback
                    traceback.print_exc()
                    self.playGameMode = None
                    self.showMessage("Error during the game update...")

            # Render game (if any), and then the overlay (if active)
            renderWidth = self.renderWidth
            renderHeight = self.renderHeight
            renderSurface = Surface((renderWidth, renderHeight))
            if self.playGameMode is not None:
                self.playGameMode.render(renderSurface)
            else:
                renderSurface.fill((0, 0, 0))
            if self.currentActiveMode == 'Overlay':
                darkSurface = pygame.Surface((renderWidth, renderHeight), flags=pygame.SRCALPHA)
                darkSurface.fill((0, 0, 0, 150))
                renderSurface.blit(darkSurface, (0, 0))
                self.overlayGameMode.render(renderSurface)

            # Compute rescaling values
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

            # Scale rendering to window size
            rescaledSurface = pygame.transform.scale(
                renderSurface, (rescaledWidth, rescaledHeight)
            )
            self.rescaledScaleX = rescaledSurface.get_width() / renderSurface.get_width()
            self.rescaledScaleY = rescaledSurface.get_height() / renderSurface.get_height()
            self.window.blit(rescaledSurface, (self.rescaledX, self.rescaledY))

            # Display
            pygame.display.update()
            self.clock.tick(60)
