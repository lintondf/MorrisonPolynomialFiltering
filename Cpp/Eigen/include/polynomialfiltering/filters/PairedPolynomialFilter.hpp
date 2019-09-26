/***** /polynomialfiltering/filters/PairedPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_PAIREDPOLYNOMIALFILTER_HPP
#define ___POLYNOMIALFILTERING_FILTERS_PAIREDPOLYNOMIALFILTER_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>


#include <polynomialfiltering/components/ICore.hpp>
#include <polynomialfiltering/filters/RecursivePolynomialFilter.hpp>
#include <polynomialfiltering/components/Emp.hpp>
#include <polynomialfiltering/components/Fmp.hpp>


namespace polynomialfiltering {
    namespace filters {
        class PairedPolynomialFilter : public RecursivePolynomialFilter {
            public:
                PairedPolynomialFilter(const int order, const double tau, const double theta);
                RealVector update(const double t, const RealVector& Zstar, const double e);
                void start(const double t, const RealVector& Z);
                bool isFading();
            protected:
                std::shared_ptr<components::ICore> empCore; ///<  provider of core expanding functions
                std::shared_ptr<components::ICore> fmpCore; ///<  provider of core fading functions
                int switchN;
                double theta;
        }; // class PairedPolynomialFilter 

    }; // namespace filters
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_PAIREDPOLYNOMIALFILTER_HPP