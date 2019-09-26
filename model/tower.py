import math

from .character import Character
from .magic_line import MagicLine
from .color import Color

class Tower(Character):
    def __init__(self, sprite, damage, range, fire_time, effect, position, side_size, price, attack_color = Color.LIGHT_BLUE):
        super().__init__(sprite, position, side_size)
        self.damage = damage
        self.range = range
        self.target = None
        self.fire_time = fire_time
        self.current_time = 0
        self.price = price
        self.current_price = price
        self.magic_lines = []
        self.attack_color = attack_color
        self.current_level = 1

    def update(self, dt):
        new_lines = []
        for line in self.magic_lines:
            if not line.timeout():
                line.update(dt)
                new_lines.append(line)
        self.magic_lines = new_lines
        if self.has_target() and (not self.on_range_of(self.target) or not self.target.is_alive() or self.target.arrived):
            self.target = None
        if self.can_fire() and self.has_target():
            self.fire(self.target)
        else:
            self.colling_down(dt)

    def draw(self, screen):
        for line in self.magic_lines:
            line.draw(screen)

    def on_range_of(self, enemy):
        pos_x, pos_y = enemy.pos_x, enemy.pos_y
        distance = math.sqrt((self.pos_x - pos_x) ** 2 + (self.pos_y - pos_y) ** 2)
        return  distance <= self.range

    def fire(self, target):
        self.cool_down()
        self.target.damage(self.damage)
        new_line = MagicLine((self.pos_x, self.pos_y - 15), (self.target.pos_x, self.target.pos_y), self.attack_color, 5)
        self.magic_lines.append(new_line)

    def can_fire(self):
        return self.current_time >= self.fire_time

    def cool_down(self):
        self.current_time = 0

    def colling_down(self, dt):
        self.current_time += dt

    def has_target(self):
        return self.target is not None

    def upgrade(self):
        self.range += 10
        self.fire_time -= 25
        self.damage += 0.5
        self.current_level += 1
    
    def increase_price(self, extra_price):
        self.current_price += extra_price

