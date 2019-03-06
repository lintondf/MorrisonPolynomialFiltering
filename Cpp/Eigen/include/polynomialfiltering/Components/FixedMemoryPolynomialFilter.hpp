/***** /PolynomialFiltering/Components/FixedMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_FIXEDMEMORYPOLYNOMIALFILTER_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_FIXEDMEMORYPOLYNOMIALFILTER_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>


namespace PolynomialFiltering {
    namespace Components {
        class FixedMemoryFilter : public AbstractFilter {
            public:
                long order;
                long L;
                long n;
                long n0;
                double t0;
                double t;
                double tau;
                RealVector Z;
                RealVector tRing;
                RealVector yRing;
                FixedMemoryFilter(const long order, const long memorySize=51);
                long getN();
                double getTau();
                double getTime();
                RealMatrix getState(const double t);
                void add(const double t, const double y, const std::string observationId="");
                RealMatrix getVRF();
                RealMatrix _getTn(const RealVector dt);
        }; // class FixedMemoryFilter 

    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_FIXEDMEMORYPOLYNOMIALFILTER_HPP