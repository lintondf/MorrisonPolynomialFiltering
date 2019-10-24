''' PolynomialFiltering.filters.controls.SimpleAnalyticRadarErrorModel
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''
from polynomialfiltering.PythonUtilities import constructor, ignore, List

from numpy import array, isscalar, copy, sin, cos, tan, pi, zeros
from numpy import array as vector
from numpy.linalg import inv
from polynomialfiltering.Main import AbstractFilterWithCovariance
from polynomialfiltering.filters.controls.IObservationErrorModel import IObservationErrorModel


class SimpleAnalyticRadarErrorModel(IObservationErrorModel):
    """
    This model is an example of an analytically-based radar error model
    Radar must measure azimuth, elevation, and range.  The associated filter must
    generate AER state vectors of size 3*i, i>=1
    """
    '''@ t : float | time of most recent observation'''
    '''@ R : array | observation covariance matrix'''
    '''@ iR : array | observation precision (inverse covariance) matrix'''
    '''@ name : str | radar name'''
    '''@ rCoef : List[float] | range-coefficients (see setRangeCoefficients)'''
    '''@ aCoef : List[float] | azimuth-coefficients (see setAzimuthCoefficients)'''
    '''@ eCoef : List[float] | elevation-coefficients (see setElevationCoefficients)'''
    
    def __init__(self, name : str ):
        self.t = 4E-324
        self.name = name
        self.rCoef = List()
        self.aCoef = List()
        self.eCoef = List()
        self.setRangeCoefficients(0.3048*20, 5E-7, 1E-5, 5E-4, 0.3048*0.1)
        self.setAzimuthCoefficients(5E-5, 0.003001, 0.06, 2E-5, 4E-5)
        self.setElevationCoefficients(5E-5, 0.003001, 0.06, 2E-5, 4E-5)
        
    def setRangeCoefficients(self, zeroSet : float, scaleFactor : float, rateFactor : float, accelerationFactor : float, refractionFactor : float) -> None:
        self.rCoef = List()
        self.rCoef.append(zeroSet)
        self.rCoef.append(scaleFactor)
        self.rCoef.append(rateFactor)
        self.rCoef.append(accelerationFactor)
        self.rCoef.append(refractionFactor)
        
    def setAzimuthCoefficients(self, zeroSet : float, rateFactor : float, accelerationFactor : float, nonOrthoFactor : float, collimationFactor) -> None:
        self.aCoef = List()
        self.aCoef.append(zeroSet)
        self.aCoef.append(rateFactor)
        self.aCoef.append(accelerationFactor)
        self.aCoef.append(nonOrthoFactor)
        self.aCoef.append(collimationFactor)
        
    def setElevationCoefficients(self, zeroSet : float, rateFactor : float, accelerationFactor : float, refractionFactor : float, droopFactor) -> None:
        self.eCoef = List()
        self.eCoef.append(zeroSet)
        self.eCoef.append(rateFactor)
        self.eCoef.append(accelerationFactor)
        self.eCoef.append(refractionFactor)
        self.eCoef.append(droopFactor)
        

    def getPrecisionMatrix(self, f: AbstractFilterWithCovariance, t:float, y:vector) -> array:
        '''@ P : array'''
        if (self.t == t) :
            return self.iR;
        self.t = t;
        P = self.getCovarianceMatrix(f, t, y)
        return self.iR

    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector) -> array:
        '''@ sigmaR : float'''
        '''@ sigmaA : float'''
        '''@ sigmaE : float'''
        '''@ Z : vector | A,E,R,[A-dot,E-dot,R-dot,[A-dot2,E-dot2,R-dot2]] [m,m/s,m/s2]'''
        '''@ P : array'''
        if (self.t == t) :
            return self.R;
        self.t = t
        Z = f.getState() # AER: values, {1st-derivs, {2nd-derives}}
        sigmaR = self.rCoef[0] + self.rCoef[1]*Z[2]
        sigmaA = self.aCoef[0] + self.aCoef[3]*tan(Z[1])
        sigmaE = self.eCoef[0] + self.eCoef[4]*cos(Z[1])
        if (abs(Z[1] - pi/2) < 1e-6) :
            sigmaA += self.aCoef[4]/cos(Z[1])
        if (Z[1] > 1e-6) :
            sigmaR += self.rCoef[4]/sin(Z[1])
            sigmaE += self.eCoef[3]/tan(Z[1])
        if (len(Z) > 3) :
            sigmaR += self.rCoef[2]*Z[2+3*1] 
            sigmaA += self.aCoef[2]*Z[0+3*1]
            sigmaE += self.eCoef[2]*Z[1+3*1]
            if (len(Z) > 6) :
                sigmaR += self.rCoef[3]*Z[2+3*2] 
                sigmaA += self.aCoef[3]*Z[0+3*2]                    
                sigmaE += self.eCoef[3]*Z[1+3*2]
        self.R = zeros([3,3])
        self.R[0,0] = sigmaA**2
        self.R[1,1] = sigmaE**2
        self.R[2,2] = sigmaR**2
        self.iR = zeros([3,3])
        self.iR[0,0] = 1/self.R[0,0]
        self.iR[1,1] = 1/self.R[1,1]
        self.iR[2,2] = 1/self.R[2,2]
        return self.R; 

