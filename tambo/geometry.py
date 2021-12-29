from os import set_inheritable
from numba.core.decorators import njit
from numba.core.types.scalars import Float
import numpy as np
from numba import jit
from scipy.interpolate import SmoothBivariateSpline

class Point(object):
    """
    Coordinate point.
    """  
    def __init__(self,longitude: Float, latitude: Float, elevation: Float, latmin: Float = 0., longmin: Float = 0.):
        self.longitude = longitude
        self.latitude = latitude
        self.elevation = elevation
        self.x, self.y = self.__set_distance_coordinate(latmin,longmin)
        self.z = self.elevation

#    @jit
    def __set_distance_coordinate(self,latmin: Float,longmin: Float):
        """
        Implements conversion from coordinate location to a coordinate in meters.
        """    
        latMid = (self.latitude + latmin)/2.0
        m_per_deg_lon = (111132.954 - (559.822 * np.cos( 2.0 * latMid )) + (1.175 * np.cos( 4.0 * latMid)) + (0.0023 * np.cos( 6.0 * latMid)))
        m_per_deg_lat = (111412.82 * np.cos(latMid)) - (93.5*np.cos(latMid*3)) + (0.118*np.cos(5*latMid))
        delta_lat = self.latitude - latmin 
        delta_long = self.longitude - longmin 

        x = delta_long * (m_per_deg_lon * 180./np.pi)
        y = delta_lat * (m_per_deg_lat * 180./np.pi)

        return x,y

class Direction(object):
    """
    Direction of motion.
    """    
    def __init__(self,phi: Float,theta: Float):
        self.phi = phi
        self.theta = theta

        self.x = np.cos(theta)*np.sin(phi)
        self.y = np.sin(theta)*np.sin(phi)
        self.z = np.cos(phi)
        
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
        self.__number_of_geometry_points = len(self.Lat)

        self.latmax = np.max(self.Lat)
        self.longmax = np.max(self.Long)
        self.elevmax = np.max(self.Elev)
        self.latmin = np.min(self.Lat)
        self.longmin = np.min(self.Long)
        self.elevmin = np.min(self.Elev)

        self.Coordinate_points = [Point(self.Lat[i],self.Long[i],self.Elev[i],self.latmin, self.longmin) for i in range(self.__number_of_geometry_points)]

        self.geometry_spline = self.__construct_spline()
        self.geometry_box = self.__compute_dim_array()

        self.density_of_rock =  5520 #"kg/m^3"
        self.density_of_air = 1225 #"kg/m^3" 
        
#    @jit
    def __coords_to_meters(self,longitude: Float,latitude: Float): 
        """
        Implements conversion from coordinate location to a coordinate in meters.
        """    
        latMid = (latitude + self.latmin)/2.0

        m_per_deg_lat = (111132.954 - (559.822 * np.cos( 2.0 * latMid )) + (1.175 * np.cos( 4.0 * latMid)) 
        + (0.0023 * np.cos( 6.0 * latMid)))
        m_per_deg_lon = (111412.82 * np.cos(latMid)) - (93.5*np.cos(latMid*3)) + (0.118*np.cos(5*latMid))
    
        delta_lat = latitude - self.latmin 
        delta_long = longitude - self.longmin 
    
        x = delta_long * (m_per_deg_lon * 180/np.pi)
        y = delta_lat * (m_per_deg_lat * 180/np.pi)
        
        return np.around(np.array([x,y],dtype =np.float32),3)
    
    def __compute_dim_array(self): 
        """
        TODO
        """    
        max_meters = self.__coords_to_meters(self.longmax,self.latmax)
        array = ([0.0,max_meters[0],0.0,max_meters[1],self.elevmin,self.elevmax])
        return np.around(np.array(array,dtype =np.float32),3)
        
    def __construct_spline(self): 
        """
        TODO
        """    
        x = [self.__coords_to_meters(g,i) for i,g in zip(self.Lat,self.Long)]
        Meters_Lats = [x[i][1] for i,c in enumerate(x)]
        Meters_Longs = [x[i][0] for i,c in enumerate(x)]
        return SmoothBivariateSpline(Meters_Longs,Meters_Lats,self.Elev,kx=3,ky=3)

if __name__ == "__main__":
    geo = Geometry("../resources/ColcaValleyData.txt")
    point = geo.Coordinate_points[0]
    print(geo.geometry_spline(point.x,point.y),point.elevation)