''' PolynomialFiltering.PythonUtilities
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

"""***************** DO NOT TRANSPILE THIS MODULE *************************"""
from numpy import exp
from scipy.stats import chi2;

def virtual(funcobj):
    return funcobj;

def chi2Cdf(x : float, df : int) -> float:
    return chi2.cdf(1e-9 + x, df)

def chi2Ppf(p : float, df : int) -> float:
    return 1e-9 + chi2.ppf(p, df );

if __name__ == '__main__':
    print(chi2Cdf(0, 2), chi2Ppf(0, 2))
    for m in range(0,5+1):
        c = chi2Ppf(0.99, m+1);
        print(m, c, exp(chi2Cdf(c,m+1)))