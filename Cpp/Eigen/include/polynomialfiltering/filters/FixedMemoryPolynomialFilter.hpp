/***** /polynomialfiltering/filters/FixedMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_FIXEDMEMORYPOLYNOMIALFILTER_HPP
#define ___POLYNOMIALFILTERING_FILTERS_FIXEDMEMORYPOLYNOMIALFILTER_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>


#include <polynomialfiltering/Main.hpp>


namespace polynomialfiltering {
    namespace filters {

        ///// @class /polynomialfiltering/filters/FixedMemoryPolynomialFilter/::FixedMemoryFilter : <CLASS>; supers(AbstractFilter,)
        /// @brief Equally-weighted, fixed memory size, irregularly spaced data filter
        /// 
        /// Same units between state and observations
        /// 
        class FixedMemoryFilter : public AbstractFilter {
            public:
                FixedMemoryFilter(const int order, const int memorySize=51);
                int getN();
                double getTau();
                double getTime();
                RealVector transitionState(const double t);
                RealVector getState();
                void add(const double t, const double y, const int observationId=-1);
                RealMatrix getVRF();
                double getFirstVRF();
                double getLastVRF();
            protected:
                int order; ///<  order of fitted polynomial
                int L; ///<  number of samples in memory window
                int n; ///<  total number of observations processed
                int n0; ///<  number of observations required for valid result
                double t0; ///<  start time of filter
                double t; ///<  current time of filter
                double tau; ///<  nominal step time of filter
                RealVector Z; ///<  UNNORMALIZED (external units) state vector
                RealVector tRing; ///<  ring buffer holding times of observations
                RealVector yRing; ///<  ring buffer holding values of observations
                RealMatrix _transitionVrf(const double t);
                RealMatrix _getTn(const RealVector& dt);
        }; // class FixedMemoryFilter 

    }; // namespace filters
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_FIXEDMEMORYPOLYNOMIALFILTER_HPP