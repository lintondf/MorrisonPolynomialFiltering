/***** /PolynomialFiltering/Components/EmpFmpPair/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_EMPFMPPAIR_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_EMPFMPPAIR_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>
#include <polynomialfiltering/components/ExpandingMemoryPolynomialFilter.hpp>
#include <polynomialfiltering/components/FadingMemoryPolynomialFilter.hpp>


namespace PolynomialFiltering {
    namespace Components {
        class EmpFmpPair : public AbstractRecursiveFilter {
            public:
                EmpFmpPair(const int order, const double theta, const double tau);
                void start(const double t, const RealVector& Z);
                RealVector predict(const double t);
                RealVector update(const double t, const RealVector& Zstar, const double e);
                int getN();
                double getTau();
                double getTime();
                RealVector getState();
                RealMatrix getVRF();
            protected:
                shared_ptr<EMPBase> emp;
                shared_ptr<FMPBase> fmp;
                shared_ptr<AbstractRecursiveFilter> current;
                double _gammaParameter(const double t, const double dtau);
                RealVector _gamma(const double n);
                RealMatrix _VRF();
        }; // class EmpFmpPair 

    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_EMPFMPPAIR_HPP