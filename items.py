import libtcodpy
import components
import config
import spells


def healing_potion(x, y):
    item_component = components.Item('A healing potion', use_function=spells.cast_heal)
    return components.Entity(x, y, 'healing potion', config.TILE_HEALING_POTION, libtcodpy.violet,
                             is_walkable=True, item=item_component)


def scroll_lightning(x, y):
    item_component = components.Item('A lightning scroll', use_function=spells.cast_lightning)
    return components.Entity(x, y, 'lightning scroll', config.TILE_SCROLL, libtcodpy.light_yellow, is_walkable=True,
                             item=item_component)


def scroll_fireball(x, y):
    item_component = components.Item('A fireball scroll', use_function=spells.cast_fireball)
    return components.Entity(x, y, 'fireball scroll', config.TILE_SCROLL, libtcodpy.orange, is_walkable=True,
                             item=item_component)
