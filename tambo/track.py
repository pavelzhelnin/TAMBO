from os import set_inheritable
from numba.core.decorators import njit
import numpy as np
from numba import jit

from tambo.geometry import Direction, Geometry, Point

class Track: 
    """
    Primary Particle Trajectory TAMBO.
    """  
    def __init__(self, point: Point, direction: Direction): 
        """
        Constructs particle trajectory.
        """    
        self.point = point
        self.direction = direction
        self.alpha = self.__get_line_eq()

    def __get_line_eq(self): 
        """
        Builds auxiliary trajectory arrray.
        """    
        data = [self.point.x,self.point.y,self.point.z,
                self.direction.x,self.direction.y,self.direction.z]
        data = np.array(data, dtype=np.float32)
        data = np.around(data,3)
        return data
    
    def find_end_points(self, geometry: Geometry):
        """
        Returns the end points of the track for a given geometry.
        """    
        start_pts1 = np.around(np.array([self.alpha[0],self.alpha[1],self.alpha[2]], dtype = np.float32),3)
        start_pts = [self.alpha[0],self.alpha[0],self.alpha[1],self.alpha[1],self.alpha[2],self.alpha[2]]
        start_pts = np.array(start_pts,dtype = np.float32)
        start_pts = np.around(start_pts,3)
        direct_pts = [self.alpha[3],self.alpha[3],self.alpha[4],self.alpha[4],self.alpha[5],self.alpha[5]]
        direct_pts = np.array(direct_pts,dtype = np.float32)
        direct_pts = np.around(direct_pts,3)
    
        for count,g in enumerate(geometry.geometry_box):
        
            flag = False
        
            if direct_pts[count] == 0: 
                continue       
        
            t = (g - start_pts[count])/direct_pts[count]
        
            if t < 0 or t == 0:  
                continue
            potential_endps = ([self.alpha[0]+(t*self.alpha[3]),self.alpha[1]+(t*self.alpha[4]),
                                self.alpha[2]+(t*self.alpha[5])])
            potential_endps = np.array(potential_endps,dtype = np.float32)
            potential_endps = np.around(potential_endps,3)
            
            #[for c,z in potential_endps]
            for c,z in enumerate(potential_endps): 

                if z < geometry.geometry_box[2*c] or z > geometry.geometry_box[2*c+1]:
                    flag = True 
                    break 
                
            if flag == False: 
                data = np.array(potential_endps, dtype=np.float32)
                data = np.around(data,3)
                endps = np.subtract(data,start_pts1)
                enpds = np.around(endps,3)
                return start_pts1,endps