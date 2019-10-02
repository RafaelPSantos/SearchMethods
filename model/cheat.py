class Cheat():
    def __init__(self, pass_code, cheat):
        self.pass_code = pass_code
        self.current_pass_code = ''
        self.cheat = cheat
        self.expire_time = 3000
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.expire_time:
            self.reset()

    def update_code(self, next_letter):
        self.current_pass_code += next_letter
        if self.correct_code_inserted():
            self.apply_cheat()

    def reset(self):
        self.current_pass_code = ''
        self.current_time = 0

    def apply_cheat(self):
        self.cheat()

    def correct_code_inserted(self):
        return self.current_pass_code == self.pass_code