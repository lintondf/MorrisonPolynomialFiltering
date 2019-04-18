''' PolynomialFiltering.PythonUtilities
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

"""***************** DO NOT TRANSPILE THIS MODULE *************************"""
from numpy import exp
from scipy.stats import chi2, f;
from typing import List;



'''********************************************************************
LcdPython Decorators
'''
def virtual(funcobj):
    '''
    @virtual marks a function as virtual.
    
    Some in target languages only explicitly marked function can be overloaded
    '''
    return funcobj;

def constructor(funcobj):
    '''
    @constructor marks a function as a class constructor
    '''
    return funcobj;

def ignore(funcobj):
    '''
    Function marked @ignore are not transpiled
    '''
    return funcobj;

def testcase(funcobj):
    '''
    Function marked @testcase are transpiled into the test template when in test generation mode
    '''
    return funcobj;


def assert_not_empty(list : List[str ]) -> None:
    assert( len(list) > 0);


'''********************************************************************
Utility functions for transpiled code; 
'''

def chi2Cdf(x : float, df : int) -> float:
    return chi2.cdf(1e-9 + x, df)

def chi2Ppf(p : float, df : int) -> float:
    return 1e-9 + chi2.ppf(p, df );

def fdistCdf(x : float, df1 : int, df2 : int) -> float:
    return f.cdf(1e-9 + x, df1, df2)

def fdistPpf(p : float, df1 : int, df2 : int) -> float:
    return 1e-9 + f.ppf(p, df1, df2)



if __name__ == '__main__':
    pass
    print(chi2Cdf(6.64, 1), chi2Cdf(2*4.61, 2), chi2Cdf(3*3.78, 3), chi2Cdf(4*3.32, 4), chi2Cdf(10*2.32, 10))
    for i in range(1,21) :
        print(i, chi2Ppf(0.99, i)/i)
#     print(chi2Cdf(3, 2), chi2Ppf(0.95, 2))
#     for m in range(0,5+1):
#         c = chi2Ppf(0.99, m+1);
#         print(m, c, exp(chi2Cdf(c,m+1)))