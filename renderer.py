import libtcodpy
import config
import log

PANEL_Y = config.SCREEN_HEIGHT - config.PANEL_HEIGHT


def renderer_init():
    global _console
    global _panel
    libtcodpy.console_set_custom_font('fonts/arial12x12.png', libtcodpy.FONT_TYPE_GREYSCALE |
                                      libtcodpy.FONT_LAYOUT_TCOD)
    libtcodpy.console_init_root(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 'vault', False)
    libtcodpy.sys_set_fps(config.LIMIT_FPS)
    _console = libtcodpy.console_new(config.MAP_WIDTH, config.MAP_HEIGHT)
    _panel = libtcodpy.console_new(config.SCREEN_WIDTH, config.PANEL_HEIGHT)


def clear_console():
    libtcodpy.console_clear(_console)


def _draw_entity(entity, map, fov_map):
    if(libtcodpy.map_is_in_fov(fov_map, entity.x_pos, entity.y_pos) or
            (entity.always_visible and map.explored[entity.x_pos][entity.y_pos])):
        libtcodpy.console_set_default_foreground(_console, entity.symbol_color)
        libtcodpy.console_put_char(_console, entity.x_pos, entity.y_pos, entity.symbol,
                                   libtcodpy.BKGND_NONE)


def clear_entity(entity):
    global _console
    libtcodpy.console_put_char(_console, entity.x_pos, entity.y_pos, ' ', libtcodpy.BKGND_NONE)


def _set(console, x, y, color, mode):
    libtcodpy.console_set_char_background(console, x, y, color, mode)


def _draw_fov(current_map):
    for y in range(current_map.map_height):
        for x in range(current_map.map_width):
            visible = libtcodpy.map_is_in_fov(current_map.fov_map, x, y)
            ground = current_map.is_transparent[x][y]
            if not visible:
                if current_map.is_explored[x][y]:
                    if ground:
                        _set(_console, x, y, config.COLOR_DARK_GROUND, libtcodpy.BKGND_SET)
                    else:
                        _set(_console, x, y, config.COLOR_DARK_WALL, libtcodpy.BKGND_SET)
            else:
                if ground:
                    _set(_console, x, y, config.COLOR_LIGHT_GROUND, libtcodpy.BKGND_SET)
                else:
                    _set(_console, x, y, config.COLOR_LIGHT_WALL, libtcodpy.BKGND_SET)
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

    y = 1
    for(line, color) in log.game_messages:
        libtcodpy.console_set_default_foreground(_panel, color)
        libtcodpy.console_print_ex(_panel, config.MSG_X, y, libtcodpy.BKGND_NONE, libtcodpy.LEFT, line)
        y += 1

    _render_bar(1, 1, config.BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcodpy.light_red,
                libtcodpy.darker_red)

    libtcodpy.console_blit(_panel, 0, 0, config.SCREEN_WIDTH, config.PANEL_HEIGHT, 0, 0, PANEL_Y)
