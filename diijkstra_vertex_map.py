class DiijkstraVertexMap():
    def __init__(self, vertex):
        self.vertex = vertex
        self.estimation = None
        self.prescient = None
        self.locked = None

    def lock(self):
        self.locked = True