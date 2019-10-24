'''
Created on Oct 18, 2019

@author: lintondf
'''
import unittest

import csv
import numpy as np
import random
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose, \
    concatenate, allclose, min, max, nonzero, cumsum, histogram, where, diag, ones
from numpy import array, array as vector, array_equal
from numpy import sqrt
from numpy.linalg import inv
from TestUtilities import assert_allclose, assert_almost_equal, assert_array_less
from scipy.optimize.zeros import brentq
from scipy import stats
from typing import List;

from TestData import TestData
from TestSuite import slow, TestCaseBase
from TestUtilities import generateTestPolynomial, generateTestData, createTestGroup, writeTestVariable, A2S, assert_report, assert_clear
from polynomialfiltering.Main import AbstractFilterWithCovariance, FilterStatus
from polynomialfiltering.Main import StateTransition
from polynomialfiltering.PythonUtilities import assert_not_empty
from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod
from polynomialfiltering.components.Fmp import makeFmp
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.filters.AdaptiveOrderPolynomialFilter import AdaptiveOrderPolynomialFilter
from polynomialfiltering.filters.RecursivePolynomialFilter import RecursivePolynomialFilter
from polynomialfiltering.filters.PairedPolynomialFilter import PairedPolynomialFilter
from numpy.random import randn

import matplotlib.pyplot as plt

import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt
from scipy.sparse.linalg.eigen.arpack._arpack import sseupd
from scipy.optimize import fminbound, minimize
from scipy.sparse.linalg.eigen.arpack.arpack import SSEUPD_ERRORS



# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    DISTRIBUTIONS = [        
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,#st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))
                print(distribution, sse)

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)

def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf

