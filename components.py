import math
import log


class Entity:
    def __init__(self, x_pos, y_pos, name, symbol, symbol_color, is_walkable=False, always_visible=False,
                 fighter=None, ai=None, item=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.name = name
        self.symbol = symbol
        self.symbol_color = symbol_color
        self.is_walkable = is_walkable
        self.always_visible = always_visible

        self.fighter = fighter
        self._set_owner(fighter)
        self.ai = ai
        self._set_owner(ai)
        self.item = item
        self._set_owner(item)

    def _set_owner(self, component):
        if component:
            component.set_owner(self)

    def distance_to(self, other):
        dx = other.x_pos - self.x_pos
        dy = other.y_pos - self.y_pos
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        return math.sqrt((x - self.x_pos) ** 2 + (y - self.y_pos) ** 2)


class Component:
    def set_owner(self, entity):
        self.owner = entity


class Item(Component):
    def __init__(self, description, count=1, use_function=None):
        self.use_function = use_function
        self.description = description
        self.count = count


class Fighter(Component):
    def __init__(self, hp, defence, power, death_function=None):
        self.max_hp = hp
        self.hp = hp
        self.defence = defence
        self.power = power
        self.death_function = death_function

    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                d_function = self.death_function
                if d_function is not None:
                    d_function(self.owner)

    def attack(self, target):
        damage = self.power - target.fighter.defence

        if damage > 0:
            target.fighter.take_damage(damage)
        else:
            log.add_message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')


class AI(Component):
    def __init__(self, take_turn):
        self.turn_function = take_turn

    def take_turn(self, player):
        self.turn_function(self.owner, player)