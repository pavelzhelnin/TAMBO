from os import set_inheritable
from numba.core.decorators import njit
import numpy as np
from numba import jit

class Point(object):
    def __init__(self,longitude, latitude, elevation, latmin = 0, longmin = 0):
        self.longitude = longitude
        self.latitude = latitude
        self.elevation = elevation
        self.set_distance_coordinate(latmin,longmin)

    @njit
    def set_distance_coordinate(self,latmin,longmin):
        """
        Implements conversion from coordinate location to a coordinate in meters.
        """    
        latMid = (self.latitude + latmin)/2.0
        m_per_deg_lon = (111132.954 - (559.822 * np.cos( 2.0 * latMid )) + (1.175 * np.cos( 4.0 * latMid)) + (0.0023 * np.cos( 6.0 * latMid)))
        m_per_deg_lat = (111412.82 * np.cos(latMid)) - (93.5*np.cos(latMid*3)) + (0.118*np.cos(5*latMid))
        delta_lat = self.latitude - latmin 
        delta_long = self.longitude - longmin 

        self.x = delta_long * (m_per_deg_lon * 180/np.pi)
        self.y = delta_lat * (m_per_deg_lat * 180/np.pi)

class Geometry(object): 
    """
    Implements the basic geometry of TAMBO.
    """    
    def __init__(self,
                text, #text file of geometry data in lat/long/elev format 
                ): 

        datafile = np.genfromtxt(text, delimiter = "\t", skip_header = 1)

        self.Lat = np.deg2rad(datafile[:,1])
        self.Long = np.deg2rad(datafile[:,2])
        self.Elev = datafile[:,3]

        self.latmax = np.max(self.Lat)
        self.longmax = np.max(self.Long)
        self.elevmax = np.max(self.Elev)
        self.latmin = np.min(self.Lat)
        self.longmin = np.min(self.Long)
        self.elevmin = np.min(self.Elev)
        
    @njit
    def coords_to_meters(self,longitude,latitude): 
        """
        Implements conversion from coordinate location to a coordinate in meters.
        """    
        latmin = self.latmin
        longmin = self.longmin
    
        latMid = (latitude + latmin)/2.0

        m_per_deg_lat = (111132.954 - (559.822 * np.cos( 2.0 * latMid )) + (1.175 * np.cos( 4.0 * latMid)) 
        + (0.0023 * np.cos( 6.0 * latMid)))
        m_per_deg_lon = (111412.82 * np.cos(latMid)) - (93.5*np.cos(latMid*3)) + (0.118*np.cos(5*latMid))
    
        delta_lat = latitude - latmin 
        delta_long = longitude - longmin 
    
        x = delta_long * (m_per_deg_lon * 180/np.pi)
        y = delta_lat * (m_per_deg_lat * 180/np.pi)
        
        return np.around(np.array([x,y],dtype =np.float32),3)
    
    def dim_array(self): 
        
        self.max_meters = self.coords_to_meters(self.longmax,self.latmax);
        
        array = ([0.0,self.max_meters[0],0.0,self.max_meters[1],self.elevmin,self.elevmax]);
        self.array = np.around(np.array(array,dtype =np.float32),3); 
        
        return array 
        
    def spline(self): 
        
        x = [coords_to_meters(g,i) for i,g in zip(self.Lat,self.Long)]
        Meters_Lats = [x[i][1] for i,c in enumerate(x)]
        Meters_Longs = [x[i][0] for i,c in enumerate(x)]
        spline = SmoothBivariateSpline(Meters_Longs,Meters_Lats,Elev,kx=3,ky=3)
        
        return spline