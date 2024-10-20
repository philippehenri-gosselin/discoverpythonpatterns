import pygame


class Menu:

    def __init__(self):
        # Windows
        pygame.init()
        self.window = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("icon.png"))

        # Font
        self.titleFont = pygame.font.Font("BD_Cartoon_Shout.ttf", 72)
        self.itemFont = pygame.font.Font("BD_Cartoon_Shout.ttf", 48)

        # Menu items
        self.menuItems = [
            {
                'title': 'Level 1',
                'action': lambda: self.loadLevel("Level 1.tmx")
            },
            {
                'title': 'Level 2',
                'action': lambda: self.loadLevel("Level 2.tmx")
            },
            {
                'title': 'Quit',
                'action': lambda: self.exitMenu()
            }
        ]
        self.currentMenuItem = 0
        self.menuCursor = pygame.image.load("cursor.png")

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def loadLevel(self, fileName):
        print("Load", fileName)

    def exitMenu(self):
        self.running = False

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitMenu()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.currentMenuItem < len(self.menuItems) - 1:
                        self.currentMenuItem += 1
                elif event.key == pygame.K_UP:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_RETURN:
                    menuItem = self.menuItems[self.currentMenuItem]
                    try:
                        menuItem['action']()
                    except Exception as ex:
                        print(ex)

    def update(self):
        pass

    def render(self):
        self.window.fill((0, 0, 0))

        # Initial y
        y = 50

        # Title
        surface = self.titleFont.render("TANK BATTLEGROUNDS !!", True, (200, 0, 0))
        x = (self.window.get_width() - surface.get_width()) // 2
        self.window.blit(surface, (x, y))
        y += (200 * surface.get_height()) // 100

        # Compute menu width
        menuWidth = 0
        for item in self.menuItems:
            surface = self.itemFont.render(item['title'], True, (200, 0, 0))
            menuWidth = max(menuWidth, surface.get_width())
            item['surface'] = surface

        menuWidth2 = max([
            self.itemFont.render(item['title'], True, (200, 0, 0)).get_width()
            for item in self.menuItems
        ])
        assert menuWidth == menuWidth2

        # Draw menu items
        x = (self.window.get_width() - menuWidth) // 2
        for index, item in enumerate(self.menuItems):
            # Item text
            surface = item['surface']
            self.window.blit(surface, (x, y))

            # Cursor
            if index == self.currentMenuItem:
                cursorX = x - self.menuCursor.get_width() - 10
                cursorY = y + (surface.get_height() - self.menuCursor.get_height()) // 2
                self.window.blit(self.menuCursor, (cursorX, cursorY))

            y += (120 * surface.get_height()) // 100

        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)


menu = Menu()
menu.run()

pygame.quit()
