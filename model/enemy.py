import math

from .character import Character

class Enemy(Character):
    def __init__(self, animation, position, side_size, path_to_target, hp = 5, value = 10, speed = 0.5):
        super().__init__(animation, position, side_size)
        self.path = path_to_target
        self.path
        self.current_target = self.path[0]
        self.min_distance = 5
        self.max_hp = hp
        self.current_hp = hp
        self.arrived = False
        self.value = value
        self.speed = speed
        self.debuffs = []

    def update(self, dt):
        self.animation.update(dt)
        self.arrived = self.current_target is None
        if self.arrived:
            return
        self.move(dt)

        if self.over_target():
            self.next_target()

        new_debuff_list = []
        for debuff in self.debuffs:
            debuff.update(dt)
            if not debuff.effect_pass():
                new_debuff_list.append(debuff)
        self.debuffs = new_debuff_list

    def move(self, dt):
        speed = self.speed
        error_margin = self.min_distance - 2
        if speed > self.distance_to_target():
            speed = self.distance_to_target()
        speed *= dt
        target_pos_x, target_pos_y = self.current_target.pos_x, self.current_target.pos_y
        if self.pos_x - error_margin > target_pos_x:
            self.pos_x -= speed
        elif self.pos_x + error_margin < target_pos_x:
            self.pos_x += speed

        if self.pos_y  - error_margin> target_pos_y:
            self.pos_y -= speed
        elif self.pos_y + error_margin < target_pos_y:
            self.pos_y += speed

    def over_target(self):
        return self.distance_to_target() <= self.min_distance

    def distance_to_target(self):
        target_pos_x, target_pos_y = self.current_target.pos_x, self.current_target.pos_y
        return math.sqrt((self.pos_x - target_pos_x) ** 2 + (self.pos_y - target_pos_y) ** 2)

    def next_target(self):
        current_index = self.path.index(self.current_target)
        if current_index + 1 < len(self.path):
            self.current_target = self.path[current_index + 1]
        else:
            self.current_target = None
        

    def damage(self, damage, debuff = None):
        self.current_hp -= damage
        if debuff is not None and not self.already_has_a_debuff(debuff.__class__):
            self.debuffs.append(debuff)

    def already_has_a_debuff(self, type_of_debuff):
        for debuff in self.debuffs:
            if isinstance(debuff, type_of_debuff):
                return True
        return False

    def is_alive(self):
        return self.current_hp > 0

