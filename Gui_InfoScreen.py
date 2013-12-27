import pygame
import Gui_Screen

TECH_PALETTE = [0x0, 0x082808, 0x0c840c]

# ==============================================================================
class Gui_InfoScreen(Gui_Screen.Gui_Screen):
# ------------------------------------------------------------------------------
    def __init__(self):
        super(Gui_InfoScreen,self).__init__()
        self.__tech_review = "achievements"
# ------------------------------------------------------------------------------
    def reset_triggers_list(self):
        self.Gui_Screen.reset_triggers_list()
        self.add_trigger({'action': "ESCAPE",  'rect': pygame.Rect((547, 441), ( 64, 17))})
# ------------------------------------------------------------------------------
    def draw(self):
        ME = self.get_me()

        Gui_Screen.DISPLAY.fill((0, 0, 0))
        self.blit(self.get_image('info_screen', 'panel'), (0, 0))
        self.blit(self.get_image('info_screen', 'button', 'history_graph',   'off'), (21, 50))
        self.blit(self.get_image('info_screen', 'button', 'tech_review',     'off'), (21, 77))
        self.blit(self.get_image('info_screen', 'button', 'race_statistics', 'off'), (21, 102))
        self.blit(self.get_image('info_screen', 'button', 'turn_summary',    'off'), (21, 128))
        self.blit(self.get_image('info_screen', 'button', 'reference',       'off'), (21, 154))

        # grid behind
        self.blit(self.get_image('app_pic', 0), (433, 115))

        # app image
        self.blit(self.get_image('app_pic', 155), (433, 115))

        tech_carets = []

        if self.__tech_review == "achievements":

            # New Construction Types
            items = []
            for tech_id in [TECH_PLANET_CONSTRUCTION, TECH_TITAN_CONTRUCTION, TECH_TRANSPORT, TECH_OUTPOST_SHIP, TECH_FREIGHTERS, TECH_COLONY_SHIP, TECH_COLONY_BASE]:
                if tech_id in ME.get_known_techs():
                    items.append(tech_id)
            if len(items):
                tech_carets.append({'title': "New Construction Types", 'items': items})

            # Spies
            items = []
            for tech_id in [TECH_TELEPATHIC_TRAINING, TECH_NEURAL_SCANNER, TECH_SPY_NETWORK]:
                if tech_id in ME.get_known_techs():
                    items.append(tech_id)
            if len(items):
                tech_carets.append({'title': "Spies", 'items': items})

        y = 64
        for carret in tech_carets:
            if len(carret['items']):
                self.write_text(K_FONT4, TECH_PALETTE, 223, y, carret['title'], 2)
                y += 16
                for item in carret['items']:
                    text = Data_CONST.get_text_list('TECH_LIST')[item]['name']
                    self.write_text(K_FONT3, TECH_PALETTE, 233, y, text, 2)
                    y += 13
                y += 6
# ------------------------------------------------------------------------------
Screen = Gui_InfoScreen()
