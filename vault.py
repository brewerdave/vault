import libtcodpy
import actions
import components
import mapmaker
import renderer


def player_move_or_attack(player, dx, dy):
    x = player.x_pos + dx
    y = player.y_pos + dy

    target = None
    for entity in player.current_map.map_entities:
        if entity.fighter and entity.x_pos == x and entity.y_pos == y:
            target = entity
            break

    if target is not None:
        actions.attack(player.fighter, target)
    else:
        if actions.move(player, dx, dy):
            player.current_map.fov_needs_recompute = True


def player_death(player):
    print 'You died!'
    player.game_state = 'dead'

    player.symbol = '%'
    player.symbol_color = libtcodpy.dark_red


def handle_keys(player):
    key = libtcodpy.console_wait_for_keypress(True)
    if key.vk == libtcodpy.KEY_ENTER and key.lalt:
        libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

    elif key.vk == libtcodpy.KEY_ESCAPE:
        return 'exit'

    if player.game_state == 'playing':

        if libtcodpy.console_is_key_pressed(libtcodpy.KEY_UP) or chr(key.c) == 'k':
            player_move_or_attack(player, 0, -1)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_DOWN) or chr(key.c) == 'j':
            player_move_or_attack(player, 0, 1)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_LEFT) or chr(key.c) == 'h':
            player_move_or_attack(player, -1, 0)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_RIGHT) or chr(key.c) == 'l':
            player_move_or_attack(player, 1, 0)

        elif chr(key.c) == 'u':
            player_move_or_attack(player, 1, -1)

        elif chr(key.c) == 'y':
            player_move_or_attack(player, -1, -1)

        elif chr(key.c) == 'n':
            player_move_or_attack(player, 1, 1)

        elif chr(key.c) == 'b':
            player_move_or_attack(player, -1, 1)

        else:
            return 'didnt-take-turn'


def new_game():
    fighter_component = components.Fighter(hp=30, defence=2, power=5, death_function=player_death)
    player = components.Entity(0, 0, 'player', '@', libtcodpy.white, is_walkable=False, fighter=fighter_component)
    player.game_state = 'playing'

    player.current_map = mapmaker.make_map(player)
    renderer.clear_console()

    return player


def play_game(player):
    while not libtcodpy.console_is_window_closed():
        renderer.render_all(player)
        player.current_map.fov_needs_recompute = False

        libtcodpy.console_flush()

        for entity in player.current_map.map_entities:
            renderer.clear_entity(entity)

        player_action = handle_keys(player)
        if player_action == 'exit':
            break

        if player.game_state == 'playing' and player_action != 'didnt-take-turn':
            for entity in player.current_map.map_entities:
                if entity.ai:
                    entity.ai.take_turn(player)

renderer.renderer_init()
play_game(new_game())


