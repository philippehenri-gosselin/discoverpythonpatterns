from state.IGameStateObserver import IGameStateObserver


class Layer(IGameStateObserver):
    def __init__(self, theme):
        self.theme = theme

    def render(self, surface):
        raise NotImplementedError()
