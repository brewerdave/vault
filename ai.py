import libtcodpy
import actions


def basic_monster(monster, player):
    if libtcodpy.map_is_in_fov(monster.current_map.fov_map, monster.x, monster.y):
        if monster.distance_to(player) >= 2:
            actions.move_towards(monster, player.x_pos, player.y_pos)
        elif player.fighter.hp > 0:
            actions.attack(monster.fighter, player)


def monster_death(monster):
    print monster.name.capitalize() + ' is dead!'
    monster.symbol = '%'
    monster.symbol_color = libtcodpy.dark_red
    monster.is_walkable = True
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name

    monster.current_map.map_objects.remove(monster)
    monster.current_map.map_objects.insert(0, monster)
