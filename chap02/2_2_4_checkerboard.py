import pygame

pygame.init()
window = pygame.display.set_mode((640, 480))

running = True
while running:

    eventList = pygame.event.get()
    for event in eventList:
        if event.type == pygame.QUIT:
            running = False

    color = (255, 255, 255)
    width = 80
    height = 80
    for y in range(3):
        for x in range(4):
            rect = (x * 2 * width, y * 2 * height, width, height)
            pygame.draw.rect(window, color, rect)
        for x in range(4):
            rect = (x * 2 * width + width, y * 2 * height + height, width, height)
            pygame.draw.rect(window, color, rect)

    pygame.display.update()

pygame.quit()
