import pygame

pygame.init()
window = pygame.display.set_mode((640, 480))

running = True
while running:

    eventList = pygame.event.get()
    for event in eventList:
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(window, (0, 0, 255), (120, 120, 400, 240))

    pygame.display.update()

pygame.quit()
