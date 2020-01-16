import tcod
import tcod.event


def main():
    # ######################################################################
    # Global Game Settings
    # ######################################################################

    # Windows Controls
    FULLSCREEN = False
    SCREEN_WIDTH = 80  # characters wide
    SCREEN_HEIGHT = 50  # characters tall
    LIMIT_FPS = 20  # 20 frames-per-second maximum

    # Game Controls
    TURN_BASED = True  # turn-based game
    REAL_TIME = not TURN_BASED  # realtime game

    # Map Parameters
    MAP_WIDTH = 80
    MAP_HEIGHT = 45

    colour_dark_wall = tcod.Color(0, 0, 100)
    colour_dark_ground = tcod.Color(50, 50, 150)

    #############################################
    # Class Declarations
    #############################################

    class Object:
        # this is a generic object: the player, a monster, an item, the stairs...
        # it's always represented by a character on screen.
        def __init__(self, x, y, char, colour):
            self.x = x
            self.y = y
            self.char = char
            self.colour = colour

        def move(self, dx, dy):
            # move by the given amount, if the destination is not blocked
            if not map[self.x + dx][self.y + dy].blocked:
                self.x += dx
                self.y += dy

        def draw(self):
            # set the colour and then draw the character that represents this object at its position
            tcod.console_set_default_foreground(con, self.colour)
            tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

        def clear(self):
            # erase the character that represents this object
            tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)

    class Tile:
        # a tile of the map and its properties
        def __init__(self, blocked, block_sight=None):
            self.blocked = blocked

            # by default, if a tile is blocked, it also blocks sight
            if block_sight is None: block_sight = blocked
            self.block_sight = block_sight

        #######################################################################
        # Function Definitions
        #######################################################################

        def get_key_event(turn_based=None):
            if turn_based:
                # Turn-based game play; wait for a key stroke
                key = tcod.console_wait_for_keypress(True)
            else:
                # Real-time game play; don't wait for a player's key stroke
                key = tcod.console_check_for_keypress()
            return key

        def handle_keys():
            global player_x, player_y

            key = get_key_event(TURN_BASED)

            if key.vk == tcod.KEY_ENTER and key.lalt:
                # Alt+Enter: toggle fullscreen
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

            elif key.vk == tcod.KEY_ESCAPE:
                return True  # exit game

            # movement keys
            if tcod.console_is_key_pressed(tcod.KEY_UP):
                player.move(0, -1)

            elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
                player.move(0, 1)

            elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
                player.move(-1, 0)

            elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
                player.move(1, 0)

        # Map generator
        def make_map():
            # fill map with "unblocked" tiles
            global map
            map = [
                [Tile(False) for y in range(MAP_HEIGHT)]
                for x in range(MAP_WIDTH)
            ]

            # Place two pillars to test the map
            map[30][22].blocked = True
            map[30][22].block_sight = True
            map[50][22].blocked = True
            map[50][22].block_sight = True

        # Render funtion
        def render_all():
            # draw all objects in the list
            for object in objects:
                object.draw()

            for y in range(MAP_HEIGHT):
                for x in range(MAP_WIDTH):
                    wall = map[x][y].block_sight
                    if wall:
                        tcod.console_set_char_background(con, x, y, colour_dark_wall, tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colour_dark_ground, tcod.BKGND_SET)

            tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    #############################################
    # Main Game Loop and initialisation
    #############################################

    # Setup Font
    font_filename = 'data\\fonts\\arial12x12.png'
    tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Initialize screen
    title = 'Python 3 + Libtcod tutorial'
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN, tcod.RENDERER_SDL2, vsync=True)
    con = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    tcod.sys_set_fps(LIMIT_FPS)
    tcod.console_set_default_foreground(con, tcod.white)

    # Setup player and NPC
    player = Object(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, '@', tcod.white)
    npc = Object(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2, '@', tcod.yellow)
    objects = [npc, player]

    # Create map
    make_map()

    while True:
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()

            else:
                # Render the screens
                render_all()

                tcod.console_flush()

                for object in objects:
                    object.clear()

                # Handle keys and exit game if needed
                if event.type == "KEYDOWN":
                    if event.sym == libtcod.event.K_ESCAPE:
                        raise SystemExit()

if __name__ == '__main__':
    main()