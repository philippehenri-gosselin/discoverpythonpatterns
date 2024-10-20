import pygame

pygame.init()
window = pygame.display.set_mode((640,480))

running = True
while running:

    eventList = pygame.event.get()
    for event in eventList:
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()    
    
pygame.quit()
