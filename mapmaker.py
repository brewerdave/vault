import libtcodpy
import dungeonmap
import config
import components
import ai

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return center_x, center_y

    def intersects(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


def make_map(player):
    new_map = dungeonmap.DungeonMap(config.MAP_WIDTH, config.MAP_HEIGHT)
    new_map.map_entities.append(player)
    player.current_map = new_map

    rooms = []
    rooms_amount = 0

    for room in range(MAX_ROOMS):
        width = libtcodpy.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        height = libtcodpy.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = libtcodpy.random_get_int(0, 0, new_map.map_width - width - 1)
        y = libtcodpy.random_get_int(0, 0, new_map.map_height - height - 1)

        new_room = Rectangle(x, y, width, height)

        failed = False
        for other_room in rooms:
            if new_room.intersects(other_room):
                failed = True
                break

        if not failed:
            _create_room(new_map, new_room)

            (new_x, new_y) = new_room.center()

            if rooms_amount == 0:
                player.x_pos = new_x
                player.y_pos = new_y

            else:
                (prev_x, prev_y) = rooms[rooms_amount - 1].center()

                if libtcodpy.random_get_int(0, 0, 1) == 1:
                    _create_horizontal_tunnel(new_map, prev_x, new_x, prev_y)
                    _create_vertical_tunnel(new_map, prev_y, new_y, new_x)
                else:
                    _create_vertical_tunnel(new_map, prev_y, new_y, prev_x)
                    _create_horizontal_tunnel(new_map, prev_x, new_x, new_y)

            place_map_entities(new_map, new_room)
            rooms.append(new_room)
            rooms_amount += 1

    new_map.initialize_fov()
    return new_map


def _create_room(new_map, room):
    for x in range(room.x1, room.x2+1):
        for y in range(room.y1, room.y2+1):
            new_map.is_walkable[x][y] = True
            new_map.is_transparent[x][y] = True


def _create_horizontal_tunnel(new_map, x1, x2, y):
    for x in range(min(x1, x2), (max(x1, x2)+1)):
        new_map.is_walkable[x][y] = True
        new_map.is_transparent[x][y] = True


def _create_vertical_tunnel(new_map, y1, y2, x):
    global game_map
    for y in range(min(y1, y2), max(y1, y2)+1):
        new_map.is_walkable[x][y] = True
        new_map.is_transparent[x][y] = True


def place_map_entities(new_map, room):
    monster_amount = libtcodpy.random_get_int(0, 0, MAX_ROOM_MONSTERS)

    for i in range(monster_amount):
        x = libtcodpy.random_get_int(0, room.x1, room.x2)
        y = libtcodpy.random_get_int(0, room.y1, room.y2)

        if libtcodpy.random_get_int(0, 0, 100) < 80:  # 80 % chance of orc
            fighter_component = components.Fighter(hp=10, defence=0, power=3, death_function=ai.monster_death)
            ai_component = components.AI(ai.basic_monster)
            monster = components.Entity(x, y, 'orc', 'o', libtcodpy.desaturated_green, is_walkable=False,
                                        fighter=fighter_component, ai=ai_component)
        else:
            fighter_component = components.Fighter(hp=16, defence=1, power=4, death_function=ai.monster_death)
            ai_component = components.AI(ai.basic_monster)
            monster = components.Entity(x, y, 'troll', 'T', libtcodpy.darker_green, is_walkable=False,
                                        fighter=fighter_component, ai=ai_component)  # Troll

        if new_map.is_tile_walkable(x, y):
            new_map.map_entities.append(monster)
            monster.current_map = new_map
