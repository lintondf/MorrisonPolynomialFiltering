''' PolynomialFiltering.Geodesy
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''


from abc import ABC, abstractmethod
from numpy import array, pi, sin, cos, transpose, sqrt, arctan2, zeros
from numpy import array as vector
from math import radians

from polynomialfiltering.PythonUtilities import copy
from polynomialfiltering.Geodesy import Geodesy

class Site(ABC):
    '''@ name : str'''
    '''@ latitude : float'''
    '''@ longitude : float'''
    '''@ altitude : float'''
    '''@ ecef : vector'''
    '''@ DC : array'''
    def __init__(self, name : str, latitude : float, longitude : float, altitude : float, geodesy : Geodesy = Geodesy(), xi : float = 0.0, eta : float = 0.0):
        '''
        Constructor
        '''
        self.name = name;
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        
        self.ecef = geodesy.geodetic2ECEF(latitude, longitude, altitude)
        self.DC = Site.siteMatrix(latitude, longitude, xi, eta)
        
    @staticmethod
    def siteMatrix(geoLatitude : float, geoLongitude : float, xi : float = 0.0, eta : float = 0.0) -> array:
        '''@ cosLat : float'''
        '''@ latitude : float'''
        '''@ longitude : float'''
        '''@ cosX : float'''
        '''@ sinX : float'''
        '''@ cosZ : float'''
        '''@ sinZ : float'''
        '''@ Mx : array'''
        '''@ Mz : array'''
        '''@ DC : array'''
        cosLat = cos(geoLatitude)
        latitude = geoLatitude + xi;
        longitude = geoLongitude + eta / cosLat
#         x = 0.5*pi - latitude # TODO trig subsitutions to eliminate
#         z = 1.5*pi - longitude
        cosX = sin(latitude)
        sinX = cos(latitude)
        cosZ = -sin(longitude)
        sinZ = -cos(longitude)
        Mx = zeros([3,3])
        Mz = zeros([3,3])
#         Mx = array([[1.0, 0, 0],[0, cosX, sinX],[0, -sinX, cosX]])
        Mx[0,0] = 1.0
        Mx[1,1] = cosX;
        Mx[1,2] = sinX;
        Mx[2,1] = -sinX;
        Mx[2,2] = cosX;
#         Mz = array([[cosZ, -sinZ, 0],[sinZ, cosZ, 0],[0, 0, 1]])
        Mz[0,0] = cosZ;
        Mz[0,1] = -sinZ;
        Mz[1,0] = sinZ;
        Mz[1,1] = cosZ;
        Mz[2,2] = 1.0;
        DC = transpose(Mx @ Mz)
        return DC
    
    @staticmethod
    def ENU2AER(ENU : array ) -> array:
        '''@ EN2 : array'''
        '''@ EN : array'''
        '''@ AER : array'''
        EN2 = ENU[:, 0]*ENU[:, 0] + ENU[:, 1]*ENU[:, 1];
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
        '''@ ENU : array'''
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
        '''@ L : array'''
        '''@ ENU : array'''
        L = copy(ECEF)
        L[:,0] = L[:,0] - self.ecef[0]
        L[:,1] = L[:,1] - self.ecef[1]
        L[:,2] = L[:,2] - self.ecef[2]
        ENU = zeros([ECEF.shape[0], ECEF.shape[1]])
        ENU[:,0:3] = (L[:,0:3] @ self.DC)
        if (ENU.shape[1] > 3) :
            ENU[:,3:6] = ECEF[:,3:6] @ self.DC
        return ENU
    
    def ENU2ECEF(self, ENU : array ) -> array:
        '''@ ECEF : array'''
        ECEF = zeros([ENU.shape[0], ENU.shape[1]])
        ECEF[:,0:3] = ENU[:,0:3] @ transpose(self.DC)
        ECEF[:,0] = ECEF[:,0] + self.ecef[0]
        ECEF[:,1] = ECEF[:,1] + self.ecef[1]
        ECEF[:,2] = ECEF[:,2] + self.ecef[2]
        if (ENU.shape[1] > 3) :
            ECEF[:,3:6] = ENU[:,3:6] @ transpose(self.DC)
        return ECEF
