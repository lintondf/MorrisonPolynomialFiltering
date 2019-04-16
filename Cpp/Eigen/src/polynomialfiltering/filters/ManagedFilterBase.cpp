/***** /PolynomialFiltering/filters/ManagedFilterBase/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/filters/ManagedFilterBase.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace PolynomialFiltering {
    namespace filters {
        using namespace Eigen;
        
            ManagedFilterBase::ManagedFilterBase (const std::shared_ptr<AbstractRecursiveFilter> worker) {
                this->worker = worker;
                this->errorModel = ConstantObservationErrorModel(eye(1), eye(1));
                this->judge = nullptr;
                this->monitor = nullptr;
            }

            FilterStatus ManagedFilterBase::getStatus () {
                return this->worker->getStatus(this);
            }

            int ManagedFilterBase::getN () {
                return this->worker->getN();
            }

            double ManagedFilterBase::getTime () {
                return this->worker->getTime();
            }

            RealVector ManagedFilterBase::getState () {
                return this->worker->getState();
            }

            std::shared_ptr<AbstractRecursiveFilter> ManagedFilterBase::getWorker () {
                return this->worker;
            }

            void ManagedFilterBase::setObservationInverseR (const RealMatrix& inverseR) {
                this->errorModel = ConstantObservationErrorModel(inverseR);
            }

            void ManagedFilterBase::setObservationErrorModel (const std::shared_ptr<IObservationErrorModel> errorModel) {
                this->errorModel = errorModel;
            }

            void ManagedFilterBase::setJudge (const std::shared_ptr<IJudge> judge) {
                this->judge = judge;
            }

            void ManagedFilterBase::setMonitor (const std::shared_ptr<IMonitor> monitor) {
                this->monitor = monitor;
            }

    }; // namespace filters
}; // namespace PolynomialFiltering

#pragma float_control(pop)