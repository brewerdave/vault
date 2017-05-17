import math
import log
import libtcodpy

def move(entity, dx, dy):
    if entity.current_map.is_tile_walkable(entity.x_pos + dx, entity.y_pos + dy):
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
            log.add_message(actor.name.capitalize() + ' kills ' + fighter.owner.name.capitalize() + '!')
            dfunction = fighter.death_function
            if dfunction is not None:
                dfunction(fighter.owner)


def attack(fighter, target):
    damage = fighter.power - target.fighter.defence

    if damage >= 0:
        log.add_message(
            fighter.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.'
        )
        inflict_damage(fighter.owner, target.fighter, damage)
    else:
        log.add_message(
            fighter.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!'
        )


def pick_up_item(player, item):
    if len(player.inventory) >= player.inventory_size:
        log.add_message("Inventory is full!", libtcodpy.light_red)
    else:
        player.inventory.append(item)
        player.current_map.map_entities.remove(item)
        log.add_message("Picked up " + item.name, libtcodpy.light_green)


def use(player, entity):
    if entity.item.use_function is None:
        log.add_message(entity.name + ' cannot be used.')
    elif entity.item.use_function(player) != 'cancelled':
        if entity.item.count > 1:
            entity.item.count -= 1
        else:
            player.inventory.remove(entity)


def heal(fighter, amount):
    fighter.hp += amount

    if fighter.hp > fighter.max_hp:
        fighter.hp = fighter.max_hp
