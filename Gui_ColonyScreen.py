import pygame
import Gui_Client
import Gui_Screen
import Network_Client

POPULATION_PALETTE   = [0x0, 0x141420, 0x6c688c]
TITLE_PALETTE        = [0x0, 0x141420, 0x6c688c, 0x605c80]
SCHEMES_FONT_PALETTE = [0x0, 0x141420, 0x6c688c]

# ==============================================================================
class Gui_ColonyScreen(Gui_Screen.Gui_Screen):

    def __init__(self):
        Gui_Screen.Gui_Screen.__init__(self)
        self.i_colony_id = -1
        self.o_colony    = None
        self.i_planet_id = -1
        self.o_planet    = None
        self.i_star_id   = -1
        self.o_star      = None
# ------------------------------------------------------------------------------
    def open_colony(self, i_colony_id):
        self.i_colony_id = i_colony_id
        self.o_colony    = self.get_colony(self.i_colony_id)
        self.i_planet_id = self.o_colony.i_planet_id
        self.o_planet    = self.get_planet(self.i_planet_id)
        self.i_star_id   = self.o_planet.i_star_id
        self.o_star      = self.get_star(self.i_star_id)
# ------------------------------------------------------------------------------
    def reset_triggers_list(self):
        Gui_Screen.Gui_Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE",                         'rect': pygame.Rect((556, 459), ( 72, 20))})
        self.add_trigger({'action': "leaders",                        'rect': pygame.Rect((556, 427), ( 72, 20))})
        self.add_trigger({'action': "buy",                            'rect': pygame.Rect((590, 123), ( 37, 22))})
        self.add_trigger({'action': "summary", 'summary': "morale",   'rect': pygame.Rect((309,  31), (202, 25))})
        self.add_trigger({'action': "summary", 'summary': "bc",       'rect': pygame.Rect((127,  31), (177, 25))})
        self.add_trigger({'action': "summary", 'summary': "food",     'rect': pygame.Rect((127,  61), (177, 25))})
        self.add_trigger({'action': "summary", 'summary': "industry", 'rect': pygame.Rect((127,  91), (177, 25))})
        self.add_trigger({'action': "summary", 'summary': "research", 'rect': pygame.Rect((127, 121), (177, 25))})
