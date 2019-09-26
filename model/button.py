from .color import Color
from .element import Element

class Button(Element):
    def __init__(self, text, position, size, font_size, centralized_position = True):
        super().__init__(position, size)
        self.text = text
        self.action = None
        self.bellow_mouse = False
        self.font_size = font_size
        self.visible_clause = None
        self.centralized = centralized_position

    def click(self):
        if self.is_active():
            self.bellow_mouse = False
            self.action()

    def draw(self, screen, drawable, font):
        color = Color.WHITE
        if not self.is_active():
            color = Color.DISABLED_COLOR
        black = (0, 0, 0)

        rec = self.rec(self.centralized)
        font = font.SysFont("arial", self.font_size)

        text_color = None
        if self.bellow_mouse and self.is_active():
            text_color = black
            drawable.rect(screen, color, rec)
        else:
            text_color = color
            drawable.rect(screen, color, rec, 1)

        label = None
        if isinstance(self.text, str):
            label = font.render(self.text, 1, text_color)
        else:
            label = font.render(self.text(), 1, text_color)

        text_size = label.get_rect()
        center_pos_x, center_pos_y = self.center_of_rec(self.centralized)
        text_pos_x = center_pos_x - text_size.width / 2
        text_pos_y = center_pos_y - text_size.height / 2
        text_pos = (text_pos_x, text_pos_y)
        screen.blit(label, text_pos)

    def point_inside_area(self, pos_x, pos_y):
        rec_pos_x, rec_pos_y, rec_width, rec_height = self.rec(self.centralized)
        inside_width = rec_pos_x < pos_x and pos_x < (rec_pos_x + rec_width)
        inside_height = rec_pos_y < pos_y and pos_y < (rec_pos_y + rec_height)
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



