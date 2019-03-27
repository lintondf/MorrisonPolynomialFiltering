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
        
            FMPBase::FMPBase (const long order, const double theta, const double tau) : AbstractRecursiveFilter(order,tau) {
                this->theta = theta;
                this->n0 = 1;
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
                RealMatrix K;
                RealVector d;
                RealMatrix D;
                t = this->theta;
                u = this->tau;
                K = Map<RowVectorXd>( new double[4] {(1., 0.894427191), (0.894427191, 1.)}, 4);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = (pow(t, 2) + 4 * t + 5) * (1 - t) / pow((1 + t), 3);
                d(1) = 2 * pow((1 - t), 3) / (pow(u, 2) * pow((1 + t), 3));
                D = diag(sqrt(d));
                return D * K;
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
                RealMatrix K;
                RealVector d;
                RealMatrix D;
                t = this->theta;
                u = this->tau;
                K = Map<RowVectorXd>( new double[9] {(1., 0.888234788196, 0.804030252207), (0.888234788196, 1., 0.981980506062), (0.804030252207, 0.981980506062, 1.)}, 9);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = (pow(t, 4) + 6 * pow(t, 3) + 16 * pow(t, 2) + 24 * t + 19) * (1 - t) / pow((1 + t), 5);
                d(1) = (13 * pow(t, 2) + 50 * t + 49) * pow((1 - t), 3) / (2 * pow(u, 2) * pow((1 + t), 5));
                d(2) = 6 * pow((1 - t), 5) / (pow(u, 4) * pow((1 + t), 5));
                D = diag(sqrt(d));
                return D * K;
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
                RealMatrix K;
                RealVector d;
                RealMatrix D;
                t = this->theta;
                u = this->tau;
                K = Map<RowVectorXd>( new double[16] {(1., 0.88436317611, 0.794996299293, 0.741982233216), (0.88436317611, 1., 0.980286162792, 0.953514126371), (0.794996299293, 0.980286162792, 1., 0.99380799), (0.741982233216, 0.953514126371, 0.99380799, 1.)}, 16);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = (pow(t, 6) + 8 * pow(t, 5) + 29 * pow(t, 4) + 64 * pow(t, 3) + 97 * pow(t, 2) + 104 * t + 69) * (1 - t) / pow((1 + t), 7);
                d(1) = 5 / 18 * (53 * pow(t, 4) + 298 * pow(t, 3) + 762 * pow(t, 2) + 970 * t + 581) * pow((1 - t), 3) / (pow(u, 2) * pow((1 + t), 7));
                d(2) = 2 * (23 * pow(t, 2) + 76 * t + 63) * pow((1 - t), 5) / (pow(u, 4) * pow((1 + t), 7));
                d(3) = 20 * pow((1 - t), 7) / (pow(u, 6) * pow((1 + t), 7));
                D = diag(sqrt(d));
                return D * K;
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
                RealMatrix K;
                RealVector d;
                RealMatrix D;
                t = this->theta;
                u = this->tau;
                K = Map<RowVectorXd>( new double[25] {(1., 0.881694998952, 0.788560555275, 0.732485084173, 0.696485834473), (0.881694998952, 1., 0.979001802066, 0.95, 0.925929720202), (0.788560555275, 0.979001802066, 1., 0.993190197131, 0.981794965522), (0.732485084173, 0.95, 0.993190197131, 1., 0.997155044022), (0.696485834473, 0.925929720202, 0.981794965522, 0.997155044022, 1.)}, 25);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = (pow(t, 8) + 10 * pow(t, 7) + 46 * pow(t, 6) + 130 * pow(t, 5) + 256 * pow(t, 4) + 380 * pow(t, 3) + 446 * pow(t, 2) + 410 * t + 251) * (1 - t) / (pow((1 + t), 9));
                d(1) = 5 * (449 * pow(t, 6) + 2988 * pow(t, 5) + 10013 * pow(t, 4) + 21216 * pow(t, 3) + 28923 * pow(t, 2) + 25588 * t + 12199) * pow((1 - t), 3) / (72 * pow(u, 2) * pow((1 + t), 9));
                d(2) = 7 * (2021 * pow(t, 4) + 10144 * pow(t, 3) + 22746 * pow(t, 2) + 25144 * t + 12521) * pow((1 - t), 5) / (72 * pow(u, 4) * pow((1 + t), 9));
                d(3) = 5 * (113 * pow(t, 2) + 338 * t + 253) * pow((1 - t), 7) / (2 * pow(u, 6) * pow((1 + t), 9));
                d(4) = 70 * pow((1 - t), 9) / (pow(u, 8) * pow((1 + t), 9));
                D = diag(sqrt(d));
                return D * K;
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
                RealMatrix K;
                RealVector d;
                RealMatrix D;
                t = this->theta;
                u = this->tau;
                K = Map<RowVectorXd>( new double[36] {(1., 0.87973592749, 0.783712552247, 0.725202936114, 0.687322471879, 0.661260314876), (0.87973592749, 1., 0.977989154933, 0.947173349319, 0.921318523517, 0.901006701352), (0.783712552247, 0.977989154933, 1., 0.992676628391, 0.980284789003, 0.96828182239), (0.725202936114, 0.947173349319, 0.992676628391, 1., 0.996879269744, 0.991020788184), (0.687322471879, 0.921318523517, 0.980284789003, 0.996879269744, 1., 0.99846033011), (0.661260314876, 0.901006701352, 0.96828182239, 0.991020788184, 0.99846033011, 1.)}, 36);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = (pow(t, 10) + 12 * pow(t, 9) + 67 * pow(t, 8) + 232 * pow(t, 7) + 562 * pow(t, 6) + 1024 * pow(t, 5) + 1484 * pow(t, 4) + 1792 * pow(t, 3) + 1847 * pow(t, 2) + 1572 * t + 923) * (1 - t) / pow((1 + t), 11);
                d(1) = 7 * (17467 * pow(t, 8) + 124874 * pow(t, 7) + 478036 * pow(t, 6) + 1239958 * pow(t, 5) + 2345510 * pow(t, 4) + 3250918 * pow(t, 3) + 3352636 * pow(t, 2) + 2454074 * t + 1028527) * pow((1 - t), 3) / (1800 * pow(u, 2) * pow((1 + t), 11));
                d(2) = 7 * (7121 * pow(t, 6) + 43016 * pow(t, 5) + 129715 * pow(t, 4) + 244880 * pow(t, 3) + 295855 * pow(t, 2) + 225176 * t + 87581) * pow((1 - t), 5) / (72 * pow((2 * 1), 2) * pow(u, 4) * pow((1 + t), 11));
                d(3) = 3 * (2549 * pow(t, 4) + 12072 * pow(t, 3) + 24926 * pow(t, 2) + 25176 * t + 11117) * pow((1 - t), 7) / (pow((3 * 2 * 1), 2) * 4 * pow(u, 6) * pow((1 + t), 11));
                d(4) = 14 * (113 * pow(t, 2) + 316 * t + 221) * pow((1 - t), 9) / (pow((4 * 3 * 2 * 1), 2) * pow(u, 8) * pow((1 + t), 11));
                d(5) = (252 * pow((1 - t), 11)) / (pow((5 * 4 * 3 * 2 * 1), 2) * pow(u, 10) * pow((1 + t), 11));
                D = diag(sqrt(d));
                return D * K;
            }

        shared_ptr<FMPBase> makeFMP (const long order, const double theta, const double tau) {
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

        double thetaFromVrf (const long order, const double tau, const double vrf) {
            double x;
            if (order == 0) {
                x = std::max(1e-14, std::min(1 - 1e-6, vrf));
                return 2 / (1 + x) - 1;
            } else if (order == 1) {
                x = pow(tau, (2. / 3.)) * pow((vrf * 1. / 2.), (1. / 3.));
                x = std::max(1e-14, std::min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            } else if (order == 2) {
                x = pow(tau, (4. / 5.)) * pow((vrf * 1. / 6.), (1. / 5.));
                x = std::max(1e-14, std::min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            } else if (order == 3) {
                x = pow(tau, (6. / 7.)) * pow((vrf * 1. / 20.), (1. / 7.));
                x = std::max(1e-14, std::min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            } else if (order == 4) {
                x = pow(tau, (8. / 9.)) * pow((vrf * 1. / 70.), (1. / 9.));
                x = std::max(1e-14, std::min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            } else {
                x = pow(tau, (10. / 11.)) * pow((vrf * 14400. / 252.), (1. / 11.));
                x = std::max(1e-14, std::min(1 - 1e-6, x));
                return  - 1. + 2. / (1.0 + x);
            }
        }

    }; // namespace Components
}; // namespace PolynomialFiltering

#pragma float_control(pop)