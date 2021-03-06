import libtcodpy
import actions
import components
import mapmaker
import renderer
import log
import ui
import config


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
    log.add_message('You died!')
    player.game_state = 'dead'

    player.symbol = '%'
    player.symbol_color = libtcodpy.dark_red


def inventory_menu(player, header):
    if len(player.inventory) == 0:
        renderer.menu(header, 'Inventory is empty.', config.INVENTORY_WIDTH)
        return None
    else:
        options = [item.name for item in player.inventory]

    index = renderer.menu(header, options, config.INVENTORY_WIDTH)
    return player.inventory[index].item


def handle_input(player):
    ui.poll()

    if ui.key.vk == libtcodpy.KEY_ENTER and ui.key.lalt:
        libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

    elif ui.key.vk == libtcodpy.KEY_ESCAPE:
        return 'exit'

    if player.game_state == 'playing':

        if ui.key.vk == libtcodpy.KEY_UP or chr(ui.key.c) == 'k':
            player_move_or_attack(player, 0, -1)

        elif ui.key.vk == libtcodpy.KEY_DOWN or chr(ui.key.c) == 'j':
            player_move_or_attack(player, 0, 1)

        elif ui.key.vk == libtcodpy.KEY_LEFT or chr(ui.key.c) == 'h':
            player_move_or_attack(player, -1, 0)

        elif ui.key.vk == libtcodpy.KEY_RIGHT or chr(ui.key.c) == 'l':
            player_move_or_attack(player, 1, 0)

        elif chr(ui.key.c) == 'u':
            player_move_or_attack(player, 1, -1)

        elif chr(ui.key.c) == 'y':
            player_move_or_attack(player, -1, -1)

        elif chr(ui.key.c) == 'n':
            player_move_or_attack(player, 1, 1)

        elif chr(ui.key.c) == 'b':
            player_move_or_attack(player, -1, 1)

        else:
            if chr(ui.key.c) == 'g':
                for entity in player.current_map.map_entities:
                    if entity.x_pos == player.x_pos and entity.y_pos == player.y_pos and entity.item:
                        actions.pick_up_item(player, entity)
                        break

            if chr(ui.key.c) == 'i':
                chosen_item = inventory_menu(player, 'Inventory')
                if chosen_item is not None:
                    actions.use(player, chosen_item.owner)

            return 'didnt-take-turn'


def new_game():
    fighter_component = components.Fighter(hp=30, defence=2, power=5, death_function=player_death)
    player = components.Entity(0, 0, 'player', config.TILE_PLAYER, libtcodpy.white, is_walkable=False,
                               fighter=fighter_component)
    player.inventory = []
    player.inventory_size = 26
    player.game_state = 'playing'
    log.init()
    log.add_message("You awaken in a vault.")
    player.current_map = mapmaker.make_map(player)
    renderer.clear_console()

    return player


def play_game(player):
    ui.init()

    while not libtcodpy.console_is_window_closed():
        renderer.render_all(player)
        player.current_map.fov_needs_recompute = False

        libtcodpy.console_flush()

        for entity in player.current_map.map_entities:
            renderer.clear_entity(entity)

        player_action = handle_input(player)
        if player_action == 'exit':
            break

        if player.game_state == 'playing' and player_action != 'didnt-take-turn':
            for entity in player.current_map.map_entities:
                if entity.ai:
                    entity.ai.take_turn(player)

renderer.renderer_init()
play_game(new_game())


