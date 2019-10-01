'''
Created on Sep 30, 2019

@author: lintondf
'''

from abc import ABC, abstractmethod
from numpy import array, pi, sin, cos, transpose, sqrt, arctan2, zeros
from numpy import array as vector
from math import radians



class Geodesy(ABC):
    '''
    Geodetic and related coordinate transforms
    '''


    def __init__(self):
        '''
        WGS-84 constants
        '''
        self.a = 6378137;
        self.b = 6.356752314200000e+006;
        self.f = 3.352810671830990e-003;
        self.ecc = 8.181919092890633e-002; 
        self.e2 = 6.694380004260828e-003;
        self.secEcc = 8.209443803685426e-002;
        self.secEccSqr = 6.739496756586904e-003;
        self.mu = 3.986004418000000e+014;
        self.omega = 7.292115000000000e-005;
        self.J2 = 1.082629989000000e-003;
        self.J3 = -2.538810000000000e-006;
        self.J4 = -1.610000000000000e-006;
        self.origin = [0, 0, 0];
        
        
    def geodetic2ECEF(self, latitude : float, longitude : float, altitude : float) -> vector:
        rc = self.a / max(1.0e-14, sqrt(( 1 - self.e2 * ( sin( latitude ) )**2 )) )
        ECEF = array([[(rc + altitude) * cos(latitude) * cos(longitude),
                       (rc + altitude) * cos(latitude) * sin(longitude),
                       (rc * (1 - self.e2) + altitude) * sin(latitude)]])
        return ECEF
        
        
class Site(ABC):
    def __init__(self, name : str, latitude : float, longitude : float, altitude : float, geodesy : Geodesy = Geodesy(), xi : float = 0.0, eta : float = 0.0):
        '''
        Constructor
        '''
        self.name = name;
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        
        self.ecef = geodesy.geodetic2ECEF(latitude, longitude, altitude)[0,:]
        self.DC = Site.siteMatrix(latitude, longitude, xi, eta)
        
    @staticmethod
    def siteMatrix(latitude : float, longitude : float, xi : float = 0.0, eta : float = 0.0) -> array:
        cosLat = cos(latitude)
        latitude += xi;
        longitude += eta / cosLat
        x = 0.5*pi - latitude
        z = 1.5*pi - longitude
        Mx = array([[1.0, 0, 0],[0, cos(x), sin(x)],[0, -sin(x), cos(x)]])
        Mz = array([[cos(z), -sin(z), 0],[sin(z), cos(z), 0],[0, 0, 1]])
        DC = transpose(Mx @ Mz)
        return DC
    
    @staticmethod
    def ENU2AER(ENU : array ) -> array:
        EN2 = ENU[:, 0]**2 + ENU[:, 1]**2;
        EN = sqrt( EN2 )
        AER = zeros([ENU.shape[0], ENU.shape[1]])
        AER[:, 0] = arctan2( ENU[:, 0], ENU[:,1] );
        AER[:, 1] = arctan2( ENU[:, 2], EN );
        AER[:, 2] = sqrt( ENU[:, 0]**2 + ENU[:, 1]**2 + ENU[:, 2]**2 );

        if (ENU.shape[1] > 3) :
            AER[:, 3] = (ENU[:, 3]*ENU[:, 1] - ENU[:, 0]*ENU[:, 4]) / EN2;
            AER[:, 5] = (ENU[:, 0]*ENU[:, 3] + ENU[:, 1]*ENU[:, 4] + ENU[:, 2]*ENU[:, 5]) / AER[:, 2];
            AER[:, 4] = (ENU[:, 5]*AER[:, 2] - ENU[:, 2]*AER[:, 5]) / (AER[:, 2]*EN);
        return AER
    
    @staticmethod
    def AER2ENU(AER : array) -> array:
        ENU = zeros([AER.shape[0], AER.shape[1]])
        ENU[:, 0] = AER[:,2] * cos(AER[:,1]) * sin(AER[:,0]);
        ENU[:, 1] = AER[:,2] * cos(AER[:,1]) * cos(AER[:,0]);
        ENU[:, 2] = AER[:,2] * sin(AER[:,1]);
        if (AER.shape[1] > 3) :
            ENU[:, 3] = (AER[:,5] * sin(AER[:,0]) * cos(AER[:,1])) + (AER[:,2] * cos(AER[:,0]) * AER[:,3] * cos(AER[:,1])) - (AER[:,2] * sin(AER[:,0]) * sin(AER[:,1]) * AER[:,4]);
            ENU[:, 4] = (AER[:,5] * cos(AER[:,0]) * cos(AER[:,1])) - (AER[:,2] * sin(AER[:,0]) * AER[:,3] * cos(AER[:,1])) - (AER[:,2] * cos(AER[:,0]) * sin(AER[:,1]) * AER[:,4]);
            ENU[:, 5] = (AER[:,5] * sin(AER[:,1])) + (AER[:,2] * cos(AER[:,1]) * AER[:,4]);
        return ENU
    
    def ECEF2ENU(self, ECEF : array) -> array:
        L = ECEF.copy()
        L[:,0] -= self.ecef[0]
        L[:,1] -= self.ecef[1]
        L[:,2] -= self.ecef[2]
        ENU = zeros([ECEF.shape[0], ECEF.shape[1]])
        ENU[:,0:3] = (L[:,0:3] @ self.DC)
        if (ENU.shape[1] > 3) :
            ENU[:,3:6] = ECEF[:,3:6] @ self.DC
        return ENU
    
    def ENU2ECEF(self, ENU : array ) -> array:
        ECEF = zeros([ENU.shape[0], ENU.shape[1]])
        ECEF[:,0:3] = ENU[:,0:3] @ transpose(self.DC)
        ECEF[:,0] += self.ecef[0]
        ECEF[:,1] += self.ecef[1]
        ECEF[:,2] += self.ecef[2]
        if (ENU.shape[1] > 3) :
            ECEF[:,3:6] = ENU[:,3:6] @ transpose(self.DC)
        return ECEF
       

