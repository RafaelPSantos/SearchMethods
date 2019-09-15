import pygame

class SpriteSheet:
  def __init__(self, filename, cols, rows):
    self.sheet = pygame.image.load(filename).convert_alpha()
    
    self.cols = cols
    self.rows = rows
    self.totalCellCount = cols * rows
    
    self.rect = self.sheet.get_rect()
    w = self.cellWidth = self.rect.width / cols
    h = self.cellHeight = self.rect.height / rows
    
    self.cells = []
    for row in range(rows):
        for col in range(cols):
            pos_x = col % self.totalCellCount * w
            pos_y = row % self.totalCellCount * h
            self.cells.append((pos_x, pos_y, w, h))
    
  def draw(self, surface, cellIndex, x, y, centralized = False):
    if centralized:
        x -= self.cellWidth / 2
        y -= self.cellHeight / 2
    surface.blit(self.sheet, (x, y), self.cells[cellIndex])