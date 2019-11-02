'''
Created on Feb 12, 2019

@author: NOOK
'''

import numpy as np
from math import sqrt
from numpy import mean, var, sum, zeros
from numpy_ringbuffer import RingBuffer

import ThinkDSP

class MidpointSmoother :
    '''@W : array'''
    def __init__(self, N : int = 11):
        self.i = 0;
        self.n = 0;
        self.N = N;
        self.samples = zeros([N]);
        self.W = zeros([N]);

    def _setWeights(self, n : int, N : int):
        self.W = zeros([N]);
        for k in range(-n, 1+n) :
            self.W[k+n] = 3.0*((3.0*N**2-7.0)-20.0*k**2)/(4.0*N*(N**2-4.0))
        
    def update(self, x : float ) :
        self.samples[self.i] = x;
        self.i = (self.i + 1) % self.N;
        self.n += 1;
        if (self.n < self.N and self.n >= 3) :
            self._setWeights(self.n/2, self.n)
            return True;
        return self.n >= 3;
    
    def getResidual(self) -> float:
        if (self.n < 3) :
            return 0.0;
        offset = (self.i + 1) % self.N;
        p = 0.0
        for i in range(0,self.N) :
            p += self.W[i] * self.samples[(offset+i) % self.N];
        return self.samples[(offset+1+self.N/2) % self.N] - p;
    
     
class RingStatistics:
    def __init__(self, samples=51):
        self.residuals = RingBuffer(capacity=samples, dtype=np.double)
        self.fmean = None;
        self.fvariance = None;
        
    def getLength(self):
        return len(self.residuals)

    def getMean(self):
        return self.fmean;
    
    def getVariance(self):
        return self.fvariance;
    
    def getSerialCorrelation(self):
        fserialCorrelation = 0.0;
        it = np.nditer(self.residuals);
        pr = None;
        n = 0;
        for r in it :
            if n > 0 :
                fserialCorrelation += (r - self.fmean) * (pr - self.fmean) / self.fvariance;
            n += 1;
            pr = r;
        if n > 1 :
            fserialCorrelation /= n - 1;
        return fserialCorrelation;
    
    def update(self, e):
        self.residuals.appendleft(e);
        self.fmean = np.mean(self.residuals);
        self.fvariance = np.var(self.residuals);
    
class FadingStatistics:
    
    def __init__(self, theta=0.95):
        self.alpha = 1-theta
        
        self.n = 0;
        self.eLast = None;
        self.fmean = 0;
        self.fvariance = 0;
        self.fserialCorrelation = 0;
        
    def getMean(self):
        if (self.n == 0) :
            return None;
        return self.fmean;
    
    def getVariance(self):
        if (self.n < 2) :
            return None;
        return self.fvariance;
    
    def getSerialCorrelation(self):
        if (self.n < 2) :
            return None;
        return self.fserialCorrelation;
    
    def update(self, e):
        if (self.n == 0) :
            self.fmean = e;
            self.fvariance = e*e;
        elif (self.n == 1) :
            self.fmean += self.alpha * (e - self.fmean);
            self.fvariance += self.alpha * (e*e - self.fvariance);            
        else :
            self.fmean += self.alpha * (e - self.fmean);
            self.fvariance += self.alpha * (e*e - self.fvariance);
            var1 = self.getVariance();
            mean1 = self.getMean();
            s1 = (e - mean1);
            s0 = (self.eLast - mean1);
            self.fserialCorrelation += self.alpha * (s1*s0) / var1 # (s1 * s0) #  / (sqrt(var1) * sqrt(var0))
#             print(self.n, s1*s0/var1, s0/sqrt(var1), s1/sqrt(var1) )
        self.eLast = e;
        self.n += 1;
        
    
def autocorr(x, t=1):
    return np.corrcoef(np.array([x[0:len(x)-t], x[t:len(x)]]))
    
if __name__ == '__main__':
    theta = 0.95
    nL = 51
#     stats = FadingStatistics(theta);
    stats = RingStatistics(51);

    for beta in np.arange(0.0,2.0+1e-6,0.5) :
        dsp = ThinkDSP.PinkNoise(beta=beta);
        S = dsp.make_wave().ys.transpose();
        S = S[0:nL]
    
        for i in range(0, len(S)) :
            stats.update(S[i]);
        fmt = "%5.3f %15.6g %15.6g %15.6g %6.3f";
        print(fmt % (beta, stats.getMean(), stats.getVariance(), stats.getMean()/stats.getVariance(), stats.getSerialCorrelation() ))
    #     print(fmt % (mean(S), var(S), autocorr(S)[0,1]))
        print(fmt % (beta, mean(S[-nL:]), var(S[-nL:]), mean(S[-nL:])/var(S[-nL:]), autocorr(S[-nL:])[0,1]))
    
