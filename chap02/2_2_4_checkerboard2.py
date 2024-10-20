import pygame

pygame.init()
windowWidth = 640
windowHeight = 480
window = pygame.display.set_mode((windowWidth, windowHeight))

running = True
while running:

    eventList = pygame.event.get()
    for event in eventList:
        if event.type == pygame.QUIT:
            running = False

    color = (255, 255, 255)
    width = 80
    height = 80
    cols = windowWidth // (2 * width)
    rows = windowHeight // (2 * width)
    for y in range(rows):
        for x in range(cols):
            rect = (x * 2 * width, y * 2 * height, width, height)
            pygame.draw.rect(window, color, rect)
        for x in range(cols):
            rect = (x * 2 * width + width, y * 2 * height + height, width, height)
            pygame.draw.rect(window, color, rect)

    pygame.display.update()

pygame.quit()
