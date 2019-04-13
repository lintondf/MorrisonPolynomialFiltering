/***** /PolynomialFiltering/filters/controls/ConstantObservationErrorModel/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/filters/controls/ConstantObservationErrorModel.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace PolynomialFiltering {
    namespace filters {
        namespace controls {
            using namespace Eigen;
            
                ConstantObservationErrorModel::ConstantObservationErrorModel (const double r) {
                    this->R = Map<RowVectorXd>( new double[1] {r}, 1);
                    this->iR = Map<RowVectorXd>( new double[1] {1.0 / r}, 1);
                }

                ConstantObservationErrorModel::ConstantObservationErrorModel (const RealMatrix& R) {
                    this->R = R;
                    this->iR = inv(R);
                }

                ConstantObservationErrorModel::ConstantObservationErrorModel (const RealMatrix& R, const RealMatrix& inverseR) {
                    this->R = R;
                    this->iR = inverseR;
                }

                RealMatrix ConstantObservationErrorModel::getPrecisionMatrix (const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId) {
                    if (observationId ==  - 1) {
                        return this->iR;
                    } else {
                        return this->iR(observationId, observationId);
                    }
                }

                RealMatrix ConstantObservationErrorModel::getCovarianceMatrix (const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId) {
                    if (observationId ==  - 1) {
                        return this->R;
                    } else {
                        return this->R(observationId, observationId);
                    }
                }

        }; // namespace controls
    }; // namespace filters
}; // namespace PolynomialFiltering

#pragma float_control(pop)