# ------------------------------------------------------------------------------
    def draw(self):
        PLAYERS    = self.list_players()
        PLANETS    = self.list_planets()
        star       = self.o_star
        planet     = self.o_planet
        colony     = self.o_colony
        colony_id  = colony.i_id

        self.blit(self.get_image('background', 'starfield'), (0, 0))
        self.blit(self.get_planet_background(planet.get_terrain(), planet.get_picture()), (0, 0))
        self.blit(self.get_image('colony_screen', 'panel'), (0, 0))

        self.reset_triggers_list()
        self.add_trigger({'action': "screen", 'screen': "colony_production", 'colony_id': colony_id, 'rect': pygame.Rect((519, 123), ( 61, 22))})

        for i in range(K_MAX_STAR_OBJECTS):
            object_id = star.v_object_ids[i]
            if object_id != 0xFFFF:
                object = PLANETS[object_id]
                print "type: %i" % object.get_type()

                if object.is_asteroid_belt():
                    x = 6
                    y = 22 + (24 * i)
                    self.blit(self.get_image('colony_screen', 'asteroids_scheme'), (x, y))
                    self.write_text(K_FONT2, SCHEMES_FONT_PALETTE, x + 29, y + 9, "Asteroids")

                if object.is_gas_giant():
                    x = 11
                    y = 27 + (24 * i)
                    self.blit(self.get_image('colony_screen', 'gasgiant_scheme'), (x, y))
                    write_text(K_FONT2, SCHEMES_FONT_PALETTE, x + 24, y + 4,  "Gas Giant -")
                    write_text(K_FONT2, SCHEMES_FONT_PALETTE, x + 24, y + 15, "uninhabitable")

                elif object.is_planet():
                    terrain = object.get_terrain()
                    size = object.get_size()
                    x = 10 + [6, 4, 3, 1, 0][size]
                    y = 26 + (24 * i) + [6, 4, 2, 1, 0][size]
                    self.blit(self.get_image('planet_scheme', terrain, size), (x, y))

            self.blit(self.get_image('colony_screen', 'scheme_arrow'), (6,  31 + (24 * i)))

        title_text    = "%s of %s" % (DICTIONARY['COLONY_ASSIGNMENT'][colony.assignment], colony.s_name)
        title_surface = self.render(K_FONT5, TITLE_PALETTE, title_text, 2)
        (tw, th)      = title_surface.get_size()

        self.blit(title_surface, (320 - (tw / 2), 1))

    #    total_population = (1000 * colony['population']) + colony['pop_raised']
    #    print
    #    print "    Colony:     %s" % colony.name
    #    print "    Population: %i (+%i)" % (total_population, colony['pop_grow'])
    #    print "    Industry:   %i" % colony.industry()
    #    print "    Research:   %i" % colony.research()
    #    print "    Food (result):%i (%i)" % (colony.food(), colony.food() - colony.population)
    #    print "    Colonists:"

        player_government_id = PLAYERS[colony.i_owner_id].get_racepick_item('goverment')

        self.blit(self.get_image('government', 'icon', player_government_id), (310, 32))

        # TODO: implement negative morale
        self.repeat_draw(340, 35, self.get_image('morale_icon', 'good'), colony.i_morale // 10, 30, 7, 155)

        x = 10 + self.repeat_draw(128, 64, self.get_image('production_10food'), colony.i_food // 10, 20, 6, 98)
        self.repeat_draw(x, 64, self.get_image('production_1food'), colony.i_food % 10, 20, 6, 98)

        # industry icons
        number = (colony.i_industry // 10) + (colony.i_industry % 10)
        xx = min(int(round(160 / max(1, number))), 20)
        #print "### colony_screen::draw ... industry icons ... number = %i, xx = %i" % (number, xx)
        x = self.repeat_draw(128, 94, self.get_image('production_10industry'), colony.i_industry // 10, xx, 99, 162)
        self.repeat_draw(x, 94, self.get_image('production_1industry'), colony.i_industry % 10, xx, 99, 162)

        # research icons

        number = (colony.i_research // 10) + (colony.i_research % 10)
        xx = min(int(round(160 / max(1, number))), 20)
        #print "### colony_screen::draw ... research icons ... number = %i, xx = %i" % (number, xx)
        x = self.repeat_draw(128, 124,self.get_image('production_10research'), colony.i_research // 10, xx, 99, 162)
        self.repeat_draw(x, 124, self.get_image('production_1research'), colony.i_research % 10, xx, 99, 162)

        for t in (FARMER, WORKER, SCIENTIST):
            c = len(colony.colonists[t])
            if c < 7:
                xx = 30
            else:
                xx = 190 / c

            if t == 0x02:
                icon = 1
                y = 62
            elif t == 0x82:
                icon = 3
                y = 92
            elif t == 0x03:
                icon = 5
                y = 122

            for i in range(c):
                colonist = colony.colonists[t][i]
                race     = colonist['race']
                picture  = PLAYERS[race].i_picture
                x = 310 + xx * i
                self.blit(self.get_image('race_icon', picture, icon), (x, y))
                if i == (c - 1):
                    xx = 28 # enlarge the Rect of last icon (no other icon is drawn over it...)
                self.add_trigger({'action': "pick-colonist:%.2x:%i" % (t, (c - i)), 'rect': pygame.Rect((x, y), (xx, 28))})

        x = 0
        for i in range(colony.marines):
            self.blit(self.get_image('race_icon', picture, 0x07), (x, 450))
            x += 30

        # TODO: count in all races not just owner!
        total_population   = (1000 * colony.total_population()) + sum(colony.pop_raised())
        pop_text           = "Pop %i,%.3i k (+%i)" % ((total_population // 1000), (total_population % 1000), sum(colony.pop_grow()))
        population         = self.render(K_FONT3, POPULATION_PALETTE, pop_text, 2)
        (tw, th)           = population.get_size()

        self.blit(population, (529, 3))
# ------------------------------------------------------------------------------
    def process_trigger(self, o_trigger):

        i_colony_id = self.i_colony_id
        o_colony    = self.get_colony(i_colony_id)
        i_planet_id = colony.i_planet_id
        o_planet    = self.get_planet(i_planet_id)
        i_star_id   = planet.i_star_id
        o_star      = self.get_star(i_star_id)

        if o_trigger['action'] == "summary":
            s_summary = o_trigger['summary']

            if s_summary == "morale":
                text_box.Screen.set_title("Morale Summary")
                text_box.Screen.set_content(colony.print_morale_summary())

            elif s_summary == "bc":
                text_box.Screen.set_title("BC Summary")
                text_box.Screen.set_content(colony.print_bc_summary())

            elif s_summary == "food":
                text_box.Screen.set_title("Food Summary")
                text_box.Screen.set_content(colony.print_food_summary())

            elif s_summary == "industry":
                text_box.Screen.set_title("Industry Summary")
                text_box.Screen.set_content(colony.print_industry_summary())

            elif s_summary == "research":
                text_box.Screen.set_title("Research Summary")
                text_box.Screen.set_content(colony.print_research_summary())

            Gui_Client.GUI.run_screen(text_box.Screen)
            self.redraw_flip()
# ------------------------------------------------------------------------------
Screen = Gui_ColonyScreen()
