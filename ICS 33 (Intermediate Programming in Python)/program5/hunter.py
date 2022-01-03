# The Hunter class is derived (in order) from both Pulsator and Mobile_Simulton.
#   It updates/displays like its Pulsator base, but is also mobile (moving in
#   a straight line or in pursuit of Prey), like its Mobile_Simultion base.


from prey  import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2


class Hunter(Pulsator, Mobile_Simulton):  
    const_dist = 200
    
    def __init__(self, x, y):
        Pulsator.__init__(self, x, y)
        w, h = self.get_dimension()
        Mobile_Simulton.__init__(self, x, y, w, h, 0, 5)
        self.randomize_angle()
        
    def update(self, model):
        eat = Pulsator.update(self, model)
        catch = model.find(lambda x : isinstance(x,Prey) and self.distance(x.get_location()) <= Hunter.const_dist)
        if catch:
            dist, caught = min([(self.distance(s.get_location()), s) for s in catch])
            sx, sy = self.get_location()
            x, y   = caught.get_location()
            self.set_angle(atan2(y - sy, x - sx))
        self.move()
        return eat
