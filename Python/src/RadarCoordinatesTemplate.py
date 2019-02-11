'''
Created on Feb 9, 2019

@author: NOOK
'''

from abc import ABC
from numpy import array, zeros
from math import sqrt, sin, cos, atan2, pi

def POW(a, b):
    return a**b;


class RadarCoordinatesTemplate(ABC):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def AER2ENU(self, A, E, R) -> array:
        ENU = zeros([len(A), 3])
        ENU[0, 0] = R[0] * cos(E[0]) * sin(A[0])
        ENU[0, 1] = R[0] * cos(E[0]) * cos(A[0])
        ENU[0, 2] = R[0] * sin(E[0])
        if (len(A) > 1) :
            ENU[1, 0] = self.d1EastdAER1(A, E, R)
            ENU[1, 1] = self.d1NorthdAER1(A, E, R)
            ENU[1, 2] = self.d1UpdAER1(A, E, R)
            if (len(A) > 2) :
                ENU[2, 0] = self.d2EastdAER2(A, E, R)
                ENU[2, 1] = self.d2NorthdAER2(A, E, R)
                ENU[2, 2] = self.d2UpdAER2(A, E, R)
                if (len(A) > 3) :
                    ENU[3, 0] = self.d3EastdAER3(A, E, R)
                    ENU[3, 1] = self.d3NorthdAER3(A, E, R)
                    ENU[3, 2] = self.d3UpdAER3(A, E, R)
                    if (len(A) > 4) :
                        ENU[4, 0] = self.d4EastdAER4(A, E, R)
                        ENU[4, 1] = self.d4NorthdAER4(A, E, R)
                        ENU[4, 2] = self.d4UpdAER4(A, E, R)
                        if (len(A) > 5) :
                            ENU[5, 0] = self.d5EastdAER5(A, E, R)
                            ENU[5, 1] = self.d5NorthdAER5(A, E, R)
                            ENU[5, 2] = self.d5UpdAER5(A, E, R)
        return ENU
    
    def ENU2AER(self, E, N, U) -> array:
        AER = zeros([len(E), 3])
        AER[0, 0] = atan2( E[0], N[0] ) % (2*pi)
        AER[0, 1] = atan2( U[0], sqrt(E[0]**2 + N[0]**2) )
        AER[0, 2] = sqrt(E[0]**2 + N[0]**2 + U[0]**2)
        if (len(E) > 1) :
            AER[1, 0] = self.d1AzimuthdENU1(E, N, U)
            AER[1, 1] = self.d1ElevationdENU1(E, N, U)
            AER[1, 2] = self.d1RangedENU1(E, N, U)
            if (len(E) > 2) :
                AER[2, 0] = self.d2AzimuthdENU2(E, N, U)
                AER[2, 1] = self.d2ElevationdENU2(E, N, U)
                AER[2, 2] = self.d2RangedENU2(E, N, U)
                if (len(E) > 3) :
                    AER[3, 0] = self.d3AzimuthdENU3(E, N, U)
                    AER[3, 1] = self.d3ElevationdENU3(E, N, U)
                    AER[3, 2] = self.d3RangedENU3(E, N, U)
                    if (len(E) > 4) :
                        AER[4, 0] = self.d4AzimuthdENU4(E, N, U)
                        AER[4, 1] = self.d4ElevationdENU4(E, N, U)
                        AER[4, 2] = self.d4RangedENU4(E, N, U)
                        if (len(E) > 5) :
                            AER[5, 0] = self.d5AzimuthdENU5(E, N, U)
                            AER[5, 1] = self.d5ElevationdENU5(E, N, U)
                            AER[5, 2] = self.d5RangedENU5(E, N, U)
        return AER
    
    '''
    public RealMatrix ENU2AER( RealVector E, RealVector N, RealVector U ) {
        RealMatrix AER = new Array2DRowRealMatrix( E.getDimension(), 3 );
        AER.setEntry(0,  0, Math.atan2(N.getEntry(0), E.getEntry(0)));  // azimuth
        AER.setEntry(0,  1, Math.atan2(U.getEntry(0), Math.sqrt(POW(E.getEntry(0),2) + POW(N.getEntry(0),2))));
        AER.setEntry(0,  2, Math.sqrt(POW(E.getEntry(0),2) + POW(N.getEntry(0),2) + POW(U.getEntry(0),2)));
        if (E.getDimension() > 1) {
            AER.setEntry(1, 0, d1AzimuthdENU1(E, N, U));
            AER.setEntry(1, 1, d1ElevationdENU1(E, N, U));
            AER.setEntry(1, 2, d1RangedENU1(E, N, U));
            if (E.getDimension() > 2) {
                AER.setEntry(2, 0, d2AzimuthdENU2(E, N, U));
                AER.setEntry(2, 1, d2ElevationdENU2(E, N, U));
                AER.setEntry(2, 2, d2RangedENU2(E, N, U));
                if (E.getDimension() > 3) {
                    AER.setEntry(3, 0, d3AzimuthdENU3(E, N, U));
                    AER.setEntry(3, 1, d3ElevationdENU3(E, N, U));
                    AER.setEntry(3, 2, d3RangedENU3(E, N, U));
                    if (E.getDimension() > 4) {
                        AER.setEntry(4, 0, d4AzimuthdENU4(E, N, U));
                        AER.setEntry(4, 1, d4ElevationdENU4(E, N, U));
                        AER.setEntry(4, 2, d4RangedENU4(E, N, U));
                        if (E.getDimension() > 5) {
                            AER.setEntry(5, 0, d5AzimuthdENU5(E, N, U));
                            AER.setEntry(5, 1, d5ElevationdENU5(E, N, U));
                            AER.setEntry(5, 2, d5RangedENU5(E, N, U));
                        }
                    }
                }
            }
        }
        return AER;
    }
    
    '''
    def d1AzimuthdENU1(self, E, N, U) -> array:
        pass # {$d1AzimuthdENU1}

    def d2AzimuthdENU2(self, E, N, U) -> array:
        pass # {$d2AzimuthdENU2}

    def d3AzimuthdENU3(self, E, N, U) -> array:
        pass # {$d3AzimuthdENU3}

    def d4AzimuthdENU4(self, E, N, U) -> array:
        pass # {$d4AzimuthdENU4}

    def d5AzimuthdENU5(self, E, N, U) -> array:
        pass # {$d5AzimuthdENU5}

    def d1ElevationdENU1(self, E, N, U) -> array:
        pass # {$d1ElevationdENU1}

    def d2ElevationdENU2(self, E, N, U) -> array:
        pass # {$d2ElevationdENU2}

    def d3ElevationdENU3(self, E, N, U) -> array:
        pass # {$d3ElevationdENU3}

    def d4ElevationdENU4(self, E, N, U) -> array:
        pass # {$d4ElevationdENU4}

    def d5ElevationdENU5(self, E, N, U) -> array:
        pass # {$d5ElevationdENU5}

    def d1RangedENU1(self, E, N, U) -> array:
        pass # {$d1RangedENU1}

    def d2RangedENU2(self, E, N, U) -> array:
        pass # {$d2RangedENU2}

    def d3RangedENU3(self, E, N, U) -> array:
        pass # {$d3RangedENU3}

    def d4RangedENU4(self, E, N, U) -> array:
        pass # {$d4RangedENU4}

    def d5RangedENU5(self, E, N, U) -> array:
        pass # {$d5RangedENU5}

    def d1EastdAER1(self, A, E, R) -> array:
        pass # {$d1EastdAER1}

    def d2EastdAER2(self, A, E, R) -> array:
        pass # {$d2EastdAER2}

    def d3EastdAER3(self, A, E, R) -> array:
        pass # {$d3EastdAER3}

    def d4EastdAER4(self, A, E, R) -> array:
        pass # {$d4EastdAER4}

    def d5EastdAER5(self, A, E, R) -> array:
        pass # {$d5EastdAER5}

    def d1NorthdAER1(self, A, E, R) -> array:
        pass # {$d1NorthdAER1}

    def d2NorthdAER2(self, A, E, R) -> array:
        pass # {$d2NorthdAER2}

    def d3NorthdAER3(self, A, E, R) -> array:
        pass # {$d3NorthdAER3}

    def d4NorthdAER4(self, A, E, R) -> array:
        pass # {$d4NorthdAER4}

    def d5NorthdAER5(self, A, E, R) -> array:
        pass # {$d5NorthdAER5}

    def d1UpdAER1(self, A, E, R) -> array:
        pass # {$d1UpdAER1}

    def d2UpdAER2(self, A, E, R) -> array:
        pass # {$d2UpdAER2}

    def d3UpdAER3(self, A, E, R) -> array:
        pass # {$d3UpdAER3}

    def d4UpdAER4(self, A, E, R) -> array:
        pass # {$d4UpdAER4}

    def d5UpdAER5(self, A, E, R) -> array:
        pass # {$d5UpdAER5}

