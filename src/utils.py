"""Miscelaneous useful class"""

import pymunk
import pymunk.pygame_util

class Camera:
    """Camera offer function to transform from physic space coordinate to screen coordinate"""

    def __init__(self, x, y, sx, sy, zoom):
        """Instantiate a camera object"""
        # Position of the camera in physic space coordinate
        self.pos = (x, y)
        # Position of the camera on the screen
        self.screen_pos = (sx, sy)
        # Zoom to apply to every distance
        self.zoom = zoom

    def trans_pos(self, pos):
        """Transform a position `(number, number)` into screen coordinate)"""
        return (-self.pos + pos) * self.zoom + self.screen_pos

    def trans_length(self, length):
        """Transform a lenght into screen coordinate"""
        return length * self.zoom

class DrawOptionsWithCamera(pymunk.pygame_util.DrawOptions):
    """Class that inherit DrawOptions and use camera to translate coordinate before drawing them"""

    def __init__(self, screen, camera):
        """Instantiate a DrawOptions using a camera"""
        super().__init__(screen)
        self.camera = camera

    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        """Change coordinate with camera and call draw_circle"""
        pos = self.camera.trans_pos(pos)
        radius = self.camera.trans_length(radius)
        super().draw_circle(pos, angle, radius, outline_color, fill_color)

    def draw_dot(self, size, pos, color):
        """Change coordinate with camera and call draw_dot"""
        pos = self.camera.trans_pos(pos)
        size = self.camera.tran_length(size)
        super().draw_dot(size, pos, color)

    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        """Change coordinate with camera and call draw_fat_segment"""
        a = self.camera.trans_pos(a)
        b = self.camera.trans_pos(b)
        radius = self.camera.trans_length(radius)
        super().draw_fat_segment(a, b, radius, outline_color, fill_color)

    def draw_polygon(self, verts, radius, outline_color, fill_color):
        raise NotImplementedError
        # super.draw_polygon(verts, radius, outline_color, fill_color)

    def draw_segment(self, a, b, color):
        """Change coordinate with camera and call draw_segment"""
        a = self.camera.trans_pos(a)
        b = self.camera.trans_pos(b)
        super().draw_segment(a, b, color)