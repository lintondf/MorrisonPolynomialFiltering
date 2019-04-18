'''
Created on Mar 4, 2019

@author: NOOK
'''

from netCDF4 import Dataset
from numpy import array, dtype, empty, zeros
from numpy.random import randn

if __name__ == '__main__':
    rootgrp = Dataset("test.nc", "w", format="NETCDF4");
    name = 'FixedMemoryFilter';
    fMF = rootgrp.createGroup(name);
    test1 = fMF.createGroup('test1');
    N = 25;
    test1.createDimension('N', N);
    test1.createDimension('mInitialize', 12);
    v = test1.createVariable('initialize', 'd', ('N', 'mInitialize'))
    v[:] = zeros([N, 12]);
    rootgrp.close();