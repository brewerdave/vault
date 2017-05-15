import math


def move(entity, dx, dy):
    if entity.current_map.is_walkable(entity.x_pos + dx, entity.y_pos + dy):
        entity.x_pos += dx
        entity.y_pos += dy
        return True
    return False


def move_towards(entity, target_x, target_y):
    dx = target_x - entity.x_pos
    dy = target_y - entity.y_pos
    distance = math.sqrt(dx ** 2 + dy ** 2)

    dx = int(round(dx / distance))
    dy = int(round(dy / distance))
    return move(entity, dx, dy)


def inflict_damage(actor, fighter, damage):
    if damage > 0:
        fighter.hp -= damage

        if fighter.hp <= 0:
            dfunction = fighter.death_function
            if dfunction is not None:
                dfunction(fighter.owner)


def attack(fighter, target):
    damage = fighter.power - target.fighter.defence

    if damage >= 0:
        print fighter.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.'
        inflict_damage(fighter.owner, target.fighter, damage)
    else:
        print fighter.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!'
