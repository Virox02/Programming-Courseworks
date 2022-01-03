# The Black_Hole class is derived from Simulton; for updating it finds+removes
#   objects (of any class derived from Prey) whose center is contained inside
#   its radius (returning a set of all eaten simultons), and displays as a
#   black circle with a radius of 10 (width/height 20).
# Calling get_dimension for the width/height (for containment and displaying)'
#   will facilitate inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):  
    radius = 10
    
    def __init__(self, x, y):
        Simulton.__init__(self, x, y, 2 * Black_Hole.radius, 2 * Black_Hole.radius)
         
    def update(self, model):
        suck = model.find(lambda smltn: isinstance(smltn, Prey) and self.contains(smltn.get_location()))
        for smltn in suck:
            model.remove(smltn)
        return suck
    
    def contains(self, xy):
        return self.distance(xy) <= self.get_dimension()[0]/2
    
    def display(self, the_canvas):
        w, h = self.get_dimension()
        the_canvas.create_oval(self._x - w/2, self._y - h/2, self._x + w/2, self._y + h/2, fill='black')