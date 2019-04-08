/***** /PolynomialFiltering/filters/controls/IObservationErrorModel/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IOBSERVATIONERRORMODEL_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IOBSERVATIONERRORMODEL_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>


namespace PolynomialFiltering {
    namespace filters {
        namespace controls {
            class IObservationErrorModel {
                public:
                    IObservationErrorModel();
                    virtual RealMatrix getPrecisionMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId) = 0;
                    virtual RealMatrix getCovarianceMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId) = 0;
            }; // class IObservationErrorModel 

        }; // namespace controls
    }; // namespace filters
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IOBSERVATIONERRORMODEL_HPP