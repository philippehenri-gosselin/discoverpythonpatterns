from .MenuGameMode import MenuGameMode


class MainMenuGameMode(MenuGameMode):
    def __init__(self, theme):
        menuItems = [
            {
                'title': 'Play',
                'action': lambda: self.notifyShowMenuRequested("play")
            },
            {
                'title': 'Select theme',
                'action': lambda: self.notifyShowMenuRequested("theme")
            },
            {
                'title': 'Credits',
                'action': lambda: self.notifyShowMessageRequested("""Credits

Font:
https://www.dafont.com/fr/bd-cartoon-shout.font

Ground/Unit tiles:
https://zintoki.itch.io/ground-shaker

Explosions tiles:
https://opengameart.org/content/explosions-0

Fire sound:
https://freesound.org/people/knova/sounds/170274/

Explosion sound: 
https://freesound.org/people/ryansnook/sounds/110115/

Musics:
https://www.freesfx.co.uk
                """)
            },
            {
                'title': 'Quit',
                'action': lambda: self.notifyQuitRequested()
            }
        ]
        super().__init__(theme, menuItems)
