import pygame
import Gui_Screen

INFO_PALETTE         = [0x0, 0x181c40, 0x688cb0]
TITLE_SHADOW_PALETTE = [0x0, 0x181c40, 0x20284c, 0x20284c]
TITLE_PALETTE        = [0x0, 0x181c40, 0x506c90, 0x445c80]
# ==============================================================================
class Gui_StarsystemScreen(Gui_Screen.Gui_Screen):

    b_panel_moved = False
    i_panel_x_min = 22
    i_panel_x_max = 180
    i_panel_y_min = 22
    i_panel_y_max = 148
    i_panel_x     = 106
    i_panel_y     = 103
# ------------------------------------------------------------------------------
    def __init__(self):
        super(Gui_StarsystemScreen,self).__init__()
# ------------------------------------------------------------------------------
    def __check_panel_moved(self):
        """Returns True if panel's position has changed and resets the moved flag"""
        if self.b_panel_moved:
            self.b_panel_moved = False
            return True
        else:
            return False
# ------------------------------------------------------------------------------
    def open_star(self, i_star_id):
        """Stores the id of a star system which is going to be displayed on this screen"""
        self.i_star_id = i_star_id
# ------------------------------------------------------------------------------
    def get_normalized_panel_pos(self, (x, y)):
        """Returns panel position within allowed ranges to prevent escaping the main window boundaries"""
        return (min(max(x, self.__panel_x_min), self.__panel_x_max), min(max(y, self.__panel_y_min), self.__panel_y_max))
# ------------------------------------------------------------------------------
    def prepare(self):
        """Copy the actual content of MainScreen, it is used on each redraw"""
        self.__BACKGROUND = gui.GUI.get_display().copy()
# ------------------------------------------------------------------------------
    def draw_planet_info(self, text_rows):
        """Draws a semi-transparent minibox in the upper-left corner of the dialog window"""
        info_x, info_y = self.get_normalized_panel_pos((self.__panel_x, self.__panel_y))
        info_x += 15
        info_y += 49
        rows = []
        width, height = 0, 6
        for text_line in text_rows:
            rows.append(self.render(K_FONT3, INFO_PALETTE, text_line))
            height += 13
            width = max(width, rows[-1].get_width())
        width += 8
        info_box = pygame.Surface((width, height))
        info_box.fill(0x000000)
        info_box.set_alpha(128)
        self.blit(info_box, (info_x, info_y))
        pygame.draw.rect(Gui_Screen.DISPLAY, 0x445c80, pygame.Rect((info_x, info_y), (width - 1, height -1)), 2)
        y = info_y + 5
        for row in rows:
            self.blit(row, (info_x + 4, y))
            y += 13
