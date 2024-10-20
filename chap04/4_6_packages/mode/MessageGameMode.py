import pygame
from pygame import SRCALPHA
from pygame.surface import Surface

from .GameMode import GameMode


class MessageGameMode(GameMode):
    def __init__(self, theme, message):
        super().__init__()
        self.font = pygame.font.Font(theme.messageFont, theme.messageSize)

        width = 0
        height = 0
        lines = message.split("\n")
        surfaces = []
        for line in lines:
            surface = self.font.render(line, True, (200, 0, 0))
            height += surface.get_height()
            width = max(width, surface.get_width())
            surfaces.append(surface)

        y = 0
        mainSurface = Surface((width, height), flags=SRCALPHA)
        for surface in surfaces:
            x = (mainSurface.get_width() - surface.get_width()) // 2
            mainSurface.blit(surface, (x, y))
            y += surface.get_height()
        self.surface = mainSurface

    def processInput(self, mouseX, mouseY):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE \
                        or event.key == pygame.K_SPACE \
                        or event.key == pygame.K_RETURN:
                    self.notifyShowMenuRequested("main")

    def update(self):
        pass

    def render(self, surface):
        x = (surface.get_width() - self.surface.get_width()) // 2
        y = (surface.get_height() - self.surface.get_height()) // 2
        surface.blit(self.surface, (x, y))
