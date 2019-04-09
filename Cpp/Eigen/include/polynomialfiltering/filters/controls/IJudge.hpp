/***** /PolynomialFiltering/filters/controls/IJudge/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IJUDGE_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IJUDGE_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/FadingMemoryPolynomialFilter.hpp>


namespace PolynomialFiltering {
    namespace filters {
        namespace controls {

            ///// @class IJudge
            /// @brief Judges the goodness of fit of a filter
            /// 
            /// Called to determine whether to accept or reject the current observation and
            /// to estimate th
            /// 
            class IJudge {
                public:
                    IJudge();
                    virtual bool scalarUpdate(const double e, const RealMatrix& iR) = 0;
                    virtual bool vectorUpdate(const RealVector& e, const RealMatrix& iR) = 0;
                    virtual double getChi2() = 0;
                    virtual shared_ptr<AbstractFilterWithCovariance> getFilter() = 0;
                    virtual double getGOF() = 0;
            }; // class IJudge 

        }; // namespace controls
    }; // namespace filters
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IJUDGE_HPP