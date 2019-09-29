from .special_effect import SpecialEffect

class BurnEffect(SpecialEffect):
    def __init__(self, enemy_affected):
        super().__init__(enemy_affected, 3000, True)

    def apply_effect(self):
        self.enemy_affected.damage(0.01)