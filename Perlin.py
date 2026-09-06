from pyglet.math import Vec2, Vec3
from pyglet.gl import *
import random

class Perlin_Noise:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grads = [[Vec2(0.0, 0.0) for _ in range(height)] for _ in range(width)]
        self.set_gradients()

    def set_gradients(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grads[x][y] = self.random_unit()

    def random_unit(self):
        while True:
            random_v = Vec2(random.uniform(-1,1), random.uniform(-1,1))
            if random_v.length() > 0:
                break
        return random_v.normalize()
    
    def smooth(self, t):
        return 3 * t ** 2 - 2 * t ** 3

    def at(self, x, y):
        q = Vec2(x, y)
        x0 = int(x)
        x1 = int(x+1)
        y0 = int(y)
        y1 = int(y+1)

        l00 = self.grads[x0][y0].dot(1-Vec2(x0, y0))
        l01 = self.grads[x0][y1].dot(1-Vec2(x0, y1))
        l10 = self.grads[x1][y0].dot(1-Vec2(x1, y0))
        l11 = self.grads[x1][y1].dot(1-Vec2(x1, y1))

        t = x - x0
        u = y - y0

        