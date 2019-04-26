/***** /polynomialfiltering/components/Emp/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/components/Emp.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        using namespace Eigen;
        
            CoreEmp0::CoreEmp0 (const double tau)) {
                this->order = 0;
                this->tau = tau;
            }

            RealVector CoreEmp0::getGamma (const double n, const double dtau) {
                return Map<RowVectorXd>( new double[1] {1. / (1. + n)}, 1);
            }

            double CoreEmp0::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp0::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealVector CoreEmp0::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp0::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp0::_getFirstVRF (const int n, const double tau) {
                return 1.0 / (n + 1);
            }

            double CoreEmp0::_getLastVRF (const int n, const double tau) {
                return 1.0 / (n + 1);
            }

            RealMatrix CoreEmp0::_getDiagonalVRF (const int n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp0::_getVRF (const int n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                return V;
            }

            CoreEmp1::CoreEmp1 (const double tau)) {
                this->order = 1;
                this->tau = tau;
            }

            RealVector CoreEmp1::getGamma (const double n, const double dtau) {
                double denom;
                denom = 1.0 / ((n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[2] {2. * (2. * n + 1.), 6.}, 2);
            }

            double CoreEmp1::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp1::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealVector CoreEmp1::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp1::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp1::_getFirstVRF (const int n, const double tau) {
                return 2 * (2 * n + 3) / (n * (n + 1));
            }

            double CoreEmp1::_getLastVRF (const int n, const double tau) {
                return 12 / (n * pow(tau, 2) * (n + 1) * (n + 2));
            }

            RealMatrix CoreEmp1::_getDiagonalVRF (const int n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp1::_getVRF (const int n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 6 / (n * tau * (n + 1));
                V(1, 0) = V(0, 1);
                return V;
            }

            CoreEmp2::CoreEmp2 (const double tau)) {
                this->order = 2;
                this->tau = tau;
            }

            RealVector CoreEmp2::getGamma (const double n, const double dtau) {
                double n2;
                double denom;
                n2 = n * n;
                denom = 1.0 / ((n + 3) * (n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[3] {3. * (3. * n2 + 3. * n + 2.), 18. * (2. * n + 1.), (2. * 1.) * 30.}, 3);
            }

            double CoreEmp2::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp2::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealVector CoreEmp2::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp2::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp2::_getFirstVRF (const int n, const double tau) {
                return 3 * (3 * pow(n, 2) + 9 * n + 8) / (n * (pow(n, 2) - 1));
            }

            double CoreEmp2::_getLastVRF (const int n, const double tau) {
                return 720 / (n * pow(tau, 4) * (n - 1) * (n + 1) * (n + 2) * (n + 3));
            }

            RealMatrix CoreEmp2::_getDiagonalVRF (const int n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = 12 * ((n - 1) * (n + 3) + 15 * pow((n + 2), 2)) / (n * pow(tau, 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3));
                V(2, 2) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp2::_getVRF (const int n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 18 * (2 * n + 3) / (n * tau * (pow(n, 2) - 1));
                V(1, 0) = V(0, 1);
                V(0, 2) = 60 / (n * pow(tau, 2) * (pow(n, 2) - 1));
                V(2, 0) = V(0, 2);
                V(1, 2) = 360 / (n * pow(tau, 3) * (n - 1) * (n + 1) * (n + 3));
                V(2, 1) = V(1, 2);
                return V;
            }

            CoreEmp3::CoreEmp3 (const double tau)) {
                this->order = 3;
                this->tau = tau;
            }

            RealVector CoreEmp3::getGamma (const double n, const double dtau) {
                double n2;
                double n3;
                double denom;
                n2 = n * n;
                n3 = n2 * n;
                denom = 1.0 / ((n + 4) * (n + 3) * (n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[4] {8. * (2. * n3 + 3. * n2 + 7. * n + 3.), 20. * (6. * n2 + 6. * n + 5.), (2. * 1.) * 120. * (2. * n + 1.), (3. * 2. * 1.) * 140.}, 4);
            }

            double CoreEmp3::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp3::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealVector CoreEmp3::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp3::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp3::_getFirstVRF (const int n, const double tau) {
                return 8 * (2 * pow(n, 3) + 9 * pow(n, 2) + 19 * n + 15) / (n * (pow(n, 3) - 2 * pow(n, 2) - n + 2));
            }

            double CoreEmp3::_getLastVRF (const int n, const double tau) {
                return 100800 / (n * pow(tau, 6) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4));
            }

            RealMatrix CoreEmp3::_getDiagonalVRF (const int n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = 200 * (6 * pow(n, 4) + 51 * pow(n, 3) + 159 * pow(n, 2) + 219 * n + 116) / (n * pow(tau, 2) * (pow(n, 6) + 7 * pow(n, 5) + 7 * pow(n, 4) - 35 * pow(n, 3) - 56 * pow(n, 2) + 28 * n + 48));
                V(2, 2) = 720 * ((n - 2) * (n + 4) + 35 * pow((n + 2), 2)) / (n * pow(tau, 4) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4));
                V(3, 3) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp3::_getVRF (const int n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 20 * (6 * pow(n, 2) + 18 * n + 17) / (n * tau * (pow(n, 3) - 2 * pow(n, 2) - n + 2));
                V(1, 0) = V(0, 1);
                V(0, 2) = 240 * (2 * n + 3) / (n * pow(tau, 2) * (pow(n, 3) - 2 * pow(n, 2) - n + 2));
                V(2, 0) = V(0, 2);
                V(0, 3) = 840 / (n * pow(tau, 3) * (pow(n, 3) - 2 * pow(n, 2) - n + 2));
                V(3, 0) = V(0, 3);
                V(1, 2) = 600 * (9 * pow(n, 2) + 39 * n + 40) / (n * pow(tau, 3) * (pow(n, 5) + 5 * pow(n, 4) - 3 * pow(n, 3) - 29 * pow(n, 2) + 2 * n + 24));
                V(2, 1) = V(1, 2);
                V(1, 3) = 1680 * (6 * pow(n, 2) + 27 * n + 32) / (n * pow(tau, 4) * (pow(n, 6) + 7 * pow(n, 5) + 7 * pow(n, 4) - 35 * pow(n, 3) - 56 * pow(n, 2) + 28 * n + 48));
                V(3, 1) = V(1, 3);
                V(2, 3) = 50400 / (n * pow(tau, 5) * (n - 2) * (n - 1) * (n + 1) * (n + 3) * (n + 4));
                V(3, 2) = V(2, 3);
                return V;
            }

            CoreEmp4::CoreEmp4 (const double tau)) {
                this->order = 4;
                this->tau = tau;
            }

            RealVector CoreEmp4::getGamma (const double n, const double dtau) {
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

            double CoreEmp4::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp4::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealVector CoreEmp4::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp4::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp4::_getFirstVRF (const int n, const double tau) {
                return 5 * (5 * pow(n, 4) + 30 * pow(n, 3) + 115 * pow(n, 2) + 210 * n + 144) / (n * (pow(n, 4) - 5 * pow(n, 3) + 5 * pow(n, 2) + 5 * n - 6));
            }

            double CoreEmp4::_getLastVRF (const int n, const double tau) {
                return 25401600 / (n * pow(tau, 8) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5));
            }

            RealMatrix CoreEmp4::_getDiagonalVRF (const int n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = 100 * (48 * pow(n, 6) + 666 * pow(n, 5) + 3843 * pow(n, 4) + 11982 * pow(n, 3) + 21727 * pow(n, 2) + 21938 * n + 9516) / (n * pow(tau, 2) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(2, 2) = 35280 * (9 * pow(n, 4) + 76 * pow(n, 3) + 239 * pow(n, 2) + 336 * n + 185) / (n * pow(tau, 4) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(3, 3) = 100800 * ((n - 3) * (n + 5) + 63 * pow((n + 2), 2)) / (n * pow(tau, 6) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5));
                V(4, 4) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp4::_getVRF (const int n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 50 * (6 * pow(n, 3) + 27 * pow(n, 2) + 59 * n + 48) / (n * tau * (pow(n, 4) - 5 * pow(n, 3) + 5 * pow(n, 2) + 5 * n - 6));
                V(1, 0) = V(0, 1);
                V(0, 2) = 2100 * (pow(n, 2) + 3 * n + 3) / (n * pow(tau, 2) * (pow(n, 4) - 5 * pow(n, 3) + 5 * pow(n, 2) + 5 * n - 6));
                V(2, 0) = V(0, 2);
                V(0, 3) = 4200 * (2 * n + 3) / (n * pow(tau, 3) * (pow(n, 4) - 5 * pow(n, 3) + 5 * pow(n, 2) + 5 * n - 6));
                V(3, 0) = V(0, 3);
                V(0, 4) = 15120 / (n * pow(tau, 4) * (pow(n, 4) - 5 * pow(n, 3) + 5 * pow(n, 2) + 5 * n - 6));
                V(4, 0) = V(0, 4);
                V(1, 2) = 4200 * (9 * pow(n, 4) + 84 * pow(n, 3) + 295 * pow(n, 2) + 467 * n + 297) / (n * pow(tau, 3) * (pow(n, 7) + 7 * pow(n, 6) - 8 * pow(n, 5) - 110 * pow(n, 4) - 11 * pow(n, 3) + 463 * pow(n, 2) + 18 * n - 360));
                V(2, 1) = V(1, 2);
                V(1, 3) = 1680 * (96 * pow(n, 4) + 894 * pow(n, 3) + 3191 * pow(n, 2) + 5059 * n + 2940) / (n * pow(tau, 4) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(3, 1) = V(1, 3);
                V(1, 4) = 151200 * (2 * pow(n, 2) + 11 * n + 19) / (n * pow(tau, 5) * (pow(n, 7) + 7 * pow(n, 6) - 8 * pow(n, 5) - 110 * pow(n, 4) - 11 * pow(n, 3) + 463 * pow(n, 2) + 18 * n - 360));
                V(4, 1) = V(1, 4);
                V(2, 3) = 352800 * (4 * pow(n, 2) + 17 * n + 18) / (n * pow(tau, 5) * (pow(n, 7) + 7 * pow(n, 6) - 8 * pow(n, 5) - 110 * pow(n, 4) - 11 * pow(n, 3) + 463 * pow(n, 2) + 18 * n - 360));
                V(3, 2) = V(2, 3);
                V(2, 4) = 302400 * (9 * pow(n, 2) + 39 * n + 47) / (n * pow(tau, 6) * (pow(n, 8) + 9 * pow(n, 7) + 6 * pow(n, 6) - 126 * pow(n, 5) - 231 * pow(n, 4) + 441 * pow(n, 3) + 944 * pow(n, 2) - 324 * n - 720));
                V(4, 2) = V(2, 4);
                V(3, 4) = 12700800 / (n * pow(tau, 7) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 3) * (n + 4) * (n + 5));
                V(4, 3) = V(3, 4);
                return V;
            }

            CoreEmp5::CoreEmp5 (const double tau)) {
                this->order = 5;
                this->tau = tau;
            }

            RealVector CoreEmp5::getGamma (const double n, const double dtau) {
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

            double CoreEmp5::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp5::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealVector CoreEmp5::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp5::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp5::_getFirstVRF (const int n, const double tau) {
                return 6 * (6 * pow(n, 5) + 45 * pow(n, 4) + 280 * pow(n, 3) + 855 * pow(n, 2) + 1334 * n + 840) / (n * (pow(n, 5) - 9 * pow(n, 4) + 25 * pow(n, 3) - 15 * pow(n, 2) - 26 * n + 24));
            }

            double CoreEmp5::_getLastVRF (const int n, const double tau) {
                return 10059033600 / (n * pow(tau, 10) * (n - 4) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5) * (n + 6));
            }

            RealMatrix CoreEmp5::_getDiagonalVRF (const int n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = 588 * (25 * pow(n, 8) + 500 * pow(n, 7) + 4450 * pow(n, 6) + 23300 * pow(n, 5) + 79585 * pow(n, 4) + 181760 * pow(n, 3) + 267180 * pow(n, 2) + 226920 * n + 84528) / (n * pow(tau, 2) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(2, 2) = 70560 * (32 * pow(n, 6) + 432 * pow(n, 5) + 2480 * pow(n, 4) + 7800 * pow(n, 3) + 14418 * pow(n, 2) + 14963 * n + 6690) / (n * pow(tau, 4) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(3, 3) = 2721600 * (48 * pow(n, 4) + 402 * pow(n, 3) + 1274 * pow(n, 2) + 1828 * n + 1047) / (n * pow(tau, 6) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(4, 4) = 25401600 * ((n - 4) * (n + 6) + 99 * pow((n + 2), 2)) / (n * pow(tau, 8) * (n - 4) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 2) * (n + 3) * (n + 4) * (n + 5) * (n + 6));
                V(5, 5) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp5::_getVRF (const int n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 126 * (5 * pow(n, 4) + 30 * pow(n, 3) + 115 * pow(n, 2) + 210 * n + 148) / (n * tau * (pow(n, 5) - 9 * pow(n, 4) + 25 * pow(n, 3) - 15 * pow(n, 2) - 26 * n + 24));
                V(1, 0) = V(0, 1);
                V(0, 2) = 840 * (8 * pow(n, 3) + 36 * pow(n, 2) + 82 * n + 69) / (n * pow(tau, 2) * (pow(n, 5) - 9 * pow(n, 4) + 25 * pow(n, 3) - 15 * pow(n, 2) - 26 * n + 24));
                V(2, 0) = V(0, 2);
                V(0, 3) = 7560 * (6 * pow(n, 2) + 18 * n + 19) / (n * pow(tau, 3) * (pow(n, 5) - 9 * pow(n, 4) + 25 * pow(n, 3) - 15 * pow(n, 2) - 26 * n + 24));
                V(3, 0) = V(0, 3);
                V(0, 4) = 90720 * (2 * n + 3) / (n * pow(tau, 4) * (pow(n, 5) - 9 * pow(n, 4) + 25 * pow(n, 3) - 15 * pow(n, 2) - 26 * n + 24));
                V(4, 0) = V(0, 4);
                V(0, 5) = 332640 / (n * pow(tau, 5) * (pow(n, 5) - 9 * pow(n, 4) + 25 * pow(n, 3) - 15 * pow(n, 2) - 26 * n + 24));
                V(5, 0) = V(0, 5);
                V(1, 2) = 17640 * (10 * pow(n, 6) + 150 * pow(n, 5) + 965 * pow(n, 4) + 3420 * pow(n, 3) + 7179 * pow(n, 2) + 8520 * n + 4356) / (n * pow(tau, 3) * (pow(n, 9) + 9 * pow(n, 8) - 18 * pow(n, 7) - 294 * pow(n, 6) - 39 * pow(n, 5) + 3081 * pow(n, 4) + 1208 * pow(n, 3) - 11436 * pow(n, 2) - 1152 * n + 8640));
                V(2, 1) = V(1, 2);
                V(1, 3) = 105840 * (12 * pow(n, 6) + 177 * pow(n, 5) + 1125 * pow(n, 4) + 3870 * pow(n, 3) + 7550 * pow(n, 2) + 7954 * n + 3588) / (n * pow(tau, 4) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(3, 1) = V(1, 3);
                V(1, 4) = 211680 * (25 * pow(n, 4) + 270 * pow(n, 3) + 1205 * pow(n, 2) + 2400 * n + 1692) / (n * pow(tau, 5) * (pow(n, 9) + 9 * pow(n, 8) - 18 * pow(n, 7) - 294 * pow(n, 6) - 39 * pow(n, 5) + 3081 * pow(n, 4) + 1208 * pow(n, 3) - 11436 * pow(n, 2) - 1152 * n + 8640));
                V(4, 1) = V(1, 4);
                V(1, 5) = 665280 * (15 * pow(n, 4) + 165 * pow(n, 3) + 770 * pow(n, 2) + 1630 * n + 1284) / (n * pow(tau, 6) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(5, 1) = V(1, 5);
                V(2, 3) = 1058400 * (16 * pow(n, 4) + 144 * pow(n, 3) + 506 * pow(n, 2) + 822 * n + 549) / (n * pow(tau, 5) * (pow(n, 9) + 9 * pow(n, 8) - 18 * pow(n, 7) - 294 * pow(n, 6) - 39 * pow(n, 5) + 3081 * pow(n, 4) + 1208 * pow(n, 3) - 11436 * pow(n, 2) - 1152 * n + 8640));
                V(3, 2) = V(2, 3);
                V(2, 4) = 604800 * (120 * pow(n, 4) + 1068 * pow(n, 3) + 3766 * pow(n, 2) + 6047 * n + 3594) / (n * pow(tau, 6) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(4, 2) = V(2, 4);
                V(2, 5) = 139708800 * (pow(n, 2) + 5 * n + 9) / (n * pow(tau, 7) * (pow(n, 9) + 9 * pow(n, 8) - 18 * pow(n, 7) - 294 * pow(n, 6) - 39 * pow(n, 5) + 3081 * pow(n, 4) + 1208 * pow(n, 3) - 11436 * pow(n, 2) - 1152 * n + 8640));
                V(5, 2) = V(2, 5);
                V(3, 4) = 114307200 * (5 * pow(n, 2) + 21 * n + 23) / (n * pow(tau, 7) * (pow(n, 9) + 9 * pow(n, 8) - 18 * pow(n, 7) - 294 * pow(n, 6) - 39 * pow(n, 5) + 3081 * pow(n, 4) + 1208 * pow(n, 3) - 11436 * pow(n, 2) - 1152 * n + 8640));
                V(4, 3) = V(3, 4);
                V(3, 5) = 279417600 * (4 * pow(n, 2) + 17 * n + 21) / (n * pow(tau, 8) * (pow(n, 10) + 11 * pow(n, 9) - 330 * pow(n, 7) - 627 * pow(n, 6) + 3003 * pow(n, 5) + 7370 * pow(n, 4) - 9020 * pow(n, 3) - 24024 * pow(n, 2) + 6336 * n + 17280));
                V(5, 3) = V(3, 5);
                V(4, 5) = 5029516800 / (n * pow(tau, 9) * (n - 4) * (n - 3) * (n - 2) * (n - 1) * (n + 1) * (n + 3) * (n + 4) * (n + 5) * (n + 6));
                V(5, 4) = V(4, 5);
                return V;
            }

        double nSwitch (const int order, const double theta) {
            if (order == 0) {
                return 2.0 / (1.0 - theta);
            } else if (order == 1) {
                return 3.2 / (1.0 - theta);
            } else if (order == 2) {
                return 4.3636 / (1.0 - theta);
            } else if (order == 3) {
                return 5.50546 / (1.0 - theta);
            } else if (order == 4) {
                return 6.6321 / (1.0 - theta);
            } else if (order == 5) {
                return 7.7478 / (1.0 - theta);
            } else {
                throw ValueError("Polynomial orders < 0 or > 5 are not supported");
            }
        }

        if(order==0):         return0;  elif(order==1):         returnmax(order,exp(-0.7469*log(tau)+0.3752));  elif(order==2):         returnmax(order,exp(-0.8363*log(tau)+1.1127));  elif(order==3):         returnmax(order,exp(-0.8753*log(tau)+1.5427));  elif(order==4):         returnmax(order,exp(-0.897*log(tau)+1.8462));  else:         returnmax(order,exp(-0.9108*log(tau)+2.0805)); nUnitLastVRF (const int order, const double tau) {
            if (order == 0) {
                return 0;
            } else if (order == 1) {
                return max(order, exp( - 0.7469 * log(tau) + 0.3752));
            } else if (order == 2) {
                return max(order, exp( - 0.8363 * log(tau) + 1.1127));
            } else if (order == 3) {
                return max(order, exp( - 0.8753 * log(tau) + 1.5427));
            } else if (order == 4) {
                return max(order, exp( - 0.897 * log(tau) + 1.8462));
            } else {
                return max(order, exp( - 0.9108 * log(tau) + 2.0805));
            }
        }

        std::shared_ptr<ICore> makeEmpCore (const int order, const double tau) {
            if (order == 0) {
                return std::make_shared<CoreEmp0>(tau);
            } else if (order == 1) {
                return std::make_shared<CoreEmp1>(tau);
            } else if (order == 2) {
                return std::make_shared<CoreEmp2>(tau);
            } else if (order == 3) {
                return std::make_shared<CoreEmp3>(tau);
            } else if (order == 4) {
                return std::make_shared<CoreEmp4>(tau);
            } else {
                return std::make_shared<CoreEmp5>(tau);
            }
        }

        std::shared_ptr<RecursivePolynomialFilter> makeEmp (const int order, const double tau) {
            std::shared_ptr<ICore> core;
            core = makeEmpCore(order, tau);
            return std::make_shared<RecursivePolynomialFilter>(order, tau, core);
        }

    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)