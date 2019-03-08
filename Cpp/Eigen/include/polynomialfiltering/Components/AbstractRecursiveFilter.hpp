/***** /PolynomialFiltering/Components/AbstractRecursiveFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_ABSTRACTRECURSIVEFILTER_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_ABSTRACTRECURSIVEFILTER_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/IRecursiveFilter.hpp>
#include <polynomialfiltering/Main.hpp>


namespace PolynomialFiltering {
    namespace Components {
        class AbstractRecursiveFilter : public IRecursiveFilter {
            public:
                static double effectiveTheta(const long order, const double n);
                AbstractRecursiveFilter(const long order, const double tau);
                void start(const double t, const RealVector Z);
                std::tuple<RealVector, double, double> predict(const double t);
                void update(const double t, const double dtau, const RealVector Zstar, const double e);
                long getN();
                double getTau();
                double getTime();
                RealVector getState(const double t);
            protected:
                long order;
                long n;
                long n0;
                double dtau;
                double t0;
                double tau;
                double t;
                RealVector Z;
                RealVector D;
                RealVector _conformState(const RealVector state);
                double _normalizeTime(const double t);
                double _normalizeDeltaTime(const double dt);
                RealVector _normalizeState(const RealVector Z);
                RealVector _denormalizeState(const RealVector Z);
                virtual double _gammaParameter(const double t, const double dtau) = 0;
                virtual RealVector _gamma(const double nOrT) = 0;
        }; // class AbstractRecursiveFilter 

    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_ABSTRACTRECURSIVEFILTER_HPP