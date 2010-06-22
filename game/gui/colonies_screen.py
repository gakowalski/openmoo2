import pygame
from screen import Screen

class ColoniesScreen(Screen):

    def __init__(self, ui):
        Screen.__init__(self, ui)

        self.__view_size = 10

        self.__list_start = 0
        self.__list_size  = 0

    def reset_triggers_list(self):
        Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE",        'rect': pygame.Rect((534, 448), (77, 19))})
        self.add_trigger({'action': "SCROLL_UP",      'rect': pygame.Rect((620, 16), (8, 18))})
        self.add_trigger({'action': "SCROLL_DOWN",    'rect': pygame.Rect((620, 318), (8, 18))})

    def draw(self):
        GAME = self.__GAME
        PLAYERS     = GAME['DATA']['players']
        COLONIES    = GAME['DATA']['colonies']
        ME          = GAME['DATA']['me']

        DISPLAY = self.get_display()

        DISPLAY.blit(self.get_image('colonies_screen', 'panel'), (0, 0))

        my_colonies = []

        for colony_id, col in COLONIES.items():
            if (col.get_owner() == ME.get_id()) and (not col.is_outpost()):
                my_colonies.append("%s:%i" % (COLONIES[colony_id].get_name(), colony_id))

        print(my_colonies)

        my_colonies.sort()
        for i in range(len(my_colonies)):
            colony_id = int(my_colonies[i].split(":")[1])
            my_colonies[i] = COLONIES[colony_id]

        self.__list_size = len(my_colonies)

        font3 = self.get_font('font3')

        for i in range(self.__list_start, min(self.__list_size, self.__list_start + self.__view_size)):
            colony = my_colonies[i]
            colony_id	= colony.get_id()
            planet_id	= colony.get_planet_id()

            if planet_id == 0xffff:
                print colony
                continue

            y = 38 + (31 * (i - self.__list_start))

            self.add_trigger({'action': "colony", 'colony_id': colony_id, 'rect': pygame.Rect((12, y), (85, 24))})
            self.add_trigger({'action': "colony_build", 'colony_id': colony_id, 'rect': pygame.Rect((513, y), (85, 24))})

#            DISPLAY.blit(FONTS['font_10'].render(colony.get_name(), 1, (0x80, 0xA0, 0xBC)), (12, y + 6))
            font3.write_text(DISPLAY, 12, y + 5, colony.get_name(), [0x0, 0x141420, 0x6c688c], 2)

            for t in (0x02, 0x82, 0x03):
                if t == 0x02:
                    x = 101
                    icon = 1
                elif t == 0x82:
                    x = 236
                    icon = 3
                elif t == 0x03:
                    x = 378
                    icon = 5

                c = len(colony.colonists[t])
                if c < 5:
                    xx = 28
                else:
                    xx = 114 / c

                for ii in range(c):
                    colonist = colony.colonists[t][ii]
                    race = colonist['race']
                    picture = PLAYERS[race].get_picture()
#                    DISPLAY.blit(self.get_ui().get_race_icon(picture, icon), (x + (xx * ii), y))
                    DISPLAY.blit(self.get_image('race_icon', picture, icon), (x + (xx * ii), y))

        self.flip()

    def run(self, GAME):
        self.__GAME = GAME
        self.draw()

        while True:
            event = self.get_event()
            if event:
                action = event['action']

                if action == "ESCAPE":
                    return

                elif action == "hover":
                    pass

                elif action == "SCROLL_UP":
                    if self.__list_start > 0:
                        self.__list_start -= 1
                        self.draw()

                elif action == "SCROLL_DOWN":
                    if self.__list_start < (self.__list_size - self.__view_size):
                        self.__list_start += 1
                        self.draw()

                elif action == "colony":
                    self.get_screen('COLONY').run(GAME, event['colony_id'])
                    self.draw()

                elif action == "colony_build":
                    self.get_screen('COLONY_BUILD').run(GAME, event['colony_id'])
                    self.draw()

                else:
                    self.log_info("gui_main_screen::run() ... UNKNONW event: %s" % event)
