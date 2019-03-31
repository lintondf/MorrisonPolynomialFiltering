/***** /PolynomialFiltering/Components/EmpFmpPair/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/components/EmpFmpPair.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace PolynomialFiltering {
    namespace Components {
        using namespace Eigen;
        
            EmpFmpPair::EmpFmpPair (const int order, const double theta, const double tau) : AbstractRecursiveFilter(order,tau) {
                this->emp = makeEMP(order, tau);
                this->fmp = makeFMP(order, theta, tau);
                this->current = this->emp;
            }

            void EmpFmpPair::start (const double t, const RealVector& Z) {
                this->current = this->emp;
                this->current->start(t, Z);
            }

            RealVector EmpFmpPair::predict (const double t) {
                return this->current->predict(t);
            }

            RealVector EmpFmpPair::update (const double t, const RealVector& Zstar, const double e) {
                RealVector innovation;
                innovation = this->current->update(t, Zstar, e);
                if (this->current == this->emp) {
                    if (this->emp->getN() >= this->emp->nSwitch(this->fmp->getTheta())) {
                        this->fmp->start(this->emp->getTime(), this->emp->getState());
                        this->current = this->fmp;
                    }
                }
                return innovation;
            }

            int EmpFmpPair::getN () {
                return this->current->getN();
            }

            double EmpFmpPair::getTau () {
                return this->current->getTau();
            }

            double EmpFmpPair::getTime () {
                return this->current->getTime();
            }

            RealVector EmpFmpPair::getState () {
                return this->current->getState();
            }

            RealMatrix EmpFmpPair::getVRF () {
                return this->current->getVRF();
            }

            double EmpFmpPair::_gammaParameter (const double t, const double dtau) {
                return 0;
            }

            RealVector EmpFmpPair::_gamma (const double n) {
                return ArrayXXd::Zero(this->order + 1, 1);
            }

            RealMatrix EmpFmpPair::_VRF () {
                return ArrayXXd::Zero(this->order + 1, this->order + 1);
            }

    }; // namespace Components
}; // namespace PolynomialFiltering

#pragma float_control(pop)