from os import set_inheritable
from numba.core.decorators import njit
import numpy as np
from numba import jit
from scipy.interpolate import SmoothBivariateSpline

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
        self.number_of_geometry_points = len(self.Lat)

        self.latmax = np.max(self.Lat)
        self.longmax = np.max(self.Long)
        self.elevmax = np.max(self.Elev)
        self.latmin = np.min(self.Lat)
        self.longmin = np.min(self.Long)
        self.elevmin = np.min(self.Elev)

        self.Coordinate_points = [Point(self.Lat[i],self.Long[i],self.Elev[i],self.latmin, self.longmin) for i in range(self.number_of_geometry_points)]

        self.geometry_spline = self.construct_spline()
        self.geometry_box = self.compute_dim_array()
        
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
    
    def compute_dim_array(self): 
        """
        TODO
        """    
        max_meters = self.coords_to_meters(self.longmax,self.latmax)
        array = ([0.0,max_meters[0],0.0,max_meters[1],self.elevmin,self.elevmax])
        return np.around(np.array(array,dtype =np.float32),3)
        
    def construct_spline(self): 
        """
        TODO
        """    
        x = [self.coords_to_meters(g,i) for i,g in zip(self.Lat,self.Long)]
        Meters_Lats = [x[i][1] for i,c in enumerate(x)]
        Meters_Longs = [x[i][0] for i,c in enumerate(x)]
        return SmoothBivariateSpline(Meters_Longs,Meters_Lats,self.Elev,kx=3,ky=3)