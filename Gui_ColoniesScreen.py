import pygame
import Gui_Screen
from Data_CONST import *

BUILD_ITEM_PALETTE = [0x0, 0x141420, 0x6c688c]

# ==============================================================================
class Gui_ColoniesScreen(Gui_Screen.Gui_Screen):

    __view_size  = 10
    __list_start = 0
    __list_size  = 0

# ------------------------------------------------------------------------------
    def __init__(self):
        super(Gui_ColoniesScreen,self).__init__()
# ------------------------------------------------------------------------------
    def reset_triggers_list(self):
        self.Gui_Screen.reset_triggers_list()
        self.add_trigger({'action': "ESCAPE",       'rect': pygame.Rect((534, 448), (77, 19))})
        self.add_trigger({'action': "SCROLL_UP",    'rect': pygame.Rect((620, 16),  (8, 18))})
        self.add_trigger({'action': "SCROLL_DOWN",  'rect': pygame.Rect((620, 318), (8, 18))})
# ------------------------------------------------------------------------------
    def draw(self):
        PLAYERS  = self.list_players()
        COLONIES = self.list_colonies()
        ME       = self.get_me()
        RULES    = self.get_rules()

        self.draw_image_by_key('colonies_screen.panel', (0, 0))

        my_colonies = []
        for colony_id, colony in COLONIES.items():
            if (colony.i_owner_id == ME.i_id) and (not colony.is_outpost()):
                my_colonies.append("%s:%i" % (COLONIES[colony_id].s_name, colony_id))

        my_colonies.sort()
        for i in range(len(my_colonies)):
            colony_id = int(my_colonies[i].split(":")[1])
            my_colonies[i] = COLONIES[colony_id]

        self.__list_size = len(my_colonies)

        for i in range(self.__list_start, min(self.__list_size, self.__list_start + self.__view_size)):
            colony    = my_colonies[i]
            colony_id = colony.i_id
            planet_id = colony.i_planet_id

            if planet_id == 0xffff:
                print colony
                continue

            y = 38 + (31 * (i - self.__list_start))

            self.add_trigger({'action': "screen", 'screen': "colony", 'colony_id': colony_id, 'rect': pygame.Rect((12, y), (85, 24))})

            # production
            colony.debug_production(RULES)  # JWL - how to get turns to completion in colonies display??
            industry_progress  = colony.get_industry_progress()
            industry           = colony.get_industry()
            if industry == 0:
                industry == 0.001  # Prevent div-by-zero crash

            build_item = colony.i_build_item
            if build_item:
                production_id   = build_item['production_id']
                production_name = RULES['buildings'][production_id]['name']
                production_cost = RULES['buildings'][production_id]['cost']
                turns           = (production_cost - industry_progress) / industry
                turns           = 1 if turns < 1 else int(turns + 0.99)
                turns           = 9999 if turns > 9999 else turns
                turns_txt       = "    %d turns" % turns
                write_text(K_FONT2, BUILD_ITEM_PALETTE, 512, y, production_name)
                write_text(K_FONT2, BUILD_ITEM_PALETTE, 512, y+10, turns_txt)

            self.add_trigger({'action': "screen", 'screen': "colony_production", 'colony_id': colony_id, 'rect': pygame.Rect((513, y), (85, 24))})

            write_text(K_FONT_3, BUILD_ITEM_PALETTE, 12, y + 5, colony.s_name, 2)

            for t in (K_FARMER, K_WORKER, K_SCIENTIST):
                if t == K_FARMER:
                    x = 101
                    icon = 1
                elif t == K_WORKER:
                    x = 236
                    icon = 3
                elif t == K_SCIENTIST:
                    x = 378
                    icon = 5

                c = len(colony.colonists[t])
                if c < 5:
                    xx = 28
                else:
                    xx = 114 / c

                for ii in range(c):
                    colonist = colony.colonists[t][ii]
                    race     = colonist['race']
                    picture  = PLAYERS[race].i_picture
                    self.draw_image_by_key('race_icon.%i.%i' % (picture, icon), (x + (xx * ii), y))
# ------------------------------------------------------------------------------
    def scroll_up(self, step = 1):
        old_start = self.__list_start
        self.__list_start = max(0, self.__list_start - step)
        if old_start != self.__list_start:
            self.redraw_flip()
# ------------------------------------------------------------------------------
    def scroll_down(self, step = 1):
        old_start = self.__list_start
        self.__list_start = min(self.__list_start + step, self.__list_size - self.__view_size + 1)
        if old_start != self.__list_start:
            self.redraw_flip()
# ------------------------------------------------------------------------------
    def process_trigger(self, trigger):

        s_action = trigger['action']
        if s_action == "SCROLL_UP":
            self.scroll_up()

        elif s_action == "SCROLL_DOWN":
            self.scroll_down()

# ------------------------------------------------------------------------------
Screen = Gui_ColoniesScreen()
