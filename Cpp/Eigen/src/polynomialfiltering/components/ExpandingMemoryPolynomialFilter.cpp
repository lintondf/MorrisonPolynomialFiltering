/***** /PolynomialFiltering/Components/ExpandingMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/components/ExpandingMemoryPolynomialFilter.hpp"

namespace PolynomialFiltering {
    namespace Components {
        using namespace Eigen;
        
            EMPBase::EMPBase (const long order, const double tau) : AbstractRecursiveFilter(order,tau) {
            }

            double EMPBase::_gammaParameter (const double t, const double dtau) {
                return this->_normalizeTime(t);
            }

            EMP0::EMP0 (const double tau) : EMPBase(0,tau) {
            }

            RealVector EMP0::_gamma (const double n) {
                return Map<RowVectorXd>( new double[1] {1. / (1. + n)}, 1);
            }

            double EMP0::nSwitch (const double theta) {
                return 2.0 / (1.0 - theta);
            }

            RealMatrix EMP0::_VRF () {
                long n;
                RealMatrix V;
                n = this->n;
                V = Map<RowVectorXd>( new double[1] {1. / (n + 1.)}, 1);
                return V;
            }

            EMP1::EMP1 (const double tau) : EMPBase(1,tau) {
            }

            RealVector EMP1::_gamma (const double n) {
                double denom;
                denom = 1.0 / ((n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[2] {2. * (2. * n + 1.), 6.}, 2);
            }

            double EMP1::nSwitch (const double theta) {
                return 3.2 / (1.0 - theta);
            }

            RealMatrix EMP1::_VRF () {
                long n;
                double u;
                RealMatrix D;
                RealMatrix K;
                RealVector d;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                u = this->tau;
                K = Map<RowVectorXd>( new double[4] {(1., 0.866025403784), (0.866025403784, 1.)}, 4);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = 2 * (2 * n + 3) / ((n + 1) * n);
                d(1) = 12 / (pow(u, 2) * (n + 2) * (n + 1) * n);
                D = diag(sqrt(d));
                return D * K;
            }

            EMP2::EMP2 (const double tau) : EMPBase(2,tau) {
            }

            RealVector EMP2::_gamma (const double n) {
                double n2;
                double denom;
                n2 = n * n;
                denom = 1.0 / ((n + 3) * (n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[3] {3. * (3. * n2 + 3. * n + 2.), 18. * (2. * n + 1.), (2. * 1.) * 30.}, 3);
            }

            double EMP2::nSwitch (const double theta) {
                return 4.3636 / (1.0 - theta);
            }

            RealMatrix EMP2::_VRF () {
                long n;
                double u;
                RealMatrix D;
                RealMatrix K;
                RealVector d;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                u = this->tau;
                K = Map<RowVectorXd>( new double[9] {(1., 0.866025403784, 0.7453559925), (0.866025403784, 1., 0.968245836552), (0.7453559925, 0.968245836552, 1.)}, 9);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = 3 * (3 * pow(n, 2) + 9 * n + 8) / ((n + 1) * n * (n - 1));
                d(1) = 12 * (16 * pow(n, 2) + 62 * n + 57) / (pow(u, 2) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1));
                d(2) = 720 / (pow(u, 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1));
                D = diag(sqrt(d));
                return D * K;
            }

            EMP3::EMP3 (const double tau) : EMPBase(3,tau) {
            }

            RealVector EMP3::_gamma (const double n) {
                double n2;
                double n3;
                double denom;
                n2 = n * n;
                n3 = n2 * n;
                denom = 1.0 / ((n + 4) * (n + 3) * (n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[4] {8. * (2. * n3 + 3. * n2 + 7. * n + 3.), 20. * (6. * n2 + 6. * n + 5.), (2. * 1.) * 120. * (2. * n + 1.), (3. * 2. * 1.) * 140.}, 4);
            }

            double EMP3::nSwitch (const double theta) {
                return 5.50546 / (1.0 - theta);
            }

            RealMatrix EMP3::_VRF () {
                long n;
                double u;
                RealMatrix D;
                RealMatrix K;
                RealVector d;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                u = this->tau;
                K = Map<RowVectorXd>( new double[16] {(1., 0.866025403784, 0.7453559925, 0.661437827766), (0.866025403784, 1., 0.968245836552, 0.916515138991), (0.7453559925, 0.968245836552, 1., 0.986013297183), (0.661437827766, 0.916515138991, 0.986013297183, 1.)}, 16);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = 4 * (4 * pow(n, 3) + 18 * pow(n, 2) + 38 * n + 30) / ((n + 1) * n * (n - 1) * (n - 2));
                d(1) = 200 * (6 * pow(n, 4) + 51 * pow(n, 3) + 159 * pow(n, 2) + 219 * n + 116) / (pow(u, 2) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2));
                d(2) = 80 * (324 * pow(n, 2) + 1278 * n + 1188) / (pow(u, 4) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2));
                d(3) = 100800 / (pow(u, 6) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2));
                D = diag(sqrt(d));
                D = D * K;
                return D;
            }

            EMP4::EMP4 (const double tau) : EMPBase(4,tau) {
            }

            RealVector EMP4::_gamma (const double n) {
                double n2;
                double n3;
                double n4;
                double denom;
                n2 = n * n;
                n3 = n2 * n;
                n4 = n2 * n2;
                denom = 1.0 / ((n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[5] {5. * (5. * n4 + 10. * n3 + 55. * n2 + 50. * n + 24.), 25. * (12. * n3 + 18. * n2 + 46. * n + 20.), (2. * 1.) * 1050. * (n2 + n + 1.), (3. * 2. * 1.) * 700. * (2. * n + 1.), (4. * 3. * 2. * 1.) * 630.}, 5);
            }

            double EMP4::nSwitch (const double theta) {
                return 6.6321 / (1.0 - theta);
            }

            RealMatrix EMP4::_VRF () {
                long n;
                double u;
                RealMatrix D;
                RealMatrix K;
                RealVector d;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                u = this->tau;
                K = Map<RowVectorXd>( new double[25] {(1., 0.866025403784, 0.7453559925, 0.661437827766, 0.6), (0.866025403784, 1., 0.968245836552, 0.916515138991, 0.866025403784), (0.7453559925, 0.968245836552, 1., 0.986013297183, 0.9583148475), (0.661437827766, 0.916515138991, 0.986013297183, 1., 0.992156741649), (0.6, 0.866025403784, 0.9583148475, 0.992156741649, 1.)}, 25);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = 5 * (5 * pow(n, 4) + 30 * pow(n, 3) + 115 * pow(n, 2) + 210 * n + 144) / ((n + 1) * n * (n - 1) * (n - 2) * (n - 3));
                d(1) = 100 * (48 * pow(n, 6) + 666 * pow(n, 5) + 3843 * pow(n, 4) + 11982 * pow(n, 3) + 21727 * pow(n, 2) + 21938 * n + 9516) / (pow(u, 2) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2) * (n - 3));
                d(2) = 720 * (441 * pow(n, 4) + 3724 * pow(n, 3) + 11711 * pow(n, 2) + 21938 * n + 9516) / (pow(u, 4) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2) * (n - 3));
                d(3) = 100800 * (64 * pow(n, 2) + 254 * n + 237) / (pow(u, 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2) * (n - 3));
                d(4) = 25401600 / (pow(u, 8) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2) * (n - 3));
                D = diag(sqrt(d));
                return D * K;
            }

            EMP5::EMP5 (const double tau) : EMPBase(5,tau) {
            }

            RealVector EMP5::_gamma (const double n) {
                double n2;
                double n3;
                double n4;
                double denom;
                n2 = n * n;
                n3 = n2 * n;
                n4 = n2 * n2;
                denom = 1.0 / ((n + 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[6] {6. * (2. * n + 1.) * (3. * n4 + 6. * n3 + 77. * n2 + 74. * n + 120.), 126. * (5. * n4 + 10. * n3 + 55. * n2 + 50. * n + 28.), (2. * 1.) * 420. * (2. * n + 1.) * (4. * n2 + 4. * n + 15.), (3. * 2. * 1.) * 1260. * (6. * n2 + 6. * n + 7.), (4. * 3. * 2. * 1.) * 3780. * (2. * n + 1.), (5. * 4. * 3. * 2. * 1.) * 2772.}, 6);
            }

            double EMP5::nSwitch (const double theta) {
                return 7.7478 / (1.0 - theta);
            }

            RealMatrix EMP5::_VRF () {
                long n;
                double u;
                RealMatrix D;
                RealMatrix K;
                RealVector d;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                u = this->tau;
                K = Map<RowVectorXd>( new double[36] {(1., 0.866025403784, 0.7453559925, 0.661437827766, 0.6, 0.552770798393), (0.866025403784, 1., 0.968245836552, 0.916515138991, 0.866025403784, 0.820651806648), (0.7453559925, 0.968245836552, 1., 0.986013297183, 0.9583148475, 0.927024810887), (0.661437827766, 0.916515138991, 0.986013297183, 1., 0.992156741649, 0.974996043044), (0.6, 0.866025403784, 0.9583148475, 0.992156741649, 1., 0.994987437107), (0.552770798393, 0.820651806648, 0.927024810887, 0.974996043044, 0.994987437107, 1.)}, 36);
                d = ArrayXd::Zero(this->order + 1);
                d(0) = 6 * (2 * n + 3) * (3 * pow(n, 4) + 18 * pow(n, 3) + 113 * pow(n, 2) + 258 * n + 280) / ((n + 1) * n * (n - 1) * (n - 2) * (n - 3) * (n - 4));
                d(1) = 588 * (25 * pow(n, 8) + 500 * pow(n, 7) + 4450 * pow(n, 6) + 23300 * pow(n, 5) + 79585 * pow(n, 4) + 181760 * pow(n, 3) + 267180 * pow(n, 2) + 226920 * n + 84528) / (pow(u, 2) * (n + 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2) * (n - 3) * (n - 4));
                d(2) = 70560 * (2 * n + 3) * (16 * pow(n, 5) + 192 * pow(n, 4) + 952 * pow(n, 3) + 2472 * pow(n, 2) + 3501 * n + 2230) / (pow(u, 4) * (n + 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2) * (n - 3) * (n - 4));
                d(3) = 2721600 * (48 * pow(n, 4) + 402 * pow(n, 3) + 1274 * pow(n, 2) + 1828 * n + 1047) / (pow(u, 6) * (n + 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2) * (n - 3) * (n - 4));
                d(4) = 50803200 * (2 * n + 3) * (25 * n + 62) / (pow(u, 8) * (n + 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2) * (n - 3) * (n - 4));
                d(5) = 10059033600 / (pow(u, 10) * (n + 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) * n * (n - 1) * (n - 2) * (n - 3) * (n - 4));
                D = diag(sqrt(d));
                return D * K;
            }

        shared_ptr<EMPBase> makeEMP (const long order, const double tau) {
            if (order == 0) {
                return std::shared_ptr<EMP0>(new EMP0(tau));
            } else if (order == 1) {
                return std::shared_ptr<EMP1>(new EMP1(tau));
            } else if (order == 2) {
                return std::shared_ptr<EMP2>(new EMP2(tau));
            } else if (order == 3) {
                return std::shared_ptr<EMP3>(new EMP3(tau));
            } else if (order == 4) {
                return std::shared_ptr<EMP4>(new EMP4(tau));
            } else {
                return std::shared_ptr<EMP5>(new EMP5(tau));
            }
        }

    }; // namespace Components
}; // namespace PolynomialFiltering

