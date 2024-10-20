import pygame

from layer.Theme import Theme
from ui.UserInterface import UserInterface

defaultTheme = Theme("../Zintoki 64px.json")
userInterface = UserInterface(defaultTheme)
userInterface.run()
pygame.quit()