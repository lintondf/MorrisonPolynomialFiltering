'''
Created on Mar 21, 2019

@author: linto
'''
from numpy import eye, array, arange, trace
from numpy import array as vector
from numpy.linalg.linalg import det, inv

from TestUtilities import correlationToCovariance

import numpy as np
from numpy import eye, array, cos, sin, radians, zeros, transpose, concatenate, cov, sqrt, diag
from numpy import array as vector
from numpy.linalg.linalg import det, inv, cholesky

from filterpy.kalman.sigma_points import MerweScaledSigmaPoints
from filterpy.kalman.sigma_points import JulierSigmaPoints

from TestUtilities import correlationToCovariance, covarianceToCorrelation

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from math import atan2, degrees, pi
from scipy.optimize.optimize import fminbound
from scipy.optimize import minimize_scalar
from scipy.stats import random_correlation
from numpy.matlib import rand
from sobel_seq import i4_sobol_generate, i4_sobol_generate_std_normal

def plot_point_cov(points, nstd=2, ax=None, **kwargs):
    """
    Plots an `nstd` sigma ellipse based on the mean and covariance of a point
    "cloud" (points, an Nx2 array).
    Parameters
    ----------
        points : An Nx2 array of the data points.
        nstd : The radius of the ellipse in numbers of standard deviations.
            Defaults to 2 standard deviations.
        ax : The axis that the ellipse will be plotted on. Defaults to the 
            current axis.
        Additional keyword arguments are pass on to the ellipse patch.
    Returns
    -------
        A matplotlib ellipse artist
    """
    pos = points.mean(axis=0)
    cov = np.cov(points, rowvar=False)
    return plot_cov_ellipse(cov, pos, nstd, ax, **kwargs)

def covariance2Ellipse(cov : array, nstd : float = 1.0):
    def eigsorted(cov):
        vals, vecs = np.linalg.eigh(cov)
        order = vals.argsort()[::-1]
        return vals[order], vecs[:,order]

    vals, vecs = eigsorted(cov)
    theta = (np.arctan2(*vecs[:,0][::-1]))

    # Width and height are "full" widths, not radius
    width, height = 2 * nstd * np.sqrt(vals)
    return (width, height, theta )

def plot_cov_ellipse(cov, pos, nstd=2, ax=None, **kwargs):
    """
    Plots an `nstd` sigma error ellipse based on the specified covariance
    matrix (`cov`). Additional keyword arguments are passed on to the 
    ellipse patch artist.
    Parameters
    ----------
        cov : The 2x2 covariance matrix to base the ellipse on
        pos : The location of the center of the ellipse. Expects a 2-element
            sequence of [x0, y0].
        nstd : The radius of the ellipse in numbers of standard deviations.
            Defaults to 2 standard deviations.
        ax : The axis that the ellipse will be plotted on. Defaults to the 
            current axis.
        Additional keyword arguments are pass on to the ellipse patch.
    Returns
    -------
        A matplotlib ellipse artist
    """
    if ax is None:
        ax = plt.gca()

    (width, height, theta) = covariance2Ellipse(cov, nstd)
    ellip = Ellipse(xy=pos, width=width, height=height, angle=np.degrees(theta), **kwargs)
    ellip.set_facecolor('none')
    ax.add_artist(ellip)
    return ellip

def ellipse2Covariance(majorAxis : float, minorAxis : float, phi : float ) -> array:
    '''
    https://stackoverflow.com/questions/41807958/convert-position-confidence-ellipse-to-covariance-matrix
    '''
    C = zeros([2,2])
    C[0,0] = majorAxis**2 * cos(phi)**2 + minorAxis**2 * sin(phi)**2
    C[1,1] = majorAxis**2 * sin(phi)**2 + minorAxis**2 * cos(phi)**2
    C[1,0] = (majorAxis**2 - minorAxis**2) * sin(phi) * cos(phi)
    C[0,1] = C[1,0]     
    return C

def randomCovariance():
    x = random_correlation.rvs((0.8, 1.2));
    D = diag(diag(1 + 10*rand(2,2)))
    return D @ x @ D
    
def oneRatio( X : array, iCs, siC ) -> float:
    maxDenom = 0
    for i in range(0,len(iCs)) :
        t = (X) @ iCs[i] @ transpose(X)
        maxDenom = max(t, maxDenom)
    r = (X) @ siC @ transpose(X)
    return r/maxDenom

