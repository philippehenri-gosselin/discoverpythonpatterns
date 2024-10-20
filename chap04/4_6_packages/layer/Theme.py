import json
import os


class Theme:
    def __init__(self, fileName):
        with open(fileName, encoding='utf-8') as file:
            data = json.load(file)

        self.assetsDir = ".."

        def failIfNotExists(data, section, name):
            if section not in data:
                raise RuntimeError("No section {} in {}".format(section, file))
            data = data[section]
            if name not in data:
                raise RuntimeError("No section {}.{} in {}".format(section, name, file))
            fileName = os.path.join(self.assetsDir, data[name])
            if not os.path.exists(fileName):
                raise RuntimeError("No file {}".format(fileName))
            return fileName

        # Window size
        self.defaultWindowWidth = int(data["defaultWindowWidth"])
        self.defaultWindowHeight = int(data["defaultWindowHeight"])

        # Fonts
        self.titleFont = failIfNotExists(data, "font", "title")
        self.titleSize = int(data["font"]["titleSize"])
        self.menuFont = failIfNotExists(data, "font", "menu")
        self.menuSize = int(data["font"]["menuSize"])
        self.messageFont = failIfNotExists(data, "font", "message")
        self.messageSize = int(data["font"]["messageSize"])

        # Images
        self.cursorImage = failIfNotExists(data, "image", "cursor")

        # Tiles
        tileData = data["tile"]
        self.tileSize = (
            int(tileData["width"]), int(tileData["height"])
        )
        self.groundTileset = failIfNotExists(data, "tile", "ground")
        self.wallsTileset = failIfNotExists(data, "tile", "walls")
        self.unitsTileset = failIfNotExists(data, "tile", "units")
        self.bulletsTileset = failIfNotExists(data, "tile", "explosions")
        self.explosionsTileset = failIfNotExists(data, "tile", "explosions")

        # Sounds and music
        def setIfExists(data, section, name):
            if section not in data:
                return None
            data = data[section]
            if name not in data:
                return None
            fileName = os.path.join(self.assetsDir, data[name])
            return fileName if os.path.exists(fileName) else None

        self.fireSound = setIfExists(data, "sound", "fire")
        self.explosionSound = setIfExists(data, "sound", "explosion")
        self.startMusic = setIfExists(data, "music", "start")
        self.playMusic = setIfExists(data, "music", "play")
        self.victoryMusic = setIfExists(data, "music", "victory")
        self.failMusic = setIfExists(data, "music", "fail")