class AdaptiveOrderPolynomialFilter_test(TestCaseBase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def generateOne(self, iter : int, ftarget : int = -1, dtarget : int = -1, verbose : bool = False):
        random.seed(iter)
        np.random.seed(iter)
        t0 = 0
        tau = 0.1
        R = 10.0
        nS = 1000
        theta = 0.95
        for forder in range(1, 5+1) :
            for dorder in range(0, forder+1) : # (2, ) : #
                if (verbose) :
                    print('PASS %4d: DATA ORDER %d; FILTER ORDER %d' % (iter, dorder, forder) )
                p = PairedPolynomialFilter(dorder, tau, theta)
                if (dorder == dtarget and forder == ftarget) :
                    trace = open('AOPF.csv', 'w')
                else :
                    trace = None
                f = AdaptiveOrderPolynomialFilter(forder, tau, theta, trace=trace)
                Y = generateTestPolynomial( dorder, nS, t0, tau )
#                 print(Y)
#                 if ((dorder == 1 and forder == 1)) :
#                     nS *= 10
                (times, truth, observations, noise) = generateTestData(dorder, nS, 0.0, Y[0:dorder+1], tau, sigma=R)
#                 print(noise)
                if (ftarget >= 0 and ftarget != forder):
                    continue
                if (dtarget >= 0 and dtarget != dorder):
                    continue
                if (dorder == dtarget and forder == ftarget and trace != None) :
                    trace.write(A2S(Y,format="%14.8g") + '\n')
                lastBest = 0
                for j in range(0,nS) :
                    Zstar = p.predict(times[j][0])
                    e = observations[j] - Zstar[0]
                    p.update(times[j][0], Zstar, e)
                    Zstar = f.predict(times[j][0])
                    e = observations[j] - Zstar[0]
                    f.update(times[j][0], Zstar, e)
                d = StateTransition.conformState( forder, p.getState() )-f.getState()
                sf = sqrt(d[0]**2 / (R**2*p.getFirstVRF()))
                if (verbose) :
                    print('%6.3f' % p.getTime(), A2S(p.getState()))
                    print('%6.3f' % f.getTime(), A2S(f.getState()))
                    print('%6.3f' % times[-1][0], A2S(d))
                    print('%6.3f, %10.6f' % (times[-1][0], sf) )
                    if (dorder == dtarget and forder == ftarget and trace != None) :
                        trace.write(A2S(f.getTime())+'\n')
                        trace.write(A2S(f.getState(),format="%14.8g")+'\n')
                        trace.write(A2S(p.getState(),format="%14.8g")+'\n')
                elif (sf > 1.0) :
                    if (f.getBest() != dorder) :
                        r = 'WRONG'
                    else :
                        r = 'OK'
                    print( '%5d, %2d, %2d, %2d, %10.6f %s' % (iter, dorder, forder, f.getBest(), sf, r))
                f.close();

    def stepVaryingOrder(self):
        iter = 1
        random.seed(iter)
        np.random.seed(iter)
        print()
        testData = TestData()
        print()
        Times = zeros([1000,1])
        Truth = zeros([1000,5+1])
        i = 0
        with open(testData.testDataPath('varyingorder.csv'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader :
                Times[i,0] = float(row[0])
                for j in range(0,5+1) :
                    Truth[i,j] = float(row[j+1])
                i += 1
                if (i >= Times.shape[0]) :
                    break
        tau = 0.1
        R = 10.0
        nS = Times.shape[0]
        theta = 0.95
        Observations = Truth[:,0:1] + R * randn(nS,1)
        Actual = zeros([1000,5+1])
        Best = zeros([1000,1])
        
        f = PairedPolynomialFilter(5, tau, theta)
        k = 0
        for j in range(0,nS) :
            Zstar = f.predict(Times[j,0])
            e = Observations[j,0] - Zstar[0]
            f.update(Times[j,0], Zstar, e)
            if (f.getStatus() == FilterStatus.RUNNING) :
                Actual[j,:] = f.getState()
            else :
                Actual[j,:] = Truth[j,:]
        sse = np.sum(np.power(Actual[k:,0] - Truth[k:,0], 2.0))
        print(k, '5th Order Only %10.3e' % sse)
#         ax = plt.subplot(3,1,1)
#         ax.plot(Times, Actual[:,0], 'r.')
#         ax.plot(Times, Truth[:,0], 'b-')
#         ax = plt.subplot(3,1,2)
#         ax.plot(Times, (Truth[:,0]-Actual[:,0]), 'b-')
#         ax = plt.subplot(3,1,3)
#         ax.plot(Times, Best, 'k-')
#         plt.show()

        def targetSSE(t : float):
            trace = open('AOPF.csv', 'w')
            f = AdaptiveOrderPolynomialFilter(5, tau, theta, trace=trace)
            f.setSwitchThreshold(t[0])
            f.setRestartThreshold(t[1])
            for j in range(0,nS) :
                Zstar = f.predict(Times[j,0])
                e = Observations[j,0] - Zstar[0]
                f.update(Times[j,0], Zstar, e)
                Actual[j,:] = f.getState()
                Best[j,0] = f.getBest()
            f.close()
            sse = np.sum(np.power(Actual[:,0] - Truth[:,0], 2.0))
            return sse

        if (False) :
            minSSE = 1e100
            minT = []
            for st in arange(2.0, 3.1, 0.05) : #arange(2.0, 10.0, 0.1) : #   # 
                for rt in arange(5.0, 6.0, 0.1) :
                    t = array([st, rt])        
                    sse = targetSSE(t)
                    if (sse < minSSE) :
                        minSSE = sse
                        minT = t
                    print('SSE  %10.6f, %10.6f, %10.3e' % (t[0], t[1], sse))
            print('MINSSE  %10.6f, %10.6f, %10.3e' % (minT[0], minT[1], minSSE))
            sse = targetSSE(minT)
        else :
            minT = [2.5, 6.0]
            minSSE = targetSSE(minT)
            print('SSE  %10.6f, %10.6f, %10.3e' % (minT[0], minT[1], minSSE))
        
        if (False) :
            t = minimize( targetSSE, [2.8, 5.6], method='Nelder-Mead', options={'disp': True})
            print(t)
            sse = targetSSE(t.x)
            print('minimize SSE  %10.6f, %10.6f, %10.3e' % (t.x[0], t.x[1], sse))
            
#         print('ACTUAL:  ', A2S(f.getState()))
#         print('EXPECT:  ', A2S(Truth[-1,:]))
        ax = plt.subplot(3,1,1)
        ax.plot(Times, Actual[:,0], 'r.')
        ax.plot(Times, Truth[:,0], 'b-')
        ax = plt.subplot(3,1,2)
        ax.plot(Times, (Truth[:,0]-Actual[:,0]), 'b-') # /Truth[:,0]
        ax = plt.subplot(3,1,3)
        ax.plot(Times, Best, 'k-')
        plt.show()
    
#     def generateVaryingOrder(self, iter : int):
#         random.seed(iter)
#         np.random.seed(iter)
#         print()
#         t0 = 0
#         tau = 0.1
#         R = 10.0
#         nS = 1000
#         theta = 0.95
#         f = AdaptiveOrderPolynomialFilter(5, tau, theta)
#         Y0 = generateTestPolynomial( 5, nS, t0, tau )
#         print(Y0)
#         Truth = zeros([nS, 5+1])
#         Times = zeros([nS,1])
#         Observations = zeros([nS,1])
#         i = 0
#         Truth[i,0] = Y0[0]
#         k = 100
#         order = 0
#         (times, truth, observations, noise) = generateTestData(order, k, 0.0, Truth[i,:], tau, sigma=R)
#         Times[i:i+k,0] = times[:,0]
#         Truth[i:i+k,0:order+1] = truth[:,0:order+1]
#         Observations[i:i+k,0] = observations[:,0]
#         i += k 
#         
#         def addSegment(i : int, k : int, order1 : int, order2 : int, Times : array, Truth : array, Observations : array):
#             Times[i,:] = Times[i-1,:]
#             Truth[i,0:order2+1] = StateTransition.conformState(order2, Y0)
#             Truth[i,0:order1+1] = Truth[i-1,0:order1+1]
#             (times, truth, observations, noise) = generateTestData(order2, k, Times[i,0], Truth[i,0:order2+1], tau, sigma=R)
#             Times[i:i+k,0] = times[:,0]
#             Truth[i:i+k,0:order2+1] = truth[:,0:order2+1]
#             Observations[i:i+k,0] = observations[:,0]
# #             print(A2S(Truth[i-1:i+1,:]))
# #             print(A2S(Truth[i+k-1:i+k+1,:]))
#             return i + k
#         
#         i = addSegment(i, 500, 0, 5, Times, Truth, Observations)
#         i = addSegment(i, 100, 5, 2, Times, Truth, Observations)
#         i = addSegment(i, 100, 1, 2, Times, Truth, Observations)
#         nS = addSegment(i, 200, 2, 4, Times, Truth, Observations)
#         
#         trace = open('AOPF.csv', 'w')
#         f = AdaptiveOrderPolynomialFilter(5, tau, theta, trace=trace)
#         for j in range(0,nS) :
#             Zstar = f.predict(Times[j][0])
#             e = Observations[j] - Zstar[0]
#             f.update(Times[j][0], Zstar, e)
#         print('ACTUAL:  ', A2S(f.getState()))
#         print('EXPECT:  ', A2S(Truth[-1,:]))
#         f.close()

    def xstep0Generate(self):
        """
        """
        print()
#         self.generateOne(132, 1, 1, verbose=True)
#         for i in range(0,1000) :
#             self.generateOne(i)
            
    def xstepSmoothedSSR(self):
        print()
        R = 10.0
        for R in (1,1,1,1) : # (1.0, 2.0, 5.0, 10.0) : # i in range(0,1) :
            X = R * randn(1000,1)
#             Y = np.multiply(X,X)
            Y = X.copy()
            y, x = np.histogram(Y, bins=200, density=True)
            x = (x + np.roll(x, -1))[:-1] / 2.0
            
            chiY = stats.chi2.fit(Y,floc=0,fscale=1)
            # Separate parts of parameters
            arg = chiY[:-2]
            loc = chiY[-2]
            scale = chiY[-1]

            # Calculate fitted PDF and error with fit in distribution
            pdf = stats.chi2.pdf(x, loc=loc, scale=scale, *arg)
            sse = np.sum(np.power(y - pdf, 2.0))
            print(R, chiY, sse)
#             ax = plt.subplot(1,1,1)
#             ax.hist(Y, density=True, bins=100)
#             ax.plot(x, y, 'm.')
#             ax.plot(x,pdf, 'y-')
#             plt.show()
            
#             print(R, chiY, sse)
            print('Y', mean(Y), var(Y), 2*R**4)
#             for theta in range(1,10) :
#                 theta = 1.0 - 0.01*theta
            for theta in (0.95,) : #  (0.6, 0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 0.999) :
                f = PairedPolynomialFilter(0, 1.0, theta) # makeFmp(0, 1.0, theta)
                f.start(0,array([0*R**2]))
                for i in range(0,len(Y)) :
                    f.add(i, Y[i])
                    X[i] = f.getState()**2
                n = X.shape[0]
                print('X',  mean(X), var(X), f.getFirstVRF())
                y, x = np.histogram(X, bins=25, density=True)
                dist = stats.chi2
                chiX = dist.fit(X) # ,floc=0, fscale=R*sqrt(f.getFirstVRF())) # floc=R**2, fscale=sqrt(2.0*R**4*f.getFirstVRF()) )
                x = (x + np.roll(x, -1))[:-1] / 2.0
                arg = chiX[:-2]
                loc = chiX[-2]
                scale = chiX[-1]
#                 print(arg, loc, scale)
#                 print(R, theta, arg[0])
    
                # Calculate fitted PDF and error with fit in distribution
                pdf = dist.pdf(x, loc=loc, scale=scale, *arg)
                cdf = dist.cdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))
                print(theta, chiX, sse)
                ax = plt.subplot(1,1,1)
#                 ax.plot(range(0,1000), Y, 'k.')
#                 ax.plot(range(0,1000), X, 'b.')
                ax.hist(X, density=True, bins=100, color='red')
#                 ax.plot(x, y, 'ko')
#                 ax.plot(x,pdf, 'b-')
                plt.show()
#         print(stats.chi2.fit((X-mean(X))/sqrt(var(X))))
#         print(mean(X),sqrt(var(X)))
#         print(mean(Y),var(Y), var(Y)/var(X), 1/(0.05/1.95))
#         ax.hist(Y, density=True, histtype='stepfilled', color='red', alpha=0.2, bins=25)
#         ax.hist(X, density=True, histtype='stepfilled', alpha=0.2, bins=25)
#         plt.show()
#         
    def stepDebug(self):
        t0 = 0
        R = 10
        print()
        for p in range(1,7) :
            print(p,stats.chi2.isf(10**-p, 1)**(1/2))
#         print(R**2, R**2 * 0.05/1.95, (R**2 * 0.05/1.95)**2)
#         print(stats.chi2.isf(0.05, 1), stats.chi2.isf(0.05, 1, loc=R**2, scale=sqrt(2.0*R**4/(0.05/1.95))))
#         print(stats.chi2.isf(sqrt(0.05), 1), stats.chi2.isf(sqrt(0.05), 1, loc=R**2, scale=sqrt(2.0*R**4/(0.05/1.95))))
#         for p in (0.05, 0.01, 0.001, 1e-4) :
#             print(p, stats.f.isf(p, 1, 1))
#             print(sqrt(p), stats.f.isf(sqrt(p), 1, 1))
#         print(stats.f.isf(0.05, 2, 2))
#         print(stats.f.isf(0.01, 2, 2))
#         print(stats.f.isf(0.001, 2, 2))
#         print(stats.f.isf(1e-6, 2, 2))
        
#         print(stats.chi2.isf(0.05, 1))
#         print(stats.chi2.isf(0.01, 1))
#         print(stats.chi2.isf(1e-6, 1))
#         print(stats.chi2.isf(sqrt(0.05), 1))
#         print(stats.chi2.isf(sqrt(0.01), 1))
#         print(stats.chi2.isf(sqrt(1e-6), 1))
#         print(stats.chi2.isf(0.05, 2))
#         print(stats.chi2.isf(0.01, 2))
#         print(stats.chi2.isf(1e-6, 2))
#         print(stats.chi2.isf(sqrt(0.05), 2))
#         print(stats.chi2.isf(sqrt(0.01), 2))
#         print(stats.chi2.isf(sqrt(1e-6), 2))
        
        if (False) : 
            print("self.fthresholds = array([")
            for i in range(0,5+1) :
                print('[',end='')
                for j in range(0,5+1) :
                    if (j > 0) :
                        print(", ", end='')
                    print('%10g' % (stats.f.isf(0.05, i+1, j+1)),end='')
                print('],')
            print("])")
#         tau = 0.1
#         R = 10.0
#         nS = 100
#         theta = 0.9375
#         for forder in range(0,5+1) :
#             f = makeFmp(forder, tau, theta) # AdaptiveOrderPolynomialFilter(forder, tau, theta)
#             for i in range(0,100) :
#                 Z = f.predict(i*tau)
#                 f.update(i*tau, Z, 0.0)
#                 
#             print(forder, f.getFirstVRF())

    def xstepFit(self):
        matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
        X = 1.0 * randn(1000,1)
        data = np.multiply(X,X)
        
        # Plot for comparison
        ax = plt.subplot(1,1,1)
        ax.hist(data, bins=50, density=True, alpha=0.5, color='blue')
        # Save plot limits
        dataYLim = ax.get_ylim()
        
        # Find best fit distribution
        best_fit_name, best_fit_params = best_fit_distribution(data, 200, ax)
        best_dist = getattr(st, best_fit_name)
        print(best_fit_name)
        
        # Update plots
        ax.set_ylim(dataYLim)
        
        # Make PDF with best params 
        pdf = make_pdf(best_dist, best_fit_params)
        
#         # Display
#         plt.figure(figsize=(12,8))
#         ax = pdf.plot(lw=2, label='PDF', legend=True)
#         data.plot(kind='hist', bins=50, normed=True, alpha=0.5, label='Data', legend=True, ax=ax)
#         
#         param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
#         param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
#         dist_str = '{}({})'.format(best_fit_name, param_str)
#         
#         ax.set_title(u'El Niño sea temp. with best fit distribution \n' + dist_str)
#         ax.set_xlabel(u'Temp. (°C)')
#         ax.set_ylabel('Frequency')
#         plt.show()
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()