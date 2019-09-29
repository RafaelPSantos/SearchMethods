class Animation():
    def __init__(self, sprites, sprite_time = 1000):
        self.sprites = sprites
        self.current_sprite_id = 0
        self.sprite_time = sprite_time
        self.current_sprite_time = 0

    def update(self, dt):
        if len(self.sprites) == 1:
            return
        self.current_sprite_time += dt
        if self.current_sprite_time > self.sprite_time:
            self.current_sprite_time = 0
            self.next_sprite()

    def next_sprite(self):
        self.current_sprite_id += 1
        if self.current_sprite_id > len(self.sprites) - 1:
            self.current_sprite_id = 0

    def sprite(self):
        return self.sprites[self.current_sprite_id]
