import pygame
import Gui_Screen
import Gui_Client
import Network_Client

# ==============================================================================
class Gui_PlanetsScreen(Gui_Screen.Gui_Screen):
# ------------------------------------------------------------------------------
    def __init__(self):
        super(Gui_PlanetsScreen,self).__init__()
        self.__viewport_size    = 8
        self.__planet_list_pos  = 0
        self.planets_to_display = 0
# ------------------------------------------------------------------------------
    def list_planets_to_display(self, player_id):
        planets = []
        for star_id, star in Network_Client.Client.list_stars().items():
            if star.visited_by_player(player_id):
                for object_id in star.v_object_ids:
                    if object_id != 0xffff:
                        planet = self.get_planet(object_id)
                        if planet.is_planet():
                            planets.append(planet)
        return planets
# ------------------------------------------------------------------------------
    def scroll_up(self, step = 1):
        old_start = self.__planet_list_pos
        self.__planet_list_pos = max(0, self.__planet_list_pos - step)
        return old_start != self.__planet_list_pos
# ------------------------------------------------------------------------------
    def scroll_down(self, step = 1):
        old_start = self.__planet_list_pos
        self.__planet_list_pos = min(self.__planet_list_pos + step, len(self.__planets_list) - self.__viewport_size)
        return old_start != self.__planet_list_pos
# ------------------------------------------------------------------------------
    def reset_triggers_list(self):
        self.reset_triggers_list()
        self.add_trigger({'action': "sort",   'sort': "climate",                   'rect': pygame.Rect((442, 200), (58, 25))})
        self.add_trigger({'action': "sort",   'sort': "minerals",                  'rect': pygame.Rect((502, 200), (64, 25))})
        self.add_trigger({'action': "sort",   'sort': "size",                      'rect': pygame.Rect((568, 200), (56, 25))})
        self.add_trigger({'action': "filter", 'filter': "no_enemy_presence",       'rect': pygame.Rect((444, 268), (177, 18))})
        self.add_trigger({'action': "filter", 'filter': "normal_gravity",          'rect': pygame.Rect((444, 291), (177, 18))})
        self.add_trigger({'action': "filter", 'filter': "non_hostile_environment", 'rect': pygame.Rect((444, 314), (177, 18))})
        self.add_trigger({'action': "filter", 'filter': "mineral_abundance",       'rect': pygame.Rect((444, 337), (177, 18))})
        self.add_trigger({'action': "filter", 'filter': "planets_in_range",        'rect': pygame.Rect((444, 360), (177, 18))})
        self.add_trigger({'action': "send_colony_ship",                            'rect': pygame.Rect((457, 390), (150, 18))})
        self.add_trigger({'action': "send_outpost_ship",                           'rect': pygame.Rect((457, 416), (150, 18))})
        self.add_trigger({'action': "ESCAPE",                                      'rect': pygame.Rect((457, 444), (150, 18))})
        self.add_trigger({'action': "SCROLL_UP",                                   'rect': pygame.Rect((422, 15),  (10, 20))})
        self.add_trigger({'action': "SCROLL_DOWN",                                 'rect': pygame.Rect((422, 447), (10, 20))})
        self.add_trigger({'action': "SCROLL_UP",                                   'rect': pygame.Rect((422, 35),  (12, 205))})
        self.add_trigger({'action': "SCROLL_DOWN",                                 'rect': pygame.Rect((422, 240), (12, 205))})

    def draw(self):
        ME                    = self.get_me()
        FONT3                 = Gui_Screen.FONT3
        viewport_font_palette = [0x0, 0x181c40, 0x688cb0]

        self.draw_image_by_key('planets_screen.panel', (0, 0))

        self.__planets_list = self.list_planets_to_display(ME.i_id)
        #TODO: sorting planets

        y = 37
        for planet in self.__planets_list[self.__planet_list_pos:self.__planet_list_pos + self.__viewport_size]:
            star_id        = planet.i_star_id
            name_t         = self.get_star(star_id).s_name
            terrain_t      = planet.get_terrain_text()
            minerals_t     = planet.get_minerals_text()
            size_t         = planet.get_size_text()
            gravity_t      = planet.get_gravity_text()
            name_label     = FONT3.render(name_t,     viewport_font_palette, 2)
            terrain_label  = FONT3.render(terrain_t,  viewport_font_palette, 2)
            gravity_label  = FONT3.render(gravity_t,  viewport_font_palette, 2)
            minerals_label = FONT3.render(minerals_t, viewport_font_palette, 2)
            size_label     = FONT3.render(size_t,     viewport_font_palette, 2)
            planet_image   = Gui_Client.GUI.get_image('starsystem_map', 'planet', planet.get_terrain(), planet.get_size())

            gui.GUI.draw_image(planet_image,   (60 - (planet_image.get_width() // 2), y + 28 - (planet_image.get_height() // 2)))
            gui.GUI.draw_image(name_label,     (60 - (name_label.get_width() // 2), y + 28))
            gui.GUI.draw_image(terrain_label,  (140 - (terrain_label.get_width() // 2), y + 11))
            gui.GUI.draw_image(gravity_label,  (217 - (gravity_label.get_width() // 2), y + 17))
            gui.GUI.draw_image(minerals_label, (311 - (minerals_label.get_width() // 2), y + 11))
            gui.GUI.draw_image(size_label,     (386 - (size_label.get_width() // 2), y + 11))

            #TODO: display industry, population sizes, food prod data, enemy presence...

            y += 55
# ------------------------------------------------------------------------------
    def process_trigger(self, trigger):
        s_action = trigger['action']

        if s_action == "SCROLL_UP":
            if self.scroll_up():
                self.redraw_flip()

        elif s_action == "SCROLL_DOWN":
            if self.scroll_down():
                self.redraw_flip()
# ------------------------------------------------------------------------------
Screen = Gui_PlanetsScreen()
