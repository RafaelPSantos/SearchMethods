from .search_method import SearchMethod

class ManhattanDistance(SearchMethod):
    def __init__(self, entrance, target, vertices):
        super().__init__(entrance, target, vertices)

    def calculate(self):
        return abs(self.entrance.line - self.target.line) + abs(self.entrance.column - self.target.column)