def find(X : array, iCs, siC):
    minR = 1E100;
    maxR = 1E-100;
    jMin = 0
    jMax = 0
    maxDenom = zeros([X.shape[0]])
    for j in range(0,X.shape[0]) :
        for i in range(0,len(iCs)) :
            t = transpose(X[j,:]) @ iCs[i] @ (X[j,:])
#                 print(j, i, t, iCs[i].flatten())
            maxDenom[j] = max(t, maxDenom[j])
    for j in range(0,X.shape[0]) :
        r = transpose(X[j,:]) @ siC @ (X[j,:])
#             print(j, X[j,:], maxDenom, r)
        r /= maxDenom[j]
        if (r < minR) :
            jMin = j
        minR = min(r, minR)
        if (r > maxR) :
            jMax = j
        maxR = max(r, maxR)
    plt.plot(X[jMin,0], X[jMin,1], 'b.')
    plt.plot(X[jMax,0], X[jMax,1], 'r.')
#         print('min', minR, X[jMin,:])
#         print('max', maxR, X[jMax,:])
    return (minR, maxR)

def sampledCI( P0 : array, minR : float, maxR : float, u : float = 0.5):
    Psci = P0 / (u*minR + (1-u)*maxR)
#         plot_cov_ellipse(Psci, [0,0], nstd=1, alpha=0.5, color='red', ax=ax)
    return Psci

def once(ax = None):
    Cs = []
    iCs = []
    cCs = []
#     for phi in (0, 39, 75) : # range(0, 180, 60 ) :
#         C = ellipse2Covariance(4, 2, radians(phi))
    XLimit = 0
    YLimit = 0
    for i in range(0,4) :
        C = randomCovariance()
        print('C%d' % i, C.flatten(), covariance2Ellipse(C, 1.0))
        XLimit = max(XLimit, sqrt(C[0,0]))
        YLimit = max(YLimit, sqrt(C[1,1]))
        Cs.append(C)
#         print(inv(C).flatten())
        iCs.append(inv(C))
#     C = array([[1, 0],[0, 100]])
#     Cs.append(C)
#     print(inv(C).flatten())
#     iCs.append(inv(C))
#     cCs.append(cholesky(C))
#     C = array([[100, 0],[0, 1]])
#     Cs.append(C)
#     print(inv(C).flatten())
#     iCs.append(inv(C))
#     cCs.append(cholesky(C))
    
#         cCs.append(cholesky(C))
#         K, D = covarianceToCorrelation(C)
#         print(D)
#         print(K)
#         cov = correlationToCovariance( K, D )
        if (ax != None) :
            plot_cov_ellipse(C, [0,0], nstd=1, alpha=0.5, color='green', ax=ax)
    siC = iCs[0].copy()
    print(0,siC.flatten())
    for i in range(1,len(iCs)) :
        siC += iCs[i]
    P0 = inv(siC)
    print('siC', siC.flatten())
    print('P0', P0.flatten(), covariance2Ellipse(P0, 1.0))
    if (ax != None) :
        plot_cov_ellipse(P0, [0,0], nstd=1, alpha=0.5, color='blue', ax=ax)
    
   ### the axis along which the maximum ratio is found does not bear a
    # simple relationship with the input covar axes or the composite axes
    if (False) :
    #     for sp in (MerweScaledSigmaPoints(2, 1e-3, 2, 1),) :
    #         Y = zeros([0,2])
    #         y = sp.sigma_points(array([0,0]), P0)
    #         Y = concatenate([Y, y[1:,:]])
    #         (minR, maxR) = find(Y)
    #         print(Y.shape[0],minR, maxR)
    #         for u in (0, 0.5, 1) :
    #             print('SPCI', u, sampledCI(P0, minR, maxR, u).flatten())
#         for sp in (MerweScaledSigmaPoints(2, 1e-1, 2, 1),) : # (JulierSigmaPoints(2), ) : # 
        Y = zeros([0,2])
