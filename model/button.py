class Button():
    def __init__(self, text, pos, size, font_size):
        self.text = text
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.action = None
        self.bellow_mouse = False
        self.font_size = font_size
        self.visible_clause = None

    def click(self):
        if self.is_active():
            self.bellow_mouse = False
            self.action()

    def draw(self, screen, drawable, font):
        white = (255, 255, 255)
        black = (0, 0, 0)
        rec = (self.left_margin(), self.top_margin(), self.width, self.height)
        font = font.SysFont("arial", self.font_size)

        text_color = None
        if self.bellow_mouse and self.is_active():
            text_color = black
            drawable.rect(screen, white, rec)
        else:
            text_color = white
            drawable.rect(screen, white, rec, 1)

        label = None
        if isinstance(self.text, str):
            label = font.render(self.text, 1, text_color)
        else:
            label = font.render(self.text(), 1, text_color)
        
        text_size = label.get_rect()
        text_pos = (self.pos_x - text_size.width / 2, self.pos_y - text_size.height / 2)
        screen.blit(label, text_pos)

    def left_margin(self):
        pos_x = self.current_position()[0]
        return pos_x - self.width / 2

    def right_margin(self):
        pos_x = self.current_position()[0]
        return pos_x + self.width / 2

    def top_margin(self):
        pos_y = self.current_position()[1]
        return pos_y - self.height / 2

    def bottom_margin(self):
        pos_y = self.current_position()[1]
        return pos_y + self.height / 2

    def point_inside_area(self, pos_x, pos_y):
        inside_width = pos_x > self.left_margin() and pos_x < self.right_margin()
        inside_height = pos_y < self.bottom_margin() and pos_y > self.top_margin()
        return inside_width and inside_height

    def current_position(self):
        def value_of(variable):
            if callable(variable):
                return variable()
            else:
                return variable
        return (value_of(self.pos_x), value_of(self.pos_y))

    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height

    def change_position(self, new_pos_x, new_pos_y):
        self.pos_x = new_pos_x
        self.pos_y = new_pos_y

    def on_click(self, action):
        self.action = action

    def active_if(self, clause):
        self.is_active = clause

    def is_active(self):
        return True

    def visible_if(self, clause):
        self.is_visible = clause

    def is_visible(self):
        return True



