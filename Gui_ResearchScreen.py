import pygame
import Gui_Screen

# ==============================================================================
class Gui_ResearchScreen(Gui_Screen.Gui_Screen):
# ------------------------------------------------------------------------------
    def __init__(self):
        super(Gui_ResearchScreen,self).__init__()
# ------------------------------------------------------------------------------
    def draw(self):
        DISPLAY           = Gui_Screen.DISPLAY
        FONT4             = Gui_Screen.FONT4
        FONT5             = Gui_Screen.FONT5
        RULES             = self.get_rules()
        ME                = self.get_me()
        research_areas    = ME.research_areas
        hover             = self.get_hover()
        tech_color        = 0x047800
        tech_hover_color  = 0x28c800
        tech_active_color = 0x64d000

        self.reset_triggers_list()
        DISPLAY.blit(self.get_image('research_screen', 'panel'), (80, 0))

        for research in research_areas:
            research_index = RULES['research'][research]['index']
            first_tech_id  = research_areas[research][0]
            first_tech     = RULES['tech_table'][first_tech_id]
            i_area_id      = first_tech['area']

            if ME.i_research_area == i_area_id:
                color = tech_active_color
            else:
                color = tech_color

            x = 95 + (227 * (research_index % 2))
            y = 51 + (105 * (research_index // 2))

            s_area_name = RULES['research_areas'][i_area_id]['name']
            FONT5.write_text(DISPLAY, x, y, s_area_name, [0x0, 0x181818, color, color], 2)

            i = 0
            y += 19
            x += 10
            for tech_id in research_areas[research]:
                if (hover is not None) and (hover['action'] == "set_research") and (hover['tech_id'] == tech_id):
                    write_color = tech_hover_color
                else:
                    write_color = color

                s_tech_name = RULES['tech_table'][tech_id]['name']
                label = FONT4.render(s_tech_name, [0x0, 0x181818, write_color], 2)

                yy = i * 15
                DISPLAY.blit(label, (x, y + yy))
                self.add_trigger({'action': "set_research", 'tech_id': tech_id, 'rect': pygame.Rect((x, y + yy), label.get_size())})
                i += 1
# ------------------------------------------------------------------------------
    def process_trigger(self, trigger):
        if trigger['action'] == "set_research":
            tech_id = trigger['tech_id']
            networking.Client.set_research(tech_id)
            return self.get_escape_trigger()
# ------------------------------------------------------------------------------
Screen = Gui_ResearchScreen()
