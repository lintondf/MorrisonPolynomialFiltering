/***** /PolynomialFiltering/Components/FadingMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/components/FadingMemoryPolynomialFilter.hpp"

namespace PolynomialFiltering {
    namespace Components {
        using namespace Eigen;
        
            FMPBase::FMPBase (const long order, const double theta, const double tau) : AbstractRecursiveFilter(order,tau) {
                this->theta = theta;
                this->n0 = 1;
            }

            double FMPBase::_gammaParameter (const double t, const double dtau) {
                return pow(this->theta, abs(dtau));
            }

            RealMatrix FMPBase::_scaleVRF (const RealMatrix V, const double u, const double theta) {
                double t;
                RealMatrix S;
                t = 1 - theta;
                S = ArrayXXd::Zero(V.rows(), V.cols());
                S(0, 0) = t;
                for (long i = 1; i < S.rows(); i++) {
                    S(i, 0) = S(i - 1, 0) * t / u;
                }
                for (long i = 0; i < S.rows(); i++) {
                    for (long j = 1; j < S.cols(); j++) {
                        S(i, j) = S(i, j - 1) * t / u;
                    }
                }
                return arrayTimes(S, V);
            }

            FMP0::FMP0 (const double theta, const double tau) : FMPBase(0,theta,tau) {
            }

            RealVector FMP0::_gamma (const double t) {
                return Map<RowVectorXd>( new double[1] {1. - t}, 1);
            }

            RealMatrix FMP0::_VRF () {
                double t;
                RealMatrix V;
                t = this->theta;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = ((1 - t) / (1 + t));
                return V;
            }

            FMP1::FMP1 (const double theta, const double tau) : FMPBase(1,theta,tau) {
            }

            RealVector FMP1::_gamma (const double t) {
                double t2;
                double mt2;
                t2 = t * t;
                mt2 = (1 - t) * (1 - t);
                return Map<RowVectorXd>( new double[2] {1. - t2, mt2}, 2);
            }

            RealMatrix FMP1::_VRF () {
                double t;
                double u;
                RealMatrix V;
                t = 1 - this->theta;
                u = this->tau;
                V = Map<RowVectorXd>( new double[4] {(1.25, 0.5), (0.5, 0.25)}, 4);
                return this->_scaleVRF(V, u, t);
            }

            FMP2::FMP2 (const double theta, const double tau) : FMPBase(2,theta,tau) {
            }

            RealVector FMP2::_gamma (const double t) {
                double t2;
                double t3;
                double mt2;
                double mt3;
                t2 = t * t;
                t3 = t2 * t;
                mt2 = (1 - t) * (1 - t);
                mt3 = (1 - t) * mt2;
                return Map<RowVectorXd>( new double[3] {1. - t3, 3.0 / 2.0 * mt2 * (1. + t), (2. * 1.) * 1.0 / 2.0 * mt3}, 3);
            }

            RealMatrix FMP2::_VRF () {
                double t;
                double u;
                RealMatrix V;
                t = 1 - this->theta;
                u = this->tau;
                V = Map<RowVectorXd>( new double[9] {(2.0625, 1.6875, 0.5), (1.6875, 1.75, 0.5625), (0.5, 0.5625, 0.1875)}, 9);
                return this->_scaleVRF(V, u, t);
            }

            FMP3::FMP3 (const double theta, const double tau) : FMPBase(3,theta,tau) {
            }

            RealVector FMP3::_gamma (const double t) {
                double t2;
                double t3;
                double t4;
                double mt2;
                double mt3;
                double mt4;
                t2 = t * t;
                t3 = t2 * t;
                t4 = t3 * t;
                mt2 = (1 - t) * (1 - t);
                mt3 = (1 - t) * mt2;
                mt4 = mt2 * mt2;
                return Map<RowVectorXd>( new double[4] {1. - t4, 1.0 / 6.0 * mt2 * (11. + 14. * t + 11. * t2), (2. * 1.) * mt3 * (1. + t), (3. * 2. * 1.) * 1.0 / 6.0 * mt4}, 4);
            }

            RealMatrix FMP3::_VRF () {
                double t;
                double u;
                RealMatrix V;
                t = 1 - this->theta;
                u = this->tau;
                V = Map<RowVectorXd>( new double[16] {(2.90625, 3.625, 2.15625, 0.5), (3.625, 5.78125, 3.75, 0.90625), (2.15625, 3.75, 2.53125, 0.625), (0.5, 0.90625, 0.625, 0.15625)}, 16);
                return this->_scaleVRF(V, u, t);
            }

            FMP4::FMP4 (const double theta, const double tau) : FMPBase(4,theta,tau) {
            }

            RealVector FMP4::_gamma (const double t) {
                double t2;
                double t3;
                double t5;
                double mt2;
                double mt3;
                double mt4;
                t2 = t * t;
                t3 = t2 * t;
                t5 = t2 * t3;
                mt2 = (1 - t) * (1 - t);
                mt3 = (1 - t) * mt2;
                mt4 = mt2 * mt2;
                return Map<RowVectorXd>( new double[5] {1. - t5, 5.0 / 12.0 * mt2 * (5. + 7. * t + 7. * t2 + 5. * t3), (2. * 1.) * 5.0 / 24.0 * mt3 * (7. + 10. * t + 7. * t2), (3. * 2. * 1.) * 5.0 / 12.0 * mt4 * (1. + t), (4. * 3. * 2. * 1.) * 1.0 / 24.0 * mt4}, 5);
            }

            RealMatrix FMP4::_VRF () {
                double t;
                double u;
                RealMatrix V;
                t = 1 - this->theta;
                u = this->tau;
                V = Map<RowVectorXd>( new double[25] {(3.7695313, 6.3476563, 5.6835938, 2.6367188, 0.5), (6.3476563, 13.75, 13.476563, 6.53125, 1.2695313), (5.6835938, 13.476563, 13.78125, 6.8359375, 1.3476563), (2.6367188, 6.53125, 6.8359375, 3.4375, 0.68359375), (0.5, 1.2695313, 1.3476563, 0.68359375, 0.13671875)}, 25);
                return this->_scaleVRF(V, u, t);
            }

            FMP5::FMP5 (const double theta, const double tau) : FMPBase(5,theta,tau) {
            }

            RealVector FMP5::_gamma (const double t) {
                double t2;
                double t3;
                double t4;
                double t6;
                double mt2;
                double mt3;
                double mt4;
                double mt5;
                double mt6;
                t2 = t * t;
                t3 = t2 * t;
                t4 = t3 * t;
                t6 = t2 * t4;
                mt2 = (1 - t) * (1 - t);
                mt3 = (1 - t) * mt2;
                mt4 = mt2 * mt2;
                mt5 = mt3 * mt2;
                mt6 = mt3 * mt3;
                return Map<RowVectorXd>( new double[6] {1. - t6, 1.0 / 60.0 * mt2 * (137. + 202. * t + 222. * t2 + 202. * t3 + 137. * t4), (2. * 1.) * 5.0 / 8.0 * mt3 * (1. + t) * (3. + 2. * t + 3. * t2), (3. * 2. * 1.) * 1.0 / 24.0 * mt4 * (17. + 26. * t + 17. * t2), (4. * 3. * 2. * 1.) * 1.0 / 8.0 * mt5 * (1. + t), (5. * 4. * 3. * 2. * 1.) * 1.0 / 120.0 * mt6}, 6);
            }

            RealMatrix FMP5::_VRF () {
                double t;
                double u;
                RealMatrix V;
                t = 1 - this->theta;
                u = this->tau;
                V = Map<RowVectorXd>( new double[36] {(4.6464844, 9.8789063, 11.832031, 8.2382813, 3.1230469, 0.5), (9.8789063, 27.138672, 35.683594, 26.003906, 10.117188, 1.6464844), (11.832031, 35.683594, 49.054687, 36.640625, 14.472656, 2.3789063), (8.2382813, 26.003906, 36.640625, 27.773438, 11.074219, 1.8320313), (3.1230469, 10.117188, 14.472656, 11.074219, 4.4433594, 0.73828125), (0.5, 1.6464844, 2.3789063, 1.8320313, 0.73828125, 0.12304688)}, 36);
                return this->_scaleVRF(V, u, t);
            }

        std::shared_ptr<FMPBase> makeFMP (const long order, const double theta, const double tau) {
            if (order == 0) {
                return std::shared_ptr<FMP0>(new FMP0(theta, tau));
            } else if (order == 1) {
                return std::shared_ptr<FMP1>(new FMP1(theta, tau));
            } else if (order == 2) {
                return std::shared_ptr<FMP2>(new FMP2(theta, tau));
            } else if (order == 3) {
                return std::shared_ptr<FMP3>(new FMP3(theta, tau));
            } else if (order == 4) {
                return std::shared_ptr<FMP4>(new FMP4(theta, tau));
            } else {
                return std::shared_ptr<FMP5>(new FMP5(theta, tau));
            }
        }

    }; // namespace Components
}; // namespace PolynomialFiltering

