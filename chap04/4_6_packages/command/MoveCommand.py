from .Command import Command


class MoveCommand(Command):
    def __init__(self, state, unit, moveVector):
        self.state = state
        self.unit = unit
        self.moveVector = moveVector

    def run(self):
        if not self.unit.alive:
            return

        # Update unit orientation
        moveVector = self.moveVector
        if moveVector[0] < 0:
            self.unit.orientation = 90
        elif moveVector[0] > 0:
            self.unit.orientation = -90
        if moveVector[1] < 0:
            self.unit.orientation = 0
        elif moveVector[1] > 0:
            self.unit.orientation = 180

        # Update unit position
        newPos = (
            self.unit.position[0] + moveVector[0],
            self.unit.position[1] + moveVector[1]
        )
        if not (0 <= newPos[0] < self.state.worldSize[0]) \
                or not (0 <= newPos[1] < self.state.worldSize[0]):
            return
        if self.state.walls[newPos[1]][newPos[0]] is not None:
            return
        for unit in self.state.units:
            if newPos == unit.position:
                return
        self.unit.position = newPos
