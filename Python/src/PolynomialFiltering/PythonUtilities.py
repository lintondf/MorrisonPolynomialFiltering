''' PolynomialFiltering.PythonUtilities
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

"""***************** DO NOT TRANSPILE THIS MODULE *************************"""
from numpy import exp
from scipy.stats import chi2, f;

def virtual(funcobj):
    return funcobj;

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