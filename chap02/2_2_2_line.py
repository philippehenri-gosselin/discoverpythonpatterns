import pygame

pygame.init()
window = pygame.display.set_mode((640, 480))

running = True
while running:

    eventList = pygame.event.get()
    for event in eventList:
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.line(window, (255, 0, 255), (0, 480), (640, 0), 2)

    pygame.display.update()

pygame.quit()
