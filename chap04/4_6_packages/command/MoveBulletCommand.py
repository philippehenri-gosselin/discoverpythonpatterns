from .Command import Command
from tools.vector import vectorAdd, vectorSub, vectorNormalize, vectorDist


class MoveBulletCommand(Command):
    def __init__(self, state, bullet):
        self.state = state
        self.bullet = bullet

    def run(self):
        bullet = self.bullet
        state = self.state
        direction = vectorSub(bullet.endPosition, bullet.startPosition)
        direction = vectorNormalize(direction)
        newPos = vectorAdd(bullet.position, direction, state.bulletSpeed)
        # If the bullet goes outside the world, destroy it
        if not state.isInside(newPos):
            bullet.alive = False
            return
        # If the bullet goes towards the target cell, destroy it
        if ((direction[0] >= 0 and newPos[0] >= bullet.endPosition[0])
            or (direction[0] < 0 and newPos[0] <= bullet.endPosition[0])) \
                and ((direction[1] >= 0 and newPos[1] >= bullet.endPosition[1])
                     or (direction[1] < 0 and newPos[1] <= bullet.endPosition[1])):
            bullet.alive = False
            return
        # If the bullet is outside the allowed range, destroy it
        if vectorDist(newPos, bullet.startPosition) > state.bulletRange:
            bullet.alive = False
            return
        # If the bullet hits a unit, destroy the bullet and the unit
        newCenterPos = vectorAdd(newPos, (0.5, 0.5))
        unit = state.findLiveUnit(newCenterPos)
        if unit is not None and unit != bullet.unit:
            bullet.alive = False
            unit.alive = False
            state.notifyUnitDestroyed(unit)
            return
        # Nothing happens, continue bullet trajectory
        bullet.position = newPos





