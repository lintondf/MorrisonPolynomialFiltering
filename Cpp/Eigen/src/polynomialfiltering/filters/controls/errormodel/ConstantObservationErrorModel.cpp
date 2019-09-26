/***** /polynomialfiltering/filters/controls/errormodel/ConstantObservationErrorModel/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */

#include "polynomialfiltering/filters/controls/errormodel/ConstantObservationErrorModel.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace filters {
        namespace controls {
            namespace errormodel {
                using namespace Eigen;
                
                    ConstantObservationErrorModel::ConstantObservationErrorModel (const double r) {
                        this->R = (RealVector1() << r).finished();
                        this->iR = (RealVector1() << 1.0 / r).finished();
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
                        RealMatrix P;
                        if (observationId ==  - 1) {
                            P = copy(this->iR);
                        } else {
                            P = this->iR.block(observationId, observationId, observationId + 1 - observationId, observationId + 1 - observationId);
                        }
                        return P;
                    }

                    RealMatrix ConstantObservationErrorModel::getCovarianceMatrix (const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId) {
                        RealMatrix P;
                        if (observationId ==  - 1) {
                            P = this->R;
                        } else {
                            P = this->R.block(observationId, observationId, observationId + 1 - observationId, observationId + 1 - observationId);
                        }
                        return P;
                    }

            }; // namespace errormodel
        }; // namespace controls
    }; // namespace filters
}; // namespace polynomialfiltering

#pragma float_control(pop)