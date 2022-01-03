import controller
import model   # Calls to update in update_all are passed a reference to model

#Use the reference to this module to pass it to update methods

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special import Special


# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
cycle_count = 0
running = False
obj_clk = None
stop1 = False
sims = set()
#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global cycle_count, running, stop1, sims
    cycle_count = 0
    running = False
    stop1 = False
    sims = set()
    


#start running the simulation
def start ():
    global running
    running = True


#stop running the simulation (freezing it)
def stop ():
    global running
    running = False


#step just one update in the simulation
def step ():
    global running, stop1
    running = True
    stop1 = True

#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global obj_clk
    obj_clk = str(kind)
    #print(str(kind))

#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    if obj_clk != None:
        if obj_clk == 'Remove':
            for t in find(lambda t: t.contains((x, y))):
                sims.remove(t)
        else:
            sims.add(eval(obj_clk + '(x, y)'))
        


#add simulton s to the simulation
def add(s):
    global sims
    sims.add(s)
    

# remove simulton s from the simulation    
def remove(s):
    global sims
    sims.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    return {x for x in sims if p(x)}


# for each simulton in this simulation, call update (passing model to it) 
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def update_all():
    global running, stop1, cycle_count, world #maybe remove world
    if running == True:
        cycle_count += 1
        sims2 = set(sims)
        for s in sims2:
            if s in sims:
                s.update(model)
        if stop1 == True:
            running = False
            stop1 = False


#How to animate: 1st: delete all simultons on the canvas; 2nd: call display on
#  all simulton being simulated, adding each back to the canvas, maybe in a
#  new location; 3rd: update the label defined in the controller for progress 
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all():
    for o in controller.the_canvas.find_all():
        controller.the_canvas.delete(o)
    
    for s in sims:
        s.display(controller.the_canvas)
    
    controller.the_progress.config(text=str(cycle_count)+" cycles/"+str(len(sims))+" simultons")
