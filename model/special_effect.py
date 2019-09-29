class SpecialEffect():
    def __init__(self, enemy_affected, duration, continuos = False):
        self.enemy_affected = enemy_affected
        self.applied = False
        self.duration = duration
        self.continuos = continuos

    def update(self, dt):
        if not self.applied:
            self.apply_effect()
            if not self.continuos:
                self.applied = True
        if not self.effect_pass():
            self.duration -= dt
            if self.effect_pass():
                self.revert_effect()

    def apply_effect(self):
        pass

    def revert_effect(self):
        pass

    def effect_pass(self):
        return self.duration <= 0