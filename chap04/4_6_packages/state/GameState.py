class GameState:
    def __init__(self):
        self.epoch = 0
        self.worldSize = (1, 1)
        self.ground = [[(0, 0)]]
        self.walls = [[(0, 0)]]
        self.units = [[(0, 0)]]
        self.bullets = []
        self.bulletSpeed = 0.1
        self.bulletRange = 4
        self.bulletDelay = 10
        self.observers = []

    def isInside(self, position):
        return 0 <= position[0] < self.worldSize[0] \
               and 0 <= position[1] < self.worldSize[1]

    def findUnit(self, position):
        for unit in self.units:
            if int(unit.position[0]) == int(position[0]) \
                    and int(unit.position[1]) == int(position[1]):
                return unit
        return None

    def findLiveUnit(self, position):
        unit = self.findUnit(position)
        if unit is None or not unit.alive:
            return None
        return unit

    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyUnitDestroyed(self, unit):
        for observer in self.observers:
            observer.unitDestroyed(unit)

    def notifyBulletFired(self, unit):
        for observer in self.observers:
            observer.bulletFired(unit)
