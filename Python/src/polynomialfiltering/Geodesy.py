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



class Geodesy(ABC):
    '''
    Geodetic and related coordinate transforms
    '''

    '''@ a : float | Earth major axis [m]'''
    '''@ b : float | Earth minor axis [m]'''
    '''@ f : float | flattening [unitless]'''
    '''@ ecc : float | Earth oblate spheriod primary eccentricity [unitless]'''
    '''@ e2 : float |  [unitless]'''
    '''@ secEcc : float | Earth oblate spheriod secondary eccentricity [unitless]'''
    '''@ secEccSqr : float |  [unitless]'''
    '''@ mu : float | Earth gravitational constant [?]'''
    '''@ omega : float | Earth rotation rate [rad/s]'''
    '''@ J2 : float | Earth 2nd order gravitational spherical harmonic [m]'''
    '''@ J3 : float | Earth 3rd order gravitational spherical harmonic [m]'''
    '''@ J4 : float | Earth 4th order gravitational spherical harmonic [m]'''
    '''@ origin : vector | model center offset'''

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
        self.origin = array([0, 0, 0]);
        
        
    def geodetic2ECEF(self, latitude : float, longitude : float, altitude : float) -> vector:
        '''@ rc : float'''
        '''@ ECEF : array'''
        '''@ E : float'''
        '''@ F : float'''
        '''@ G : float'''
        rc = sqrt( 1 - self.e2 * sin( latitude )**2 )
        rc = self.a / max(1.0e-14, rc )
        E = (rc + altitude) * cos(latitude) * cos(longitude)
        F = (rc + altitude) * cos(latitude) * sin(longitude)
        G = (rc * (1 - self.e2) + altitude) * sin(latitude)
        ECEF = array([E, F, G])
        return ECEF
        
        