### multiple sigma point sets
#         for k in (1e-3,1e-2,1e-1,1,10) :
#             sp = MerweScaledSigmaPoints(2, k, 2, 1)
#             y = sp.sigma_points(array([0,0]), P0)
#             Y = concatenate([Y, y[1:,:]])
### spiral points
#         a = sqrt(sum(diag(P0)))
#         print(a)
#         a /= 16
#         for theta in range(1,4*360,30) :
#             rt = radians(theta)
#             r = rt * a
#             y = array([[r*cos(rt), r*sin(rt)]])
#             Y = concatenate([Y, y])
## any point along MC max or min ray yields same result
## only mod(90) rotations yield same results
        y0 = array([[-1.01524460e-04,  6.63671562e-01],[-0.27046941, -0.11319619]])
        print( degrees(atan2(y0[1,0], y0[1,1])))
#         Y = concatenate([Y, y0])
        def targetMaxY0(rk : float) -> float :
            M = array([[cos(rk), -sin(rk)],[sin(rk), cos(rk)]])
            y = M @ y0
            return -oneRatio(y[1,:], iCs, siC)
        
        rk = fminbound( targetMaxY0, radians(-1), radians(1))
        M = array([[cos(rk), -sin(rk)],[sin(rk), cos(rk)]])
        y = M @ y0
        Y = concatenate([Y, y])
        print( degrees(atan2(y[1,0], y[1,1])))
        print(degrees(rk), y[0,:], oneRatio(y[0,:], iCs, siC))
        print(degrees(rk), y[1,:], oneRatio(y[1,:], iCs, siC))
        rk = atan2(y[1,0], y[1,1])
        M = array([[cos(rk), -sin(rk)],[sin(rk), cos(rk)]])
#         for y0 in ([1,0],[-1,0],[0,-1],[0,1])  :
#             y = M @ y0
#             print(y0, degrees(atan2(y[0], y[1])), oneRatio(y))
            
#         for k in range(0,90,10) :
#             rk = radians(k)
#             M = array([[cos(rk), -sin(rk)],[sin(rk), cos(rk)]])
#             y = M @ [1,0]
#             print(k, oneRatio(y))
        def targetMaxUnit(rk : float) -> float :
            M = array([[cos(rk), -sin(rk)],[sin(rk), cos(rk)]])
            y = M @ [1,0]
            return -oneRatio(y, iCs, siC)
        
        rk = fminbound( targetMaxUnit, radians(0), radians(90))
        M = array([[cos(rk), -sin(rk)],[sin(rk), cos(rk)]])
        y = M @ [1,0]
        print(y, degrees(atan2(y[0], y[1])), oneRatio(y, iCs, siC))
        (minR, maxR) = find(Y, iCs, siC)
        print(Y.shape[0],minR, maxR)
#         plt.plot(Y[:,0], Y[:,1], 'g+')
        for u in (0.5,) :
            print('SPCI', u, sampledCI(P0, minR, maxR, u).flatten())
    #     for sp in (MerweScaledSigmaPoints(2, 1e-3, 2, 1),) :
    #         Y = zeros([0,2])
    #         for c in Cs :
    #             y = sp.sigma_points(array([0,0]), c)
    #             Y = concatenate([Y, y[1:,:]])
    #         y = sp.sigma_points(array([0,0]), P0)
    #         Y = concatenate([Y, y[1:,:]])
    #         (minR, maxR) = find(Y)
    #         print(Y.shape[0],minR, maxR)
    #         for u in (0, 0.5, 1) :
    #             print('SPCI', u, sampledCI(P0, minR, maxR, u).flatten())
    ## Adding P0 sigma points does not change anything
    #     Y = zeros([0,2])
    #     y = sp.sigma_points(array([0,0]), P0)
    #     Y = concatenate([Y, y[1:,:]])
    #     (minR, maxR) = find(Y)
    #     print(Y.shape[0],minR, maxR)
    # #     print(sampledCI(P0, minR, maxR, 0).flatten())
    #     print(sampledCI(P0, minR, maxR, 0.5).flatten())
    # #     print(sampledCI(P0, minR, maxR, 1).flatten())
    
    #     Y = array([[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]])
    #     (minR, maxR) = find(Y)
    #     print(Y.shape[0],minR, maxR)
    #     print(sampledCI(P0, minR, maxR, 0.5).flatten())
    if (True) :
        for N in (200, 10000,) : # (100, 1000, 10000, 100000) : 
            X = np.random.multivariate_normal(
                    mean=(0,0), cov=P0, size=N
                    )
    #         print(N, X.shape)
            (minR, maxR) = find(X, iCs, siC)
    #         print(X)
            print(X.shape[0],minR, maxR)
            for u in (0.5, ) :
                P = sampledCI(P0, minR, maxR, u)
                print('SCI', u, P.flatten(), covariance2Ellipse(P, 1))
