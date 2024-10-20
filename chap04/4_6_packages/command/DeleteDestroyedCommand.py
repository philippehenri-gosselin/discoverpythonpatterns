from .Command import Command


class DeleteDestroyedCommand(Command):
    def __init__(self, itemList):
        self.itemList = itemList

    def run(self):
        newList = [item for item in self.itemList if item.alive]
        self.itemList[:] = newList
