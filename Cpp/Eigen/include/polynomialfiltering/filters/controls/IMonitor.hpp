/***** /polynomialfiltering/filters/controls/IMonitor/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IMONITOR_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IMONITOR_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>


namespace polynomialfiltering {
    namespace filters {
        namespace controls {
            class IMonitor {
                public:
                    IMonitor();
                    virtual void accepted(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const RealVector& innovation, const int observationId) = 0;
                    virtual void rejected(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const RealVector& innovation, const int observationId) = 0;
            }; // class IMonitor 

        }; // namespace controls
    }; // namespace filters
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IMONITOR_HPP