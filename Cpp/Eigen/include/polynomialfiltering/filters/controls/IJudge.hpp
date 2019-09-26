/***** /polynomialfiltering/filters/controls/IJudge/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IJUDGE_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IJUDGE_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>


#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/Fmp.hpp>


namespace polynomialfiltering {
    namespace filters {
        namespace controls {

            ///// @class /polynomialfiltering/filters/controls/::IJudge : <CLASS>; supers(ABC,)
            /// @brief Judges the goodness of fit of a filter
            /// 
            /// Called to determine whether to accept or reject the current observation and
            /// to estimate the goodness of fit
            /// 
            class IJudge {
                public:
                    IJudge() {};
                    virtual bool scalarUpdate(const double e, const RealMatrix& iR) = 0;
                    virtual bool vectorUpdate(const RealVector& e, const RealMatrix& iR) = 0;
                    virtual double getChi2() = 0;
                    virtual std::shared_ptr<AbstractFilterWithCovariance> getFilter() = 0;
                    virtual double getGOF() = 0;
            }; // class IJudge 

        }; // namespace controls
    }; // namespace filters
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IJUDGE_HPP