import pygame

unitsTexture = pygame.image.load("units.png")
window = pygame.display.set_mode((256, 256))
location = pygame.math.Vector2(96, 96)
rectangle = pygame.Rect(64, 0, 64, 64)
window.blit(unitsTexture, location, rectangle)

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    pygame.display.update()

pygame.quit()
