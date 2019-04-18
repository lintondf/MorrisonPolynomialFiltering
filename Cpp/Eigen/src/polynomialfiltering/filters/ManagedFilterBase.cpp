/***** /polynomialfiltering/filters/ManagedFilterBase/
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
namespace polynomialfiltering {
    namespace filters {
        using namespace Eigen;
        
            ManagedFilterBase::ManagedFilterBase (const int order, const /*rTS*/std::shared_ptr<components::AbstractRecursiveFilter> worker) : AbstractFilterWithCovariance,IManagedFilter(order) {
                this->worker = worker;
                this->errorModel = /*eNE*/std::make_shared<controls::ConstantObservationErrorModel>(1.0);
                this->judge = nullptr;
                this->monitor = nullptr;
            }

            FilterStatus ManagedFilterBase::getStatus () {
                return this->worker->getStatus();
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

            /*rTS*/std::shared_ptr<components::AbstractRecursiveFilter> ManagedFilterBase::getWorker () {
                return this->worker;
            }

            void ManagedFilterBase::setObservationInverseR (const RealMatrix& inverseR) {
                this->errorModel = /*eNE*/std::make_shared<controls::ConstantObservationErrorModel>(inverseR);
            }

            void ManagedFilterBase::setObservationErrorModel (const /*rTS*/std::shared_ptr<controls::IObservationErrorModel> errorModel) {
                this->errorModel = errorModel;
            }

            void ManagedFilterBase::setJudge (const /*rTS*/std::shared_ptr<controls::IJudge> judge) {
                this->judge = judge;
            }

            void ManagedFilterBase::setMonitor (const /*rTS*/std::shared_ptr<controls::IMonitor> monitor) {
                this->monitor = monitor;
            }

    }; // namespace filters
}; // namespace polynomialfiltering

#pragma float_control(pop)