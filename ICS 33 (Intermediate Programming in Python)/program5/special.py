'''For special, I have modified the Blackhole. It is no longer constant, it 
pulsates (grows and shrinks constantly). It has a default yellow color, and 
everytime it eats a ball it blinks as green. 
'''

from blackhole import Black_Hole

class Special(Black_Hole):
    cycle_count = 50
    max_hole = 40
    min_hole = 10
    
    
    def __init__(self, x, y):
        Black_Hole.__init__(self, x, y)
        self.dsize = 1
        self.color = 'yellow'
        
    def update(self, model):
        self.color = 'yellow'
        w, h = self.get_dimension()
        self.set_dimension(w + self.dsize, h + self.dsize)
        #print(w, h)
        #print('bef', self.get_dimension()[0])
        
        if self.get_dimension()[0] == Special.max_hole:
            self.dsize = -1
            #print('aft', self.get_dimension()[0])
            
        if self.get_dimension()[0] == Special.min_hole:
            self.dsize = 1
            #print('-aft', self.get_dimension()[0])
        v = Black_Hole.update(self, model)
        if v != set():
            self.color = 'green'
        return v
            
    
    
    def display(self, the_canvas):
        w, h = self.get_dimension()
        the_canvas.create_oval(self._x - w/2, self._y - h/2, self._x + w/2, self._y + h/2, fill= self.color)
        
