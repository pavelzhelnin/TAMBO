import numpy as np

from tambo.geometry import Geometry
from tambo.track import Track

class TAMBO(object):
    """
    Master class of TAMBO.
    """  
    def __init__(self, geometry: Geometry): 
        self.geometry = geometry

    def inject_particle(self, trajectory: Track):
        end_points = trajectory.find_end_points(self.geometry)

    def __integrate_cd(self, t,array):
    
        #array = beginning x,y,z and endpoint x,y,z 
    
        density_of_rock =  5520 #"kg/m^3"
        density_of_air = 1225 #"kg/m^3" 
        z = array[0][2] + (t * array[1][2])
        y = array[0][1] + (t * array[1][1])
        x = array[0][0] + (t * array[1][0])
    
        dzdt = array[1][2]
        dydt = array[1][1]
        dxdt = array[1][0]
    
        if z <= meters_elevations.ev(x,y): 
            return density_of_rock * np.sqrt(1+ dzdt**2 + dydt**2 + dxdt**2)
        if z > meters_elevations.ev(x,y): 
            return density_of_air * np.sqrt(1+ dzdt**2 + dydt**2 + dxdt**2)
    