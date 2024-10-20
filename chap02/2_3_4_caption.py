import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
pygame.display.set_icon(pygame.image.load("icon.png"))
clock = pygame.time.Clock()

x = 120
y = 120
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            elif event.key == pygame.K_RIGHT:
                x += 8
            elif event.key == pygame.K_LEFT:
                x -= 8
            elif event.key == pygame.K_DOWN:
                y += 8
            elif event.key == pygame.K_UP:
                y -= 8

    window.fill((0, 0, 0))
    pygame.draw.rect(window, (0, 0, 255), (x, y, 400, 240))
    pygame.display.update()

    clock.tick(60)

pygame.quit()
