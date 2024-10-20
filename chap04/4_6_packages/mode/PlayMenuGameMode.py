import os

from .MenuGameMode import MenuGameMode


class PlayMenuGameMode(MenuGameMode):
    def __init__(self, theme):
        menuItems = []
        for file in os.listdir(theme.assetsDir):
            name, ext = os.path.splitext(file)
            if ext != ".tmx":
                continue
            file = os.path.join(theme.assetsDir, file)
            menuItems.append({
                'title': name,
                'action': lambda file=file: self.notifyLoadLevelRequested(file)
            })
        menuItems.append({
            'title': 'Back',
            'action': lambda: self.notifyShowMenuRequested("main")
        })
        super().__init__(theme, menuItems)