#         def targetU( u : float) :
#             d = trace(sampledCI(P0, minR, maxR, u))
#             return d
#         
#         u = fminbound(targetU, 0, 1)
#         Pstar = sampledCI(P0, minR, maxR, u)
#         print('SCI*', u, Pstar.flatten(), covariance2Ellipse(Pstar, 1))
#         if (ax != None) :
#             plot_cov_ellipse(Pstar, [0,0], nstd=1, alpha=0.5, color='red', ax=ax)
    #     exit(0)
    if (False) :
        X = i4_sobol_generate_std_normal(2, 100)
        X = X[1:,:]
        (minR, maxR) = find(X, iCs, siC)
#         print(X)
        print(X.shape[0],minR, maxR)
        for u in (0.5, ) :
            P = sampledCI(P0, minR, maxR, u)
            print('SSCI', u, P.flatten(), covariance2Ellipse(P, 1))
    if (False):
        t = radians(arange(0,180,4))
        X = zeros([t.shape[0], 2])
        X[:,0] = cos(t);
        X[:,1] = sin(t);
        (minR, maxR) = find(X, iCs, siC)
#         print(X)
        print(X.shape[0],minR, maxR)
        for u in (0.5, ) :
            P = sampledCI(P0, minR, maxR, u)
            print('RCI', u, P.flatten(), covariance2Ellipse(P, 1))
            
        for i in range(0,X.shape[0]) :
            print(t[i], oneRatio(X[i,:], iCs, siC))
        
    if (False) : # works great in 2D but how would I do it in 6D?
        def targetMinUnit(t : float) -> float :
            y = array([cos(t), sin(t)])
            return oneRatio(y, iCs, siC)
        
        def targetMaxUnit(t : float) -> float :
            y = array([cos(t), sin(t)])
            return -oneRatio(y, iCs, siC)

#         tl = 0
#         tu = pi/2
#         minR = 1E300
#         for i in range(0,10) :
#             rl = oneRatio(tl, iCs, siC)
#             ru = oneRatio(tu, iCs, siC)
        options={'xatol': 1e-03, 'maxiter': 150, 'disp': 0}
        tmin = minimize_scalar(targetMinUnit, bounds=[0, pi/2], method='Bounded', options=options)
        minR = oneRatio(array([cos(tmin.x), sin(tmin.x)]), iCs, siC )
        tmax = minimize_scalar(targetMaxUnit, bounds=[0, pi/2], method='Bounded', options=options)
        maxR = oneRatio(array([cos(tmax.x), sin(tmax.x)]), iCs, siC )
        P = sampledCI(P0, minR, maxR, 0.5)
        print('BCI', tmin.nfev+tmax.nfev, P.flatten(), covariance2Ellipse(P, 1))
        
#     u = 0
#     Psci = P0 / (u*minR + (1-u)*maxR)
#     print(Psci)
#     plot_cov_ellipse(Psci, [0,0], nstd=1, alpha=0.5, color='red')
#     u = 0.5
#     Psci = P0 / (u*minR + (1-u)*maxR)
#     print(Psci)
#     plot_cov_ellipse(Psci, [0,0], nstd=1, alpha=0.5, color='yellow')
#     u = 1
#     Psci = P0 / (u*minR + (1-u)*maxR)
#     print(Psci)
#     plot_cov_ellipse(Psci, [0,0], nstd=1, alpha=0.5, color='cyan')
    return (XLimit, YLimit)
    
if __name__ == '__main__':
    ax = None
#     f0 = plt.figure(figsize=(10, 6))
#     ax = plt.subplot(111)
    (XLimit, YLimit) = once(ax)
    if (False) :
        plt.plot(0,0, 'k+')
        plt.xlim(-XLimit, XLimit)
        plt.ylim(-YLimit, YLimit)
        plt.show()
   
    