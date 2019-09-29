from .special_effect import SpecialEffect

class SlowDownEffect(SpecialEffect):
    def __init__(self, enemy_affected):
        super().__init__(enemy_affected, 2000, False)
        self.enemy_affected_speed = enemy_affected.speed

    def apply_effect(self):
        self.enemy_affected.speed /= 2

    def revert_effect(self):
        self.enemy_affected.speed = self.enemy_affected_speed