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

#pragma float_control(push)
#pragma float_control(precise, off)
namespace PolynomialFiltering {
    namespace Components {
        using namespace Eigen;
        
            FMPBase::FMPBase (const int order, const double theta, const double tau) : AbstractRecursiveFilter(order,tau) {
                this->theta = theta;
                this->n0 = 1;
            }

            double FMPBase::getTheta () {
                return this->theta;
            }

            double FMPBase::_gammaParameter (const double t, const double dtau) {
                return pow(this->theta, abs(dtau));
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
                t = this->theta;
                u = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                return V;
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
                t = this->theta;
                u = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                return V;
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
                t = this->theta;
                u = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                return V;
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
                double mt5;
                t2 = t * t;
                t3 = t2 * t;
                t5 = t2 * t3;
                mt2 = (1 - t) * (1 - t);
                mt3 = (1 - t) * mt2;
                mt4 = mt2 * mt2;
                mt5 = mt2 * mt3;
                return Map<RowVectorXd>( new double[5] {1. - t5, 5.0 / 12.0 * mt2 * (5. + 7. * t + 7. * t2 + 5. * t3), (2. * 1.) * 5.0 / 24.0 * mt3 * (7. + 10. * t + 7. * t2), (3. * 2. * 1.) * 5.0 / 12.0 * mt4 * (1. + t), (4. * 3. * 2. * 1.) * 1.0 / 24.0 * mt5}, 5);
            }

            RealMatrix FMP4::_VRF () {
                double t;
                double u;
                RealMatrix V;
                t = this->theta;
                u = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                return V;
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
                return Map<RowVectorXd>( new double[6] {1. - t6, 1.0 / 60.0 * mt2 * (137. + 202. * t + 222. * t2 + 202. * t3 + 137. * t4), 5.0 / 8.0 * mt3 * (3. + 5. * t + 5. * t2 + 3. * t3), 1.0 / 24.0 * mt4 * (17. + 26. * t + 17. * t2), 1.0 / 8.0 * mt5 * (1. + t), mt6 / 120.0}, 6);
            }

            RealMatrix FMP5::_VRF () {
                double t;
                double u;
                RealMatrix V;
                t = this->theta;
                u = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                return V;
            }

        shared_ptr<FMPBase> makeFMP (const int order, const double theta, const double tau) {
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

        double thetaFromVrf (const int order, const double tau, const double vrf) {
            double x;
            if (order == 0) {
                x = max(1e-14, min(1 - 1e-6, vrf));
                return 2 / (1 + x) - 1;
            } else if (order == 1) {
                x = pow(tau, (2. / 3.)) * pow((vrf * 1. / 2.), (1. / 3.));
                x = max(1e-14, min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            } else if (order == 2) {
                x = pow(tau, (4. / 5.)) * pow((vrf * 1. / 6.), (1. / 5.));
                x = max(1e-14, min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            } else if (order == 3) {
                x = pow(tau, (6. / 7.)) * pow((vrf * 1. / 20.), (1. / 7.));
                x = max(1e-14, min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            } else if (order == 4) {
                x = pow(tau, (8. / 9.)) * pow((vrf * 1. / 70.), (1. / 9.));
                x = max(1e-14, min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            } else {
                x = pow(tau, (10. / 11.)) * pow((vrf * 14400. / 252.), (1. / 11.));
                x = max(1e-14, min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            }
        }

    }; // namespace Components
}; // namespace PolynomialFiltering

#pragma float_control(pop)