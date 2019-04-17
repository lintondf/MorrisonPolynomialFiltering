'''
Created on Apr 12, 2019

@author: NOOK
'''

from polynomialfiltering.PythonUtilities import constructor, ignore

from numpy import array, isscalar
from numpy import array as vector
from numpy.linalg import inv
from polynomialfiltering.Main import AbstractFilterWithCovariance
from polynomialfiltering.filters.controls.IObservationErrorModel import IObservationErrorModel

class EmpiricalObservationErrorModel(IObservationErrorModel):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        