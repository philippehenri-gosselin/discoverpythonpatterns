class GameMode:
    def __init__(self):
        self.observers = []

    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyLoadLevelRequested(self, fileName):
        for observer in self.observers:
            observer.loadLevelRequested(fileName)

    def notifyShowMenuRequested(self, menuName):
        for observer in self.observers:
            observer.showMenuRequested(menuName)

    def notifyShowMessageRequested(self, message):
        for observer in self.observers:
            observer.showMessageRequested(message)

    def notifyChangeThemeRequested(self, themeFile):
        for observer in self.observers:
            observer.changeThemeRequested(themeFile)

    def notifyShowGameRequested(self):
        for observer in self.observers:
            observer.showGameRequested()

    def notifyGameWon(self):
        for observer in self.observers:
            observer.gameWon()

    def notifyGameLost(self):
        for observer in self.observers:
            observer.gameLost()

    def notifyQuitRequested(self):
        for observer in self.observers:
            observer.quitRequested()

    def processInput(self, mouseX, mouseY):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def render(self, window):
        raise NotImplementedError()
