import math


class Entity:
    def __init__(self, x_pos, y_pos, name, symbol, symbol_color, is_walkable=False, always_visible=False,
                 fighter=None, ai=None):
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

    def _set_owner(self, component):
        if component:
            component.set_owner(self)

    def distance_to(self, other):
        dx = other.x_pos - self.x_pos
        dy = other.y_pos - self.y_pos
        return math.sqrt(dx ** 2 + dy ** 2)



class Component:
    def set_owner(self, entity):
        self.owner = entity


class Fighter:
    def __init__(self, hp, defence, power, death_function=None):
        self.max_hp = hp
        self.hp = hp
        self.defence = defence
        self.power = power
        self.death_function = death_function

    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
            if self.hp <=0:
                d_function = self.death_function
                if d_function is not None:
                    d_function(self.owner)

    def attack(self, target):
        damage = self.power - target.fighter.defence

        if damage > 0:
            print self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.'
            target.fighter.take_damage(damage)
        else:
            print self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!'
