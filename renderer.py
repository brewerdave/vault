def draw(self):
    if libtcodpy.map_is_in_fov(fov_map, self.x_pos, self.y_pos):
        libtcodpy.console_set_default_foreground(console, self.symbol_color)
        libtcodpy.console_put_char(console, self.x_pos, self.y_pos, self.symbol, libtcodpy.BKGND_NONE)


def clear(self):
    libtcodpy.console_put_char(console, self.x_pos, self.y_pos, ' ', libtcodpy.BKGND_NONE)