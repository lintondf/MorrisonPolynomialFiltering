'''
Created on Feb 23, 2019

@author: NOOK
'''
import unittest
from TestUtilities import *
from numpy import arange, array2string, cov, zeros, mean, std, var, diag,\
    transpose
from numpy.random import randn
from numpy.testing import assert_almost_equal
from math import sqrt, sin
from runstats import Statistics
from scipy.stats._continuous_distns import chi2

from PolynomialFiltering.Components.FixedMemoryPolynomialFilter import FixedMemoryFilter;



class Test(unittest.TestCase):

    Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);


    def testName(self):
        tau = 0.1;
        N = 25;
        for order in range(2,6): 
            fixed = FixedMemoryFilter(order, 11);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=0.0)
            for i in range(0,12) :
                fixed.add(times[i], observations[i]);
            print(fixed.getState(times[11])-truth[11,:]);
        fixed = FixedMemoryFilter(2, 11);
        (times, truth, observations, noise) = generateTestData(fixed.order, 23, 0.0, self.Y0[0:fixed.order+1], tau, sigma=0.0)
        for i in range(0,12) :
            for j in range(0,12):
                fixed.add(times[i+j], observations[i+j]);
            j = i+11;
            print(fixed.getState(times[j])-truth[j,:]);
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()