# ------------------------------------------------------------------------------
    def draw(self):
        """Draws the background, starsystem dialog window, planets/asteroids orbit schemes, planets picturesand central star picture"""
        ME                   = self.get_me()
        star_id              = self.i_star_id
        star                 = self.get_star(star_id)
        hover                = self.get_hover()

        X, Y = self.get_normalized_panel_pos((self.i_panel_x, self.i_panel_y))

        self.reset_triggers_list()
        self.add_trigger({'action': "ESCAPE", 'hover_id': "escape_button", 'rect': pygame.Rect((X + 264, Y + 239), (64, 19))})
        self.add_trigger({'action': "drag",   'drag_id': "window_title",   'rect': pygame.Rect((X + 14,  Y + 12),  (319, 26))})

        self.blit(self.__BACKGROUND, (0, 0))

        # dialog window
        self.blit_image((X, Y), 'starsystem_map', 'panel')

        # dialog title
        title_text   = "Star System " + star.get_name()
        title_shadow = self.render(K_FONT5, TITLE_SHADOW_PALETTE, title_text, 2)
        title        = self.render(K_FONT5, TITLE_PALETTE, title_text, 2)
        (tw, th)     = title.get_size()

        self.blit(title_shadow, (X + 174 - (tw / 2), Y + 20))
        self.blit(title,        (X + 173 - (tw / 2), Y + 19))

        if star.visited():
            self.blit_image((X + 156, Y + 120), 'starsystem_map', 'star', star.i_class)

            show_info = None

            for i in range(M_MAX_STAR_OBJECTS):
                planet_id = star.v_object_ids[i]
                if planet_id != 0xffff:
                    planet = self.get_planet(planet_id)

                    # draw a planet/asteroid orbit scheme first
                    if planet.is_asteroid_belt():
                        if i == 0:
                            # FIXME: where are the asteroid belts for objects 1~4 ?
                            self.blit_image((X + 29, Y + 59), 'starsystem_map', 'asteroids', i)
                    elif planet.is_planet() or planet.is_gas_giant():
                        self.blit_image((X + 29, Y + 59), 'starsystem_map', 'orbit', i)

                    x           = X + 200 + (25 * i) + (5 - planet.get_size())
                    y           = Y + 121 + (5 - planet.get_size())
                    hover_id    = "planet_%i" % planet_id
                    planet_size = planet.get_size()
                    planet_info = []

                    if planet.is_gas_giant():
                        planet_image = self.get_image('starsystem_map', 'gas_giant', planet_size)
                        w, h = planet_image.get_size()
                        w -= (10 - planet_size)
                        h -= (10 - planet_size)
                        planet_rect = pygame.Rect((x, y), (w, h))
                        self.blit(planet_image, (x, y))
                        self.add_trigger({'action': "gas_giant", 'planet_id': planet_id, 'hover_id': hover_id, 'rect': planet_rect})
                        planet_info.append("Gas Giant (uninhabitable)")

                    elif planet.is_planet():
                        planet_image = self.get_image('starsystem_map', 'planet', planet.get_terrain(), planet_size)
                        w, h = planet_image.get_size()
                        w -= (10 - planet_size)
                        h -= (10 - planet_size)
                        planet_rect = pygame.Rect((x, y), (w, h))

                        self.blit(planet_image, (x, y))

                        planet_info.append("%s %s" % (star.get_name(), greek_num(i)))
                        planet_info.append("%s, %s" % (planet.size_text(), planet.terrain_text()))

                        colony_id = planet.get_colony_id()

                        if colony_id < 0xffff:
                            colony = networking.Client.get_colony(colony_id)
                            player = networking.Client.get_player(colony.get_owner())

                            if colony.is_owned_by(ME.get_id()) and colony.is_colony():
                                self.add_trigger({'action': "screen", 'screen': "colony", 'colony_id': colony_id, 'hover_id': hover_id, 'rect': planet_rect})
                                planet_info.append("%i / %i pop" % (colony.i_population, colony.i_max_population))
                            else:
                                self.add_trigger({'action': "enemy_colony", 'hover_id': hover_id, 'rect': planet_rect})
                                planet_info.append("??? enemy pop")

                            if colony.is_outpost():
                                subkey = 'outpost_mark'
                            else:
                                subkey = 'colony_mark'
                            self.blit_image((x-6, y), 'starsystem_map', subkey, player.i_color)

                        else:
                            self.add_trigger({'action': "planet", 'planet_id': planet_id, 'hover_id': hover_id, 'rect': planet_rect})
                            planet_info.append("%i max pop" % planet.get_max_population())

                        planet_info.append("%s" % (planet.minerals_text()))

                        # set the info-box content if hover machtes
                    if hover and hover['hover_id'] == hover_id:
                        show_info = planet_info

            # finaly render the on-hover info-box so it's not over-drawed by a planet otbit schemes
            if show_info:
                self.draw_planet_info(show_info)
# ------------------------------------------------------------------------------
    def animate(self):
        """Redraws the draggable panel"""
        if self.hover_changed() or self.__check_panel_moved():
            self.redraw_noflip()
# ------------------------------------------------------------------------------
    def on_mousedrag(self, drag_item, (mouse_x, mouse_y), (rel_x, rel_y)):
        """Updates the panel position and sets the moved flag"""
        self.i_panel_x += rel_x
        self.i_panel_y += rel_y
        self.b_panel_moved = True
# ------------------------------------------------------------------------------
    def on_mousedrop(self, drag_item, (mouse_x, mouse_y)):
        """Just reset the panel position so next time drag will not be affected by out-of border position"""
        self.i_panel_x, self.i_panel_y = self.get_normalized_panel_pos((self.i_panel_x, self.i_panel_y))
# ------------------------------------------------------------------------------
Screen = Gui_StarsystemScreen()
