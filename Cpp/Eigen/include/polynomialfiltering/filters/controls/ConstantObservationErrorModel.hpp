/***** /PolynomialFiltering/filters/controls/ConstantObservationErrorModel/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_CONSTANTOBSERVATIONERRORMODEL_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_CONSTANTOBSERVATIONERRORMODEL_HPP

#include "io.h"
#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/filters/controls/IObservationErrorModel.hpp>


namespace PolynomialFiltering {
    namespace filters {
        namespace controls {
            class ConstantObservationErrorModel : public IObservationErrorModel {
                public:
                    ConstantObservationErrorModel(const RealMatrix& R);
                    ConstantObservationErrorModel(const RealMatrix& R, const RealMatrix& inverseR);
                    RealMatrix getPrecisionMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId=-1);
                    RealMatrix getCovarianceMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId=-1);
                protected:
                    RealMatrix R; ///<  observation covariance matrix
                    RealMatrix iR; ///<  observation precision (inverse covariance) matrix
            }; // class ConstantObservationErrorModel 

        }; // namespace controls
    }; // namespace filters
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_CONSTANTOBSERVATIONERRORMODEL_HPP