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