''' PolynomialFiltering.filters.controls.IJudge
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from polynomialfiltering.PythonUtilities import virtual, chi2Cdf, chi2Ppf

from numpy import array, zeros, eye, exp, transpose
from numpy import array as vector;

from polynomialfiltering.Main import AbstractFilterWithCovariance
from polynomialfiltering.components.FadingMemoryPolynomialFilter import makeFMP
from polynomialfiltering.filters.controls.IJudge import IJudge


class BaseVectorJudge(IJudge):
    """
    Judges the goodness of fit of a filter
    """
    
    '''@chi2Starts : array | chi2 initialization values corresponding to 0.999999 Chi2 probability indexed by filter order'''
    
    '''@f : AbstractFilterWithCovariance | filter to judge'''
    '''@chi2Smoothing : float | Chi2 smoothing factor for goodness-of-fit; 0 no smoothing; 1 ignore residuals completely'''
    '''@chi2 : float | Chi2 statistic for last update'''
    '''@chi2Smoothed : float | Smoothed Chi2 statistic'''
        
    
    def __init__(self, f : AbstractFilterWithCovariance, editChi2 : float, chi2Smoothing : float = 0.9):
        # computed via chi2.ppf(1-1e-6, df)
        self.chi2Starts = array([23.92812697687947, 27.631021115871036, 30.664849706154268, 33.37684158165888, 35.88818687961042, 38.258336377145845]);

        self.f = f;
        self.df = f.getOrder() + 1;
        self.editChi2 = editChi2;
        self.chi2Smoothing = chi2Smoothing;
        self.chi2 = self.chi2Starts[f.getOrder()];
        self.chi2Smoothed = self.chi2;
        
    @classmethod
    def probabilityToChi2(self, p : float, df : int) -> float:
        return chi2Ppf(p, df);

    @virtual
    def scalarUpdate(self, e : float, iR : array ) -> bool:
        if (iR[0,0] == 0) :
            return True;
        self.chi2 = 1e-9 + (e * iR[0,0] * e);
        self.chi2Smoothed = self.chi2Smoothing * self.chi2Smoothed + (1-self.chi2Smoothing) * self.chi2;
        return self.chi2 < self.editChi2;

    @virtual
    def vectorUpdate(self, e : vector, iR : array ) -> bool:
        if (iR[0,0] == 0) :
            return True;
#             S[ie, ie] = GOFs[i,ie];
#             F[ie, ie] = chi2Cdf(S[ie, ie], 1)
#         print(i, A2S(diag(S)))
#         bestRatio = -1;
#         for j in range(0,K) :
#             if (S[j,j] != 0.0) :
#                 for k in range(j+1,K) :
#                     if (S[k,k] != 0.0 and S[k,k] < S[j,j]) :
#                         dS = S[j,j] - S[k,k];
#                         if (dS < chi2Ppf(0.5, 1)) :
#                             continue
#                         S[j,k] = dS
# #                         threshold = chi2Ppf(0.95, 1)
# #                         threshold = fdistPpf(0.95, 1, 2 );
# #                         x = dS / S[j,j]
# #                         x /= threshold;
#                         F[j,k] = dS
#                         if (dS < bestRatio) :
#                             bestRatio = dS;
#                             Best[i] = k; 
# # residual chi2 mean is not dependent on L; do this only for multi-element residuals                        
# #                         F[j,k] = (S[j,k]/(k-j)) /  (S[j,j]/(L-j-1))
# #                         fThreshold = fdistPpf(0.95, (k-j), (L-j-1) );
# #                         F[j,k] /= fThreshold;
# #                         if (F[j,k] < bestRatio)
# #                             bestRatio = F[j,k]
# #                             Best[i] = k;
# # residual chi2 mean is not dependent on L; do this only for multi-element residuals                        
        self.chi2 = (transpose(e) @ iR @ e);
        self.chi2Smoothed = self.chi2Smoothing * self.chi2Smoothed + (1-self.chi2Smoothing) * self.chi2;
        return self.chi2 < self.editChi2;

    @virtual
    def getChi2(self) -> float:
        return self.chi2;
    
    @virtual
    def getGOF(self) -> float:
        return chi2Cdf(self.chi2Smoothed, self.df)
# 
#     
# if __name__ == "__main__":
#     fmp = makeFMP(5, 0.99, 0.1);
#     threshold = BaseVectorJudge.probabilityToChi2(0.95, fmp.getOrder()+1);
#     print(threshold)
#     judge = BaseVectorJudge(fmp, threshold, 0.0)
#     i = zeros([6])
#     for e in range(0,10) :
#         chi2 = judge.scalarUpdate(e, eye(1));
#         j = judge.getGOF();
#         print(e, chi2, j)
#         