import libtcodpy


class DungeonMap(object):
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.map_objects = []
        self.recompute_fov = True
        self.fov_map = None
        self.is_walkable = [[False for y in range(map_height)] for x in range(map_width)]
        self.is_explored = [[False for y in range(map_height)] for x in range(map_width)]
        self.is_transparent = [[False for y in range(map_height)] for x in range(map_width)]

    def initialize_fov(self):
        self.recompute_fov = True
        self.fov_map = libtcodpy.map_new(self.map_width, self.map_height)
        for y in range(self.map_height):
            for x in range(self.map_width):
                libtcodpy.map_set_properties(
                    self.fov_map, x, y, self.is_transparent[x][y], self.is_walkable[x][y])

    def is_walkable(self, x, y):
        if x < 0 or x >= self.map_width or y < 0 or y >= self.map_height:
            return False

        if not self.is_walkable[x][y]:
            return False

        for map_object in self.map_objects:
            if not map_object.is_walkable and map_object.x_pos == x and map_object.y_pos == y:
                return False

        return True
