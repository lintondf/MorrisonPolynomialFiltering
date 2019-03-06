/***** /PolynomialFiltering/Components/IRecursiveFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_IRECURSIVEFILTER_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_IRECURSIVEFILTER_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>


namespace PolynomialFiltering {
    namespace Components {
        class IRecursiveFilter : public AbstractFilter {
            public:
                IRecursiveFilter();
                virtual void start(const double t, const RealMatrix Z) = 0;
                virtual std::tuple<RealMatrix, double, double> predict(const double t) = 0;
                virtual void update(const double t, const RealMatrix dtau, const RealMatrix Zstar, const RealMatrix e) = 0;
                virtual long getN() = 0;
                virtual double getTime() = 0;
                virtual RealMatrix getState(const double t) = 0;
        }; // class IRecursiveFilter 

    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_IRECURSIVEFILTER_HPP