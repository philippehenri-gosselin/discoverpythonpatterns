class GameItem:
    def __init__(self, position, tile):
        self.alive = True
        self.position = position
        self.tile = tile
        self.orientation = 0
