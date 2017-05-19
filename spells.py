import libtcodpy
import log
import actions
import config
import ui
import renderer


def cast_heal(player, amount=config.HEALING_POTION_AMOUNT):
    if player.fighter.hp == player.fighter.max_hp:
        log.add_message('Already at full health')
        return 'cancelled'

    log.add_message('You feel much better!')
    actions.heal(player.fighter, amount)


def cast_lightning(player):
    monster = _closest_monster(player, config.LIGHTNING_RANGE)
    if monster is None:
        log.add_message('No enemy in range', config.COLOR_ERROR_MESSAGE)
        return 'cancelled'

    log.add_message('Lightning strikes ' + monster.name + ' for ' + str(config.LIGHTNING_DAMAGE) + ' damage',
                    config.COLOR_MAGIC_MESSAGE)
    actions.inflict_damage(player, monster.fighter, config.LIGHTNING_DAMAGE)


def cast_fireball(player):
    log.add_message('Left-click to target or right-click to cancel', config.COLOR_INFO_MESSAGE)
    (x, y) = _target_tile(player)
    if x is None:
        log.add_message('Spell cancelled', config.COLOR_ERROR_MESSAGE)
        return 'cancelled'
    log.add_message('Your fireball explodes')

    for entity in player.current_map.map_entities:
        if entity.distance(x, y) <= config.FIREBALL_RADIUS and entity.fighter:
            log.add_message(entity.name + ' takes ' + str(config.FIREBALL_DAMAGE) + ' damage',
                            config.COLOR_DAMAGE_MESSAGE)
            entity.fighter.take_damage(config.FIREBALL_DAMAGE)


def _closest_monster(player, max_range):
    # Closest monster in FOV
    closest_enemy = None
    closest_distance = max_range + 1

    for entity in player.current_map.map_entities:
        if(entity.fighter and not entity == player and
               libtcodpy.map_is_in_fov(player.current_map.fov_map, entity.x_pos, entity.y_pos)):
            distance = player.distance_to(entity)
            if distance < closest_distance:
                closest_enemy = entity
                closest_distance = distance
    return closest_enemy


def _target_tile(player, max_range=None):
    while True:
        libtcodpy.console_flush()
        libtcodpy.sys_check_for_event(libtcodpy.EVENT_KEY_PRESS|libtcodpy.EVENT_MOUSE, ui.key, ui.mouse)
        renderer.render_all(player)

        (x, y) = (ui.mouse.cx, ui.mouse.cy)

        if (ui.mouse.lbutton_pressed and libtcodpy.map_is_in_fov(player.current_map.fov_map, x, y) and
           (max_range is None or player.distance(x, y) <= max_range)):
            return x, y

        if ui.mouse.rbutton_pressed or ui.key.vk == libtcodpy.KEY_ESCAPE:
            return None, None
