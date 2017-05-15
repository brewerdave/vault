import libtcodpy
import math
import dungeonmap
import config

libtcodpy.console_set_custom_font('fonts/arial10x10.png', libtcodpy.FONT_TYPE_GREYSCALE | libtcodpy.FONT_LAYOUT_TCOD)
libtcodpy.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'vault', False)
console = libtcodpy.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)







def player_move_or_attack(dx, dy):
    global fov_recompute

    x = player.x_pos + dx
    y = player.y_pos + dy

    target = None
    for game_object in game_objects:
        if game_object.fighter and game_object.x_pos == x and game_object.y_pos == y:
            target = game_object
            break

    if target is not None:
        player.fighter.attack(target)
    else:
        player.move(dx, dy)
        fov_recompute = True


def player_death(player):
    global game_state
    print 'You died!'
    game_state = 'dead'

    player.symbol = '%'
    player.symbol_color = libtcodpy.dark_red






def render_all():
    global fov_recompute

    for game_object in game_objects:
        if game_object != player:
            game_object.draw()
    player.draw()

    if fov_recompute:
        fov_recompute = False
        libtcodpy.map_compute_fov(fov_map, player.x_pos, player.y_pos, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            visible = libtcodpy.map_is_in_fov(fov_map, x, y)
            ground = game_map[x][y].is_transparent
            if not visible:
                if game_map[x][y].is_explored:
                    if ground:
                        libtcodpy.console_set_char_background(console, x, y, color_dark_ground, libtcodpy.BKGND_SET)
                    else:
                        libtcodpy.console_set_char_background(console, x, y, color_dark_wall, libtcodpy.BKGND_SET)
            else:
                if ground:
                    libtcodpy.console_set_char_background(console, x, y, color_light_ground, libtcodpy.BKGND_SET)
                else:
                    libtcodpy.console_set_char_background(console, x, y, color_light_wall, libtcodpy.BKGND_SET)
                game_map[x][y].is_explored = True

    libtcodpy.console_blit(console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcodpy.console_set_default_foreground(console, libtcodpy.white)
    libtcodpy.console_print_ex(console, 1, SCREEN_HEIGHT - 2, libtcodpy.BKGND_NONE, libtcodpy.LEFT,
                               'HP: ' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp))


def clear_all():
    for game_object in game_objects:
        game_object.clear()


def handle_keys():
    key = libtcodpy.console_wait_for_keypress(True)
    if key.vk == libtcodpy.KEY_ENTER and key.lalt:
        libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

    elif key.vk == libtcodpy.KEY_ESCAPE:
        return 'exit'

    if game_state == 'playing':

        if libtcodpy.console_is_key_pressed(libtcodpy.KEY_UP) or chr(key.c) == 'k':
            player_move_or_attack(0, -1)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_DOWN) or chr(key.c) == 'j':
            player_move_or_attack(0, 1)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_LEFT) or chr(key.c) == 'h':
            player_move_or_attack(-1, 0)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_RIGHT) or chr(key.c) == 'l':
            player_move_or_attack(1, 0)

        elif chr(key.c) == 'u':
            player_move_or_attack(1, -1)

        elif chr(key.c) == 'y':
            player_move_or_attack(-1, -1)

        elif chr(key.c) == 'n':
            player_move_or_attack(1, 1)

        elif chr(key.c) == 'b':
            player_move_or_attack(-1, 1)

        else:
            return 'didnt-take-turn'




game_state = 'playing'
player_action = None


def new_game():
    fighter_component = Fighter(hp=30, defence=2, power=5, death_function=player_death)
    player = GameObject(0, 0, 'player', '@', libtcodpy.white, is_walkable=False, fighter=fighter_component)
    current_map = dungeonmap.DungeonMap(MAP_WIDTH, MAP_HEIGHT)

while not libtcodpy.console_is_window_closed():
    render_all()
    libtcodpy.console_flush()
    clear_all()

    player_action = handle_keys()
    if game_state == 'playing' and player_action != 'didnt-take-turn':
        for game_object in game_objects:
            if game_object.ai:
                game_object.ai.take_turn()

    if player_action == 'exit':
        break
