from os import set_inheritable
from numba.core.decorators import njit
import numpy as np
from numba import jit
from scipy.interpolate import SmoothBivariateSpline

class Track: 
    """
    Primary Particle Trajectory TAMBO.
    """  
    def __init__(self, point, direction): 
        self.point = point
        self.direction = direction

    def __get_line_eq(self): 
        data = [self.point.x,self.point.y,self.point.z,
                self.direction.x,self.direction.y,self.direction.z]
        data = np.array(data, dtype=np.float32)
        data = np.around(data,3)
        return data
    
    def __find_end_points(self,alpha):
    
        start_pts1 = np.around(np.array([alpha[0],alpha[1],alpha[2]], dtype = np.float32),3)
        start_pts = [alpha[0],alpha[0],alpha[1],alpha[1],alpha[2],alpha[2]]
        start_pts = np.array(start_pts,dtype = np.float32)
        start_pts = np.around(start_pts,3)
        direct_pts = [alpha[3],alpha[3],alpha[4],alpha[4],alpha[5],alpha[5]]
        direct_pts = np.array(direct_pts,dtype = np.float32)
        direct_pts = np.around(direct_pts,3)
    
        for count,g in enumerate(array):
        
            flag = False
        
            if direct_pts[count] == 0: 
                continue       
        
            t = (g - start_pts[count])/direct_pts[count]
        
            if t < 0 or t == 0:  
                continue
            potential_endps = ([alpha[0]+(t*alpha[3]),alpha[1]+(t*alpha[4]),
                                alpha[2]+(t*alpha[5])])
            potential_endps = np.array(potential_endps,dtype = np.float32)
            potential_endps = np.around(potential_endps,3)
            
            #[for c,z in potential_endps]
            for c,z in enumerate(potential_endps): 

                if z < array[2*c] or z > array[2*c+1]:
                    flag = True 
                    break 
                
            if flag == False: 
    
                data = np.array(potential_endps, dtype=np.float32)
                data = np.around(data,3)
                endps = np.subtract(data,start_pts1)
                enpds = np.around(endps,3)
                return start_pts1,endps
            
    def integrate_cd (t,array):
    
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
    