import libtcodpy
import config
import log
import ui

PANEL_Y = config.SCREEN_HEIGHT - config.PANEL_HEIGHT


def renderer_init():
    global _console
    global _panel

    libtcodpy.console_set_custom_font('fonts/tileset.png', libtcodpy.FONT_TYPE_GREYSCALE |
                                      libtcodpy.FONT_LAYOUT_TCOD, 32, 10)
    libtcodpy.console_init_root(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 'vault', False)
    libtcodpy.sys_set_fps(config.LIMIT_FPS)
    _console = libtcodpy.console_new(config.MAP_WIDTH, config.MAP_HEIGHT)
    _panel = libtcodpy.console_new(config.SCREEN_WIDTH, config.PANEL_HEIGHT)
    init_custom_font()


def init_custom_font():
    index = 256

    for row in range(5,6):
        libtcodpy.console_map_ascii_codes_to_font(index, 32, 0, row)
        index += 32


def clear_console():
    libtcodpy.console_clear(_console)


def _draw_entity(entity, map, fov_map):
    if(libtcodpy.map_is_in_fov(fov_map, entity.x_pos, entity.y_pos) or
            (entity.always_visible and map.explored[entity.x_pos][entity.y_pos])):
        libtcodpy.console_set_default_foreground(_console, entity.symbol_color)
        libtcodpy.console_put_char_ex(_console, entity.x_pos, entity.y_pos, entity.symbol,
                                      libtcodpy.white, libtcodpy.black)


def clear_entity(entity):
    global _console
    libtcodpy.console_put_char(_console, entity.x_pos, entity.y_pos, ' ', libtcodpy.BKGND_NONE)


def _set(console, x, y, tile, tint_color, transparent_color):
    libtcodpy.console_put_char_ex(console, x, y, tile, tint_color, transparent_color)


def _draw_fov(current_map):
    for y in range(current_map.map_height):
        for x in range(current_map.map_width):
            visible = libtcodpy.map_is_in_fov(current_map.fov_map, x, y)
            ground = current_map.is_transparent[x][y]
            if not visible:
                if current_map.is_explored[x][y]:
                    if ground:
                        _set(_console, x, y, config.TILE_FLOOR, libtcodpy.grey, libtcodpy.black)
                    else:
                        _set(_console, x, y, config.TILE_WALL, libtcodpy.grey, libtcodpy.black)
            else:
                if ground:
                    _set(_console, x, y, config.TILE_FLOOR, libtcodpy.grey, libtcodpy.black)
                else:
                    _set(_console, x, y, config.TILE_WALL, libtcodpy.grey, libtcodpy.black)
                current_map.is_explored[x][y] = True


def _render_bar(x, y, total_width, name, value, maximum_value, bar_color, back_color):
    bar_width = int(float(value) / maximum_value * total_width)

    libtcodpy.console_set_default_background(_panel, back_color)
    libtcodpy.console_rect(_panel, x, y, total_width, 1, False, libtcodpy.BKGND_SCREEN)

    libtcodpy.console_set_default_background(_panel, bar_color)
    if bar_width > 0:
        libtcodpy.console_rect(_panel, x, y, bar_width, 1, False, libtcodpy.BKGND_SCREEN)

    libtcodpy.console_set_default_foreground(_panel, libtcodpy.white)
    libtcodpy.console_print_ex(_panel, x + total_width / 2, y, libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               name + ': ' + str(value) + '/' + str(maximum_value))


def _get_names_under_mouse(entities, fov_map, mouse):
    (x,y) = (mouse.cx, mouse.cy)
    names = [entity.name for entity in entities
             if entity.x_pos == x and entity.y_pos == y and
             libtcodpy.map_is_in_fov(fov_map, entity.x_pos, entity.y_pos)]

    names = ', '.join(names)
    return names.capitalize()


def menu(header, options, width):
    if len(options) > 26:
        raise ValueError('More than 26 menu items not currently supported')

    header_height = libtcodpy.console_get_height_rect(_console, 0, 0, width, config.SCREEN_HEIGHT, header)
    height = len(options) + header_height

    window = libtcodpy.console_new(width, height)
    libtcodpy.console_set_default_foreground(window, libtcodpy.white)
    libtcodpy.console_print_rect_ex(window, 0, 0, window, height, libtcodpy.BKGND_NONE, libtcodpy.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcodpy.console_print_ex(window, 0, y, libtcodpy.BKGND_NONE, libtcodpy.LEFT, text)
        y += 1
        letter_index += 1

    x = config.SCREEN_WIDTH/2 - width/2
    y = config.SCREEN_HEIGHT/2 - height/2
    libtcodpy.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

    libtcodpy.console_flush()
    key = libtcodpy.console_wait_for_keypress(True)

    index = key.c - ord('a')
    if 0 <= index < len(options):
        return index
    return None


def render_all(player):
    global _console, _panel

    current_map = player.current_map
    if current_map.recompute_fov:
        libtcodpy.map_compute_fov(current_map.fov_map, player.x_pos, player.y_pos, config.TORCH_RADIUS,
                                  config.FOV_LIGHT_WALLS, config.FOV_ALGORITHM)
    _draw_fov(current_map)

    for entity in current_map.map_entities:
        if entity != player:
            _draw_entity(entity, current_map, current_map.fov_map)
    _draw_entity(player, current_map, current_map.fov_map)

    libtcodpy.console_blit(_console, 0, 0, config.MAP_WIDTH, config.MAP_HEIGHT, 0, 0, 0)

    # Handle bottom panel
    libtcodpy.console_set_default_background(_panel, libtcodpy.black)
    libtcodpy.console_clear(_panel)

    # Message Log
    y = 1
    for(line, color) in log.game_messages:
        libtcodpy.console_set_default_foreground(_panel, color)
        libtcodpy.console_print_ex(_panel, config.MSG_X, y, libtcodpy.BKGND_NONE, libtcodpy.LEFT, line)
        y += 1

    # Health Bar
    _render_bar(1, 1, config.BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcodpy.light_red,
                libtcodpy.darker_red)

    # Items under mouse
    libtcodpy.console_set_default_foreground(_panel, libtcodpy.light_grey)
    libtcodpy.console_print_ex(_panel, 1, 0, libtcodpy.BKGND_NONE, libtcodpy.LEFT,
                               _get_names_under_mouse(current_map.map_entities, current_map.fov_map, ui.mouse))

    libtcodpy.console_blit(_panel, 0, 0, config.SCREEN_WIDTH, config.PANEL_HEIGHT, 0, 0, PANEL_Y)
