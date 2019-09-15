import pygame

class MagicLine():
    def __init__(self, start_point, end_point, color, weight = 1):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.weight = weight
        self.duration = 50
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.start_point, self.end_point, self.weight)

    def timeout(self):
        return self.current_time >= self.duration