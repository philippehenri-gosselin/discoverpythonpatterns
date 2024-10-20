class IGameModeObserver:
    def loadLevelRequested(self, fileName):
        pass

    def showMenuRequested(self, menuName):
        pass

    def showMessageRequested(self, message):
        pass

    def changeThemeRequested(self, themeFile):
        pass

    def showGameRequested(self):
        pass

    def gameWon(self):
        pass

    def gameLost(self):
        pass

    def quitRequested(self):
        pass
