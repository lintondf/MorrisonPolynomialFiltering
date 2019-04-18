/***** /polynomialfiltering/components/ExpandingMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/components/ExpandingMemoryPolynomialFilter.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        using namespace Eigen;
        
            EMPBase::EMPBase (const int order, const double tau) : AbstractRecursiveFilter(order,tau) {
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
                int n;
                RealMatrix V;
                n = this->n;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = 1.0 / (n + 1);
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
                int n;
                double tau;
                RealMatrix V;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                tau = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = 2 * (2 * n + 1) / (pow(n, 2) + 3 * n + 2);
                V(0, 1) = 6 / (tau * (n + 1) * (n + 2));
                V(1, 0) = V(0, 1);
                V(1, 1) = 12 / (n * pow(tau, 2) * (n + 1) * (n + 2));
                return V;
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
                int n;
                double tau;
                RealMatrix V;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                tau = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = 3 * (3 * pow(n, 2) + 3 * n + 2) / (pow(n, 3) + 6 * pow(n, 2) + 11 * n + 6);
                V(0, 1) = 18 * (2 * n + 1) / (tau * (n + 1) * (n + 2) * (n + 3));
                V(1, 0) = V(0, 1);
                V(0, 2) = 60 / (pow(tau, 2) * (n + 1) * (n + 2) * (n + 3));
                V(2, 0) = V(0, 2);
                V(1, 1) = 12 * (15 * pow(n, 2) + (n - 1) * (n + 3)) / (n * pow(tau, 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3));
                V(1, 2) = 360 / (pow(tau, 3) * (n - 1) * (n + 1) * (n + 2) * (n + 3));
                V(2, 1) = V(1, 2);
                V(2, 2) = 720 / (n * pow(tau, 4) * (n - 1) * (n + 1) * (n + 2) * (n + 3));
                return V;
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
                int n;
                double tau;
                RealMatrix V;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                tau = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = 8 * (2 * pow(n, 3) + 3 * pow(n, 2) + 7 * n + 3) / (pow(n, 4) + 10 * pow(n, 3) + 35 * pow(n, 2) + 50 * n + 24);
                V(0, 1) = 20 * (6 * pow(n, 2) + 6 * n + 5) / (tau * (pow(n, 4) + 10 * pow(n, 3) + 35 * pow(n, 2) + 50 * n + 24));
                V(1, 0) = V(0, 1);
                V(0, 2) = 240 * (2 * n + 1) / (pow(tau, 2) * (n + 1) * (n + 2) * (n + 3) * (n + 4));
                V(2, 0) = V(0, 2);
                V(0, 3) = 840 / (pow(tau, 3) * (n + 1) * (n + 2) * (n + 3) * (n + 4));
                V(3, 0) = V(0, 3);
                V(1, 1) = 200 * (6 * pow(n, 4) - 3 * pow(n, 3) - 3 * pow(n, 2) - 3 * n + 2) / (n * pow(tau, 2) * (pow(n, 6) + 7 * pow(n, 5) + 7 * pow(n, 4) - 35 * pow(n, 3) - 56 * pow(n, 2) + 28 * n + 48));
                V(1, 2) = 600 * (9 * pow(n, 2) - 3 * n - 2) / (pow(tau, 3) * (pow(n, 6) + 7 * pow(n, 5) + 7 * pow(n, 4) - 35 * pow(n, 3) - 56 * pow(n, 2) + 28 * n + 48));
                V(2, 1) = V(1, 2);
                V(1, 3) = 1680 * (6 * pow(n, 2) - 3 * n + 2) / (n * pow(tau, 4) * (pow(n, 6) + 7 * pow(n, 5) + 7 * pow(n, 4) - 35 * pow(n, 3) - 56 * pow(n, 2) + 28 * n + 48));
                V(3, 1) = V(1, 3);
                V(2, 2) = 720 * (35 * pow(n, 2) + (n - 2) * (n + 4)) / (n * pow(tau, 4) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4));
                V(2, 3) = 50400 / (pow(tau, 5) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4));
                V(3, 2) = V(2, 3);
                V(3, 3) = 100800 / (n * pow(tau, 6) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4));
                return V;
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
                int n;
                double tau;
                RealMatrix V;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                tau = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = 5 * (5 * pow(n, 4) + 10 * pow(n, 3) + 55 * pow(n, 2) + 50 * n + 24) / (pow(n, 5) + 15 * pow(n, 4) + 85 * pow(n, 3) + 225 * pow(n, 2) + 274 * n + 120);
                V(0, 1) = 50 * (6 * pow(n, 3) + 9 * pow(n, 2) + 23 * n + 10) / (tau * (pow(n, 5) + 15 * pow(n, 4) + 85 * pow(n, 3) + 225 * pow(n, 2) + 274 * n + 120));
                V(1, 0) = V(0, 1);
                V(0, 2) = 2100 * (pow(n, 2) + n + 1) / (pow(tau, 2) * (pow(n, 5) + 15 * pow(n, 4) + 85 * pow(n, 3) + 225 * pow(n, 2) + 274 * n + 120));
                V(2, 0) = V(0, 2);
                V(0, 3) = 4200 * (2 * n + 1) / (pow(tau, 3) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5));
                V(3, 0) = V(0, 3);
                V(0, 4) = 15120 / (pow(tau, 4) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5));
                V(4, 0) = V(0, 4);
                V(1, 1) = 100 * (48 * pow(n, 6) - 90 * pow(n, 5) + 63 * pow(n, 4) - 198 * pow(n, 3) + 307 * pow(n, 2) + 98 * n - 60) / (n * pow(tau, 2) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(1, 2) = 4200 * (9 * pow(n, 4) - 12 * pow(n, 3) + 7 * pow(n, 2) - 7 * n + 15) / (pow(tau, 3) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(2, 1) = V(1, 2);
                V(1, 3) = 1680 * (96 * pow(n, 4) - 126 * pow(n, 3) + 131 * pow(n, 2) + 49 * n - 30) / (n * pow(tau, 4) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(3, 1) = V(1, 3);
                V(1, 4) = 151200 * (2 * pow(n, 2) - 3 * n + 5) / (pow(tau, 5) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(4, 1) = V(1, 4);
                V(2, 2) = 35280 * (9 * pow(n, 4) - 4 * pow(n, 3) - pow(n, 2) - 4 * n + 5) / (n * pow(tau, 4) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(2, 3) = 352800 * n * (4 * n - 1) / (pow(tau, 5) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(3, 2) = V(2, 3);
                V(2, 4) = 302400 * (9 * pow(n, 2) - 3 * n + 5) / (n * pow(tau, 6) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(4, 2) = V(2, 4);
                V(3, 3) = 100800 * (63 * pow(n, 2) + (n - 3) * (n + 5)) / (n * pow(tau, 6) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5));
                V(3, 4) = 12700800 / (pow(tau, 7) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5));
                V(4, 3) = V(3, 4);
                V(4, 4) = 25401600 / (n * pow(tau, 8) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5));
                return V;
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
                int n;
                double tau;
                RealMatrix V;
                n = this->n;
                if (n < this->order) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                tau = this->tau;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = 6 * (6 * pow(n, 5) + 15 * pow(n, 4) + 160 * pow(n, 3) + 225 * pow(n, 2) + 314 * n + 120) / (pow(n, 6) + 21 * pow(n, 5) + 175 * pow(n, 4) + 735 * pow(n, 3) + 1624 * pow(n, 2) + 1764 * n + 720);
                V(0, 1) = 126 * (5 * pow(n, 4) + 10 * pow(n, 3) + 55 * pow(n, 2) + 50 * n + 28) / (tau * (pow(n, 6) + 21 * pow(n, 5) + 175 * pow(n, 4) + 735 * pow(n, 3) + 1624 * pow(n, 2) + 1764 * n + 720));
                V(1, 0) = V(0, 1);
                V(0, 2) = 840 * (8 * pow(n, 3) + 12 * pow(n, 2) + 34 * n + 15) / (pow(tau, 2) * (pow(n, 6) + 21 * pow(n, 5) + 175 * pow(n, 4) + 735 * pow(n, 3) + 1624 * pow(n, 2) + 1764 * n + 720));
                V(2, 0) = V(0, 2);
                V(0, 3) = 7560 * (6 * pow(n, 2) + 6 * n + 7) / (pow(tau, 3) * (pow(n, 6) + 21 * pow(n, 5) + 175 * pow(n, 4) + 735 * pow(n, 3) + 1624 * pow(n, 2) + 1764 * n + 720));
                V(3, 0) = V(0, 3);
                V(0, 4) = 90720 * (2 * n + 1) / (pow(tau, 4) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5) * (n + 6));
                V(4, 0) = V(0, 4);
                V(0, 5) = 332640 / (pow(tau, 5) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5) * (n + 6));
                V(5, 0) = V(0, 5);
                V(1, 1) = 588 * (25 * pow(n, 8) - 100 * pow(n, 7) + 250 * pow(n, 6) - 700 * pow(n, 5) + 1585 * pow(n, 4) - 280 * pow(n, 3) - 540 * pow(n, 2) - 600 * n + 288) / (n * pow(tau, 2) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(1, 2) = 17640 * (10 * pow(n, 6) - 30 * pow(n, 5) + 65 * pow(n, 4) - 100 * pow(n, 3) + 219 * pow(n, 2) - 44 * n - 48) / (pow(tau, 3) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(2, 1) = V(1, 2);
                V(1, 3) = 105840 * (12 * pow(n, 6) - 33 * pow(n, 5) + 75 * pow(n, 4) - 30 * pow(n, 3) + 50 * pow(n, 2) - 50 * n + 24) / (n * pow(tau, 4) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(3, 1) = V(1, 3);
                V(1, 4) = 211680 * (25 * pow(n, 4) - 70 * pow(n, 3) + 185 * pow(n, 2) - 20 * n - 48) / (pow(tau, 5) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(4, 1) = V(1, 4);
                V(1, 5) = 665280 * (15 * pow(n, 4) - 45 * pow(n, 3) + 140 * pow(n, 2) - 50 * n + 24) / (n * pow(tau, 6) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(5, 1) = V(1, 5);
                V(2, 2) = 70560 * (32 * pow(n, 6) - 48 * pow(n, 5) + 80 * pow(n, 4) - 120 * pow(n, 3) + 258 * pow(n, 2) + 53 * n - 60) / (n * pow(tau, 4) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(2, 3) = 1058400 * (16 * pow(n, 4) - 16 * pow(n, 3) + 26 * pow(n, 2) - 14 * n + 33) / (pow(tau, 5) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(3, 2) = V(2, 3);
                V(2, 4) = 604800 * (120 * pow(n, 4) - 108 * pow(n, 3) + 238 * pow(n, 2) + 41 * n - 60) / (n * pow(tau, 6) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(4, 2) = V(2, 4);
                V(2, 5) = 139708800 * (pow(n, 2) - n + 3) / (pow(tau, 7) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(5, 2) = V(2, 5);
                V(3, 3) = 2721600 * (48 * pow(n, 4) - 18 * pow(n, 3) + 14 * pow(n, 2) - 20 * n + 39) / (n * pow(tau, 6) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(3, 4) = 114307200 * (5 * pow(n, 2) - n + 1) / (pow(tau, 7) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(4, 3) = V(3, 4);
                V(3, 5) = 279417600 * (4 * pow(n, 2) - n + 3) / (n * pow(tau, 8) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(5, 3) = V(3, 5);
                V(4, 4) = 25401600 * (99 * pow(n, 2) + (n - 4) * (n + 6)) / (n * pow(tau, 8) * (n - 4) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5) * (n + 6));
                V(4, 5) = 5029516800 / (pow(tau, 9) * (n - 4) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5) * (n + 6));
                V(5, 4) = V(4, 5);
                V(5, 5) = 10059033600 / (n * pow(tau, 10) * (n - 4) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5) * (n + 6));
                return V;
            }

        /*rTS*/std::shared_ptr<EMPBase> makeEMP (const int order, const double tau) {
            if (order == 0) {
                return /*eNE*/std::make_shared<EMP0>(tau);
            } else if (order == 1) {
                return /*eNE*/std::make_shared<EMP1>(tau);
            } else if (order == 2) {
                return /*eNE*/std::make_shared<EMP2>(tau);
            } else if (order == 3) {
                return /*eNE*/std::make_shared<EMP3>(tau);
            } else if (order == 4) {
                return /*eNE*/std::make_shared<EMP4>(tau);
            } else {
                return /*eNE*/std::make_shared<EMP5>(tau);
            }
        }

    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)