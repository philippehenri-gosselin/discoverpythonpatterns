import pygame

from .Layer import Layer


class SoundLayer(Layer):
    def __init__(self, theme):
        super().__init__(theme)
        if theme.fireSound is not None:
            self.fireSound = pygame.mixer.Sound(theme.fireSound)
            self.fireSound.set_volume(0.2)
        else:
            self.fireSound = None
        if theme.explosionSound is not None:
            self.explosionSound = pygame.mixer.Sound(theme.explosionSound)
            self.explosionSound.set_volume(0.2)
        else:
            self.explosionSound = None

    def unitDestroyed(self, unit):
        if self.explosionSound is not None:
            self.explosionSound.play()

    def bulletFired(self, unit):
        if self.fireSound is not None:
            self.fireSound.play()

    def render(self, surface):
        pass
