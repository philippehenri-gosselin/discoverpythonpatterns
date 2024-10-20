import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.clock = pygame.time.Clock()
        self.x = 120
        self.y = 120
        self.running = True

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    self.x += 8
                elif event.key == pygame.K_LEFT:
                    self.x -= 8
                elif event.key == pygame.K_DOWN:
                    self.y += 8
                elif event.key == pygame.K_UP:
                    self.y -= 8

    def update(self):
        pass

    def render(self):
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, (0, 0, 255), (self.x, self.y, 400, 240))
        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)


game = Game()
game.run()
pygame.quit()