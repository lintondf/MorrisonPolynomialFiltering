/***** /polynomialfiltering/components/Emp/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */

#include "polynomialfiltering/components/Emp.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        using namespace Eigen;
        
            int CoreEmp0::order;
            double CoreEmp0::tau;
            CoreEmp0::CoreEmp0 (const double tau) {
                this->order = 0;
                this->tau = tau;
            }

            int CoreEmp0::getSamplesToStart () {
                return this->order + 2;
            }

            RealVector CoreEmp0::getGamma (const double n, const double dtau) {
                RealVector g(1);
                g = (RealVector1() << 1.0 / (1.0 + n)).finished();
                return g;
            }

            double CoreEmp0::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp0::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealMatrix CoreEmp0::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp0::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp0::_getFirstVRF (const double n, const double tau) {
                return 1.0 / (n + 1.0);
            }

            double CoreEmp0::_getLastVRF (const double n, const double tau) {
                return 1.0 / (n + 1.0);
            }

            RealMatrix CoreEmp0::_getDiagonalVRF (const double n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp0::_getVRF (const double n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                return V;
            }

            int CoreEmp1::order;
            double CoreEmp1::tau;
            CoreEmp1::CoreEmp1 (const double tau) {
                this->order = 1;
                this->tau = tau;
            }

            int CoreEmp1::getSamplesToStart () {
                return this->order + 2;
            }

            RealVector CoreEmp1::getGamma (const double n, const double dtau) {
                double denom;
                RealVector g(2);
                denom = 1.0 / ((n + 2) * (n + 1));
                g = (RealVector2() << 2.0 * (2.0 * n + 1.0), 6.0).finished();
                return denom * g;
            }

            double CoreEmp1::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp1::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealMatrix CoreEmp1::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp1::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp1::_getFirstVRF (const double n, const double tau) {
                return 2.0 * (2.0 * n + 3.0) / (n * (n + 1.0));
            }

            double CoreEmp1::_getLastVRF (const double n, const double tau) {
                return 12.0 / (n * pow(tau, 2) * (n + 1.0) * (n + 2.0));
            }

            RealMatrix CoreEmp1::_getDiagonalVRF (const double n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp1::_getVRF (const double n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 6.0 / (n * tau * (n + 1.0));
                V(1, 0) = V(0, 1);
                return V;
            }

            int CoreEmp2::order;
            double CoreEmp2::tau;
            CoreEmp2::CoreEmp2 (const double tau) {
                this->order = 2;
                this->tau = tau;
            }

            int CoreEmp2::getSamplesToStart () {
                return this->order + 2;
            }

            RealVector CoreEmp2::getGamma (const double n, const double dtau) {
                double n2;
                double denom;
                RealVector g(3);
                n2 = n * n;
                denom = 1.0 / ((n + 3) * (n + 2) * (n + 1));
                g = (RealVector3() << 3.0 * (3.0 * n2 + 3.0 * n + 2.0), 18.0 * (2.0 * n + 1.0), (2.0 * 1.0) * 30.0).finished();
                return denom * g;
            }

            double CoreEmp2::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp2::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealMatrix CoreEmp2::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp2::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp2::_getFirstVRF (const double n, const double tau) {
                return 3.0 * (3.0 * pow(n, 2) + 9.0 * n + 8.0) / (n * (pow(n, 2) - 1.0));
            }

            double CoreEmp2::_getLastVRF (const double n, const double tau) {
                return 720.0 / (n * pow(tau, 4) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0));
            }

            RealMatrix CoreEmp2::_getDiagonalVRF (const double n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = 12.0 * ((n - 1.0) * (n + 3.0) + 15.0 * pow((n + 2.0), 2)) / (n * pow(tau, 2) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0));
                V(2, 2) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp2::_getVRF (const double n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 18.0 * (2.0 * n + 3.0) / (n * tau * (pow(n, 2) - 1.0));
                V(1, 0) = V(0, 1);
                V(0, 2) = 60.0 / (n * pow(tau, 2) * (pow(n, 2) - 1.0));
                V(2, 0) = V(0, 2);
                V(1, 2) = 360.0 / (n * pow(tau, 3) * (n - 1.0) * (n + 1.0) * (n + 3.0));
                V(2, 1) = V(1, 2);
                return V;
            }

            int CoreEmp3::order;
            double CoreEmp3::tau;
            CoreEmp3::CoreEmp3 (const double tau) {
                this->order = 3;
                this->tau = tau;
            }

            int CoreEmp3::getSamplesToStart () {
                return this->order + 2;
            }

            RealVector CoreEmp3::getGamma (const double n, const double dtau) {
                double n2;
                double n3;
                double denom;
                RealVector g(4);
                n2 = n * n;
                n3 = n2 * n;
                denom = 1.0 / ((n + 4) * (n + 3) * (n + 2) * (n + 1));
                g = (RealVector4() << 8.0 * (2.0 * n3 + 3.0 * n2 + 7.0 * n + 3.0), 20.0 * (6.0 * n2 + 6.0 * n + 5.0), (2.0 * 1.0) * 120.0 * (2.0 * n + 1.0), (3.0 * 2.0 * 1.0) * 140.0).finished();
                return denom * g;
            }

            double CoreEmp3::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp3::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealMatrix CoreEmp3::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp3::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp3::_getFirstVRF (const double n, const double tau) {
                return 8.0 * (2.0 * pow(n, 3) + 9.0 * pow(n, 2) + 19.0 * n + 15.0) / (n * (pow(n, 3) - 2.0 * pow(n, 2) - n + 2.0));
            }

            double CoreEmp3::_getLastVRF (const double n, const double tau) {
                return 100800.0 / (n * pow(tau, 6) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0));
            }

            RealMatrix CoreEmp3::_getDiagonalVRF (const double n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = 200.0 * (6.0 * pow(n, 4) + 51.0 * pow(n, 3) + 159.0 * pow(n, 2) + 219.0 * n + 116.0) / (n * pow(tau, 2) * (pow(n, 6) + 7.0 * pow(n, 5) + 7.0 * pow(n, 4) - 35.0 * pow(n, 3) - 56.0 * pow(n, 2) + 28.0 * n + 48.0));
                V(2, 2) = 720.0 * ((n - 2.0) * (n + 4.0) + 35.0 * pow((n + 2.0), 2)) / (n * pow(tau, 4) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0));
                V(3, 3) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp3::_getVRF (const double n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 20.0 * (6.0 * pow(n, 2) + 18.0 * n + 17.0) / (n * tau * (pow(n, 3) - 2.0 * pow(n, 2) - n + 2.0));
                V(1, 0) = V(0, 1);
                V(0, 2) = 240.0 * (2.0 * n + 3.0) / (n * pow(tau, 2) * (pow(n, 3) - 2.0 * pow(n, 2) - n + 2.0));
                V(2, 0) = V(0, 2);
                V(0, 3) = 840.0 / (n * pow(tau, 3) * (pow(n, 3) - 2.0 * pow(n, 2) - n + 2.0));
                V(3, 0) = V(0, 3);
                V(1, 2) = 600.0 * (9.0 * pow(n, 2) + 39.0 * n + 40.0) / (n * pow(tau, 3) * (pow(n, 5) + 5.0 * pow(n, 4) - 3.0 * pow(n, 3) - 29.0 * pow(n, 2) + 2.0 * n + 24.0));
                V(2, 1) = V(1, 2);
                V(1, 3) = 1680.0 * (6.0 * pow(n, 2) + 27.0 * n + 32.0) / (n * pow(tau, 4) * (pow(n, 6) + 7.0 * pow(n, 5) + 7.0 * pow(n, 4) - 35.0 * pow(n, 3) - 56.0 * pow(n, 2) + 28.0 * n + 48.0));
                V(3, 1) = V(1, 3);
                V(2, 3) = 50400.0 / (n * pow(tau, 5) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 3.0) * (n + 4.0));
                V(3, 2) = V(2, 3);
                return V;
            }

            int CoreEmp4::order;
            double CoreEmp4::tau;
            CoreEmp4::CoreEmp4 (const double tau) {
                this->order = 4;
                this->tau = tau;
            }

            int CoreEmp4::getSamplesToStart () {
                return this->order + 2;
            }

            RealVector CoreEmp4::getGamma (const double n, const double dtau) {
                double n2;
                double n3;
                double n4;
                double denom;
                RealVector g(5);
                n2 = n * n;
                n3 = n2 * n;
                n4 = n2 * n2;
                denom = 1.0 / ((n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1));
                g = (RealVector5() << 5.0 * (5.0 * n4 + 10.0 * n3 + 55.0 * n2 + 50.0 * n + 24.0), 25.0 * (12.0 * n3 + 18.0 * n2 + 46.0 * n + 20.0), (2.0 * 1.0) * 1050.0 * (n2 + n + 1.0), (3.0 * 2.0 * 1.0) * 700.0 * (2.0 * n + 1.0), (4.0 * 3.0 * 2.0 * 1.0) * 630.0).finished();
                return denom * g;
            }

            double CoreEmp4::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp4::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealMatrix CoreEmp4::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp4::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp4::_getFirstVRF (const double n, const double tau) {
                return 5.0 * (5.0 * pow(n, 4) + 30.0 * pow(n, 3) + 115.0 * pow(n, 2) + 210.0 * n + 144.0) / (n * (pow(n, 4) - 5.0 * pow(n, 3) + 5.0 * pow(n, 2) + 5.0 * n - 6.0));
            }

            double CoreEmp4::_getLastVRF (const double n, const double tau) {
                return 25401600.0 / (n * pow(tau, 8) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0) * (n + 5.0));
            }

            RealMatrix CoreEmp4::_getDiagonalVRF (const double n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = 100.0 * (48.0 * pow(n, 6) + 666.0 * pow(n, 5) + 3843.0 * pow(n, 4) + 11982.0 * pow(n, 3) + 21727.0 * pow(n, 2) + 21938.0 * n + 9516.0) / (n * pow(tau, 2) * (pow(n, 8) + 9.0 * pow(n, 7) + 6.0 * pow(n, 6) - 126.0 * pow(n, 5) - 231.0 * pow(n, 4) + 441.0 * pow(n, 3) + 944.0 * pow(n, 2) - 324.0 * n - 720.0));
                V(2, 2) = 35280.0 * (9.0 * pow(n, 4) + 76.0 * pow(n, 3) + 239.0 * pow(n, 2) + 336.0 * n + 185.0) / (n * pow(tau, 4) * (pow(n, 8) + 9.0 * pow(n, 7) + 6.0 * pow(n, 6) - 126.0 * pow(n, 5) - 231.0 * pow(n, 4) + 441.0 * pow(n, 3) + 944.0 * pow(n, 2) - 324.0 * n - 720.0));
                V(3, 3) = 100800.0 * ((n - 3.0) * (n + 5.0) + 63.0 * pow((n + 2.0), 2)) / (n * pow(tau, 6) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0) * (n + 5.0));
                V(4, 4) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp4::_getVRF (const double n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 50.0 * (6.0 * pow(n, 3) + 27.0 * pow(n, 2) + 59.0 * n + 48.0) / (n * tau * (pow(n, 4) - 5.0 * pow(n, 3) + 5.0 * pow(n, 2) + 5.0 * n - 6.0));
                V(1, 0) = V(0, 1);
                V(0, 2) = 2100.0 * (pow(n, 2) + 3.0 * n + 3.0) / (n * pow(tau, 2) * (pow(n, 4) - 5.0 * pow(n, 3) + 5.0 * pow(n, 2) + 5.0 * n - 6.0));
                V(2, 0) = V(0, 2);
                V(0, 3) = 4200.0 * (2.0 * n + 3.0) / (n * pow(tau, 3) * (pow(n, 4) - 5.0 * pow(n, 3) + 5.0 * pow(n, 2) + 5.0 * n - 6.0));
                V(3, 0) = V(0, 3);
                V(0, 4) = 15120.0 / (n * pow(tau, 4) * (pow(n, 4) - 5.0 * pow(n, 3) + 5.0 * pow(n, 2) + 5.0 * n - 6.0));
                V(4, 0) = V(0, 4);
                V(1, 2) = 4200.0 * (9.0 * pow(n, 4) + 84.0 * pow(n, 3) + 295.0 * pow(n, 2) + 467.0 * n + 297.0) / (n * pow(tau, 3) * (pow(n, 7) + 7.0 * pow(n, 6) - 8.0 * pow(n, 5) - 110.0 * pow(n, 4) - 11.0 * pow(n, 3) + 463.0 * pow(n, 2) + 18.0 * n - 360.0));
                V(2, 1) = V(1, 2);
                V(1, 3) = 1680.0 * (96.0 * pow(n, 4) + 894.0 * pow(n, 3) + 3191.0 * pow(n, 2) + 5059.0 * n + 2940.0) / (n * pow(tau, 4) * (pow(n, 8) + 9.0 * pow(n, 7) + 6.0 * pow(n, 6) - 126.0 * pow(n, 5) - 231.0 * pow(n, 4) + 441.0 * pow(n, 3) + 944.0 * pow(n, 2) - 324.0 * n - 720.0));
                V(3, 1) = V(1, 3);
                V(1, 4) = 151200.0 * (2.0 * pow(n, 2) + 11.0 * n + 19.0) / (n * pow(tau, 5) * (pow(n, 7) + 7.0 * pow(n, 6) - 8.0 * pow(n, 5) - 110.0 * pow(n, 4) - 11.0 * pow(n, 3) + 463.0 * pow(n, 2) + 18.0 * n - 360.0));
                V(4, 1) = V(1, 4);
                V(2, 3) = 352800.0 * (4.0 * pow(n, 2) + 17.0 * n + 18.0) / (n * pow(tau, 5) * (pow(n, 7) + 7.0 * pow(n, 6) - 8.0 * pow(n, 5) - 110.0 * pow(n, 4) - 11.0 * pow(n, 3) + 463.0 * pow(n, 2) + 18.0 * n - 360.0));
                V(3, 2) = V(2, 3);
                V(2, 4) = 302400.0 * (9.0 * pow(n, 2) + 39.0 * n + 47.0) / (n * pow(tau, 6) * (pow(n, 8) + 9.0 * pow(n, 7) + 6.0 * pow(n, 6) - 126.0 * pow(n, 5) - 231.0 * pow(n, 4) + 441.0 * pow(n, 3) + 944.0 * pow(n, 2) - 324.0 * n - 720.0));
                V(4, 2) = V(2, 4);
                V(3, 4) = 12700800.0 / (n * pow(tau, 7) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 3.0) * (n + 4.0) * (n + 5.0));
                V(4, 3) = V(3, 4);
                return V;
            }

            int CoreEmp5::order;
            double CoreEmp5::tau;
            CoreEmp5::CoreEmp5 (const double tau) {
                this->order = 5;
                this->tau = tau;
            }

            int CoreEmp5::getSamplesToStart () {
                return this->order + 2;
            }

            RealVector CoreEmp5::getGamma (const double n, const double dtau) {
                double n2;
                double n3;
                double n4;
                double denom;
                RealVector g(6);
                n2 = n * n;
                n3 = n2 * n;
                n4 = n2 * n2;
                denom = 1.0 / ((n + 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1));
                g = (RealVector6() << 6.0 * (2.0 * n + 1.0) * (3.0 * n4 + 6.0 * n3 + 77.0 * n2 + 74.0 * n + 120.0), 126.0 * (5.0 * n4 + 10.0 * n3 + 55.0 * n2 + 50.0 * n + 28.0), (2.0 * 1.0) * 420.0 * (2.0 * n + 1.0) * (4.0 * n2 + 4.0 * n + 15.0), (3.0 * 2.0 * 1.0) * 1260.0 * (6.0 * n2 + 6.0 * n + 7.0), (4.0 * 3.0 * 2.0 * 1.0) * 3780.0 * (2.0 * n + 1.0), (5.0 * 4.0 * 3.0 * 2.0 * 1.0) * 2772.0).finished();
                return denom * g;
            }

            double CoreEmp5::getFirstVRF (const int n) {
                return this->_getFirstVRF(n, this->tau);
            }

            double CoreEmp5::getLastVRF (const int n) {
                return this->_getLastVRF(n, this->tau);
            }

            RealMatrix CoreEmp5::getDiagonalVRF (const int n) {
                return this->_getDiagonalVRF(n, this->tau);
            }

            RealMatrix CoreEmp5::getVRF (const int n) {
                return this->_getVRF(n, this->tau);
            }

            double CoreEmp5::_getFirstVRF (const double n, const double tau) {
                return 6.0 * (6.0 * pow(n, 5) + 45.0 * pow(n, 4) + 280.0 * pow(n, 3) + 855.0 * pow(n, 2) + 1334.0 * n + 840.0) / (n * (pow(n, 5) - 9.0 * pow(n, 4) + 25.0 * pow(n, 3) - 15.0 * pow(n, 2) - 26.0 * n + 24.0));
            }

            double CoreEmp5::_getLastVRF (const double n, const double tau) {
                return 10059033600.0 / (n * pow(tau, 10.0) * (n - 4.0) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0) * (n + 5.0) * (n + 6.0));
            }

            RealMatrix CoreEmp5::_getDiagonalVRF (const double n, const double tau) {
                RealMatrix V;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                V(0, 0) = this->_getFirstVRF(n, tau);
                V(1, 1) = 588.0 * (25.0 * pow(n, 8) + 500.0 * pow(n, 7) + 4450.0 * pow(n, 6) + 23300.0 * pow(n, 5) + 79585.0 * pow(n, 4) + 181760.0 * pow(n, 3) + 267180.0 * pow(n, 2) + 226920.0 * n + 84528.0) / (n * pow(tau, 2) * (pow(n, 10.0) + 11.0 * pow(n, 9) - 330.0 * pow(n, 7) - 627.0 * pow(n, 6) + 3003.0 * pow(n, 5) + 7370.0 * pow(n, 4) - 9020.0 * pow(n, 3) - 24024.0 * pow(n, 2) + 6336.0 * n + 17280.0));
                V(2, 2) = 70560.0 * (32.0 * pow(n, 6) + 432.0 * pow(n, 5) + 2480.0 * pow(n, 4) + 7800.0 * pow(n, 3) + 14418.0 * pow(n, 2) + 14963.0 * n + 6690.0) / (n * pow(tau, 4) * (pow(n, 10.0) + 11.0 * pow(n, 9) - 330.0 * pow(n, 7) - 627.0 * pow(n, 6) + 3003.0 * pow(n, 5) + 7370.0 * pow(n, 4) - 9020.0 * pow(n, 3) - 24024.0 * pow(n, 2) + 6336.0 * n + 17280.0));
                V(3, 3) = 2721600.0 * (48.0 * pow(n, 4) + 402.0 * pow(n, 3) + 1274.0 * pow(n, 2) + 1828.0 * n + 1047.0) / (n * pow(tau, 6) * (pow(n, 10.0) + 11.0 * pow(n, 9) - 330.0 * pow(n, 7) - 627.0 * pow(n, 6) + 3003.0 * pow(n, 5) + 7370.0 * pow(n, 4) - 9020.0 * pow(n, 3) - 24024.0 * pow(n, 2) + 6336.0 * n + 17280.0));
                V(4, 4) = 25401600.0 * ((n - 4.0) * (n + 6.0) + 99.0 * pow((n + 2.0), 2)) / (n * pow(tau, 8) * (n - 4.0) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0) * (n + 5.0) * (n + 6.0));
                V(5, 5) = this->_getLastVRF(n, tau);
                return V;
            }

            RealMatrix CoreEmp5::_getVRF (const double n, const double tau) {
                RealMatrix V;
                V = this->_getDiagonalVRF(n, tau);
                V(0, 1) = 126.0 * (5.0 * pow(n, 4) + 30.0 * pow(n, 3) + 115.0 * pow(n, 2) + 210.0 * n + 148.0) / (n * tau * (pow(n, 5) - 9.0 * pow(n, 4) + 25.0 * pow(n, 3) - 15.0 * pow(n, 2) - 26.0 * n + 24.0));
                V(1, 0) = V(0, 1);
                V(0, 2) = 840.0 * (8.0 * pow(n, 3) + 36.0 * pow(n, 2) + 82.0 * n + 69.0) / (n * pow(tau, 2) * (pow(n, 5) - 9.0 * pow(n, 4) + 25.0 * pow(n, 3) - 15.0 * pow(n, 2) - 26.0 * n + 24.0));
                V(2, 0) = V(0, 2);
                V(0, 3) = 7560.0 * (6.0 * pow(n, 2) + 18.0 * n + 19.0) / (n * pow(tau, 3) * (pow(n, 5) - 9.0 * pow(n, 4) + 25.0 * pow(n, 3) - 15.0 * pow(n, 2) - 26.0 * n + 24.0));
                V(3, 0) = V(0, 3);
                V(0, 4) = 90720.0 * (2.0 * n + 3.0) / (n * pow(tau, 4) * (pow(n, 5) - 9.0 * pow(n, 4) + 25.0 * pow(n, 3) - 15.0 * pow(n, 2) - 26.0 * n + 24.0));
                V(4, 0) = V(0, 4);
                V(0, 5) = 332640.0 / (n * pow(tau, 5) * (pow(n, 5) - 9.0 * pow(n, 4) + 25.0 * pow(n, 3) - 15.0 * pow(n, 2) - 26.0 * n + 24.0));
                V(5, 0) = V(0, 5);
                V(1, 2) = 17640.0 * (10.0 * pow(n, 6) + 150.0 * pow(n, 5) + 965.0 * pow(n, 4) + 3420.0 * pow(n, 3) + 7179.0 * pow(n, 2) + 8520.0 * n + 4356.0) / (n * pow(tau, 3) * (pow(n, 9) + 9.0 * pow(n, 8) - 18.0 * pow(n, 7) - 294.0 * pow(n, 6) - 39.0 * pow(n, 5) + 3081.0 * pow(n, 4) + 1208.0 * pow(n, 3) - 11436.0 * pow(n, 2) - 1152.0 * n + 8640.0));
                V(2, 1) = V(1, 2);
                V(1, 3) = 105840.0 * (12.0 * pow(n, 6) + 177.0 * pow(n, 5) + 1125.0 * pow(n, 4) + 3870.0 * pow(n, 3) + 7550.0 * pow(n, 2) + 7954.0 * n + 3588.0) / (n * pow(tau, 4) * (pow(n, 10.0) + 11.0 * pow(n, 9) - 330.0 * pow(n, 7) - 627.0 * pow(n, 6) + 3003.0 * pow(n, 5) + 7370.0 * pow(n, 4) - 9020.0 * pow(n, 3) - 24024.0 * pow(n, 2) + 6336.0 * n + 17280.0));
                V(3, 1) = V(1, 3);
                V(1, 4) = 211680.0 * (25.0 * pow(n, 4) + 270.0 * pow(n, 3) + 1205.0 * pow(n, 2) + 2400.0 * n + 1692.0) / (n * pow(tau, 5) * (pow(n, 9) + 9.0 * pow(n, 8) - 18.0 * pow(n, 7) - 294.0 * pow(n, 6) - 39.0 * pow(n, 5) + 3081.0 * pow(n, 4) + 1208.0 * pow(n, 3) - 11436.0 * pow(n, 2) - 1152.0 * n + 8640.0));
                V(4, 1) = V(1, 4);
                V(1, 5) = 665280.0 * (15.0 * pow(n, 4) + 165.0 * pow(n, 3) + 770.0 * pow(n, 2) + 1630.0 * n + 1284.0) / (n * pow(tau, 6) * (pow(n, 10.0) + 11.0 * pow(n, 9) - 330.0 * pow(n, 7) - 627.0 * pow(n, 6) + 3003.0 * pow(n, 5) + 7370.0 * pow(n, 4) - 9020.0 * pow(n, 3) - 24024.0 * pow(n, 2) + 6336.0 * n + 17280.0));
                V(5, 1) = V(1, 5);
                V(2, 3) = 1058400.0 * (16.0 * pow(n, 4) + 144.0 * pow(n, 3) + 506.0 * pow(n, 2) + 822.0 * n + 549.0) / (n * pow(tau, 5) * (pow(n, 9) + 9.0 * pow(n, 8) - 18.0 * pow(n, 7) - 294.0 * pow(n, 6) - 39.0 * pow(n, 5) + 3081.0 * pow(n, 4) + 1208.0 * pow(n, 3) - 11436.0 * pow(n, 2) - 1152.0 * n + 8640.0));
                V(3, 2) = V(2, 3);
                V(2, 4) = 604800.0 * (120.0 * pow(n, 4) + 1068.0 * pow(n, 3) + 3766.0 * pow(n, 2) + 6047.0 * n + 3594.0) / (n * pow(tau, 6) * (pow(n, 10.0) + 11.0 * pow(n, 9) - 330.0 * pow(n, 7) - 627.0 * pow(n, 6) + 3003.0 * pow(n, 5) + 7370.0 * pow(n, 4) - 9020.0 * pow(n, 3) - 24024.0 * pow(n, 2) + 6336.0 * n + 17280.0));
                V(4, 2) = V(2, 4);
                V(2, 5) = 139708800.0 * (pow(n, 2) + 5.0 * n + 9.0) / (n * pow(tau, 7) * (pow(n, 9) + 9.0 * pow(n, 8) - 18.0 * pow(n, 7) - 294.0 * pow(n, 6) - 39.0 * pow(n, 5) + 3081.0 * pow(n, 4) + 1208.0 * pow(n, 3) - 11436.0 * pow(n, 2) - 1152.0 * n + 8640.0));
                V(5, 2) = V(2, 5);
                V(3, 4) = 114307200.0 * (5.0 * pow(n, 2) + 21.0 * n + 23.0) / (n * pow(tau, 7) * (pow(n, 9) + 9.0 * pow(n, 8) - 18.0 * pow(n, 7) - 294.0 * pow(n, 6) - 39.0 * pow(n, 5) + 3081.0 * pow(n, 4) + 1208.0 * pow(n, 3) - 11436.0 * pow(n, 2) - 1152.0 * n + 8640.0));
                V(4, 3) = V(3, 4);
                V(3, 5) = 279417600.0 * (4.0 * pow(n, 2) + 17.0 * n + 21.0) / (n * pow(tau, 8) * (pow(n, 10.0) + 11.0 * pow(n, 9) - 330.0 * pow(n, 7) - 627.0 * pow(n, 6) + 3003.0 * pow(n, 5) + 7370.0 * pow(n, 4) - 9020.0 * pow(n, 3) - 24024.0 * pow(n, 2) + 6336.0 * n + 17280.0));
                V(5, 3) = V(3, 5);
                V(4, 5) = 5029516800.0 / (n * pow(tau, 9) * (n - 4.0) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 3.0) * (n + 4.0) * (n + 5.0) * (n + 6.0));
                V(5, 4) = V(4, 5);
                return V;
            }

        double nSwitch (const int order, const double theta) {
            if (1.0 - theta <= 0.0) {
                return 0.0;
            }
            if (order == 0) {
                return 2.0 / (1.0 - theta);
            } else if (order == 1.0) {
                return 3.2 / (1.0 - theta);
            } else if (order == 2.0) {
                return 4.3636 / (1.0 - theta);
            } else if (order == 3.0) {
                return 5.50546 / (1.0 - theta);
            } else if (order == 4.0) {
                return 6.6321 / (1.0 - theta);
            } else if (order == 5.0) {
                return 7.7478 / (1.0 - theta);
            } else {
                throw ValueError("Polynomial orders < 0.0 or > 5.0 are not supported");
            }
        }

        int nUnitLastVRF (const int order, const double tau) {
            if (order == 0) {
                return 1 + 0;
            } else if (order == 1.0) {
                return 1 + int(max(order, exp( - 0.7469 * log(tau) + 0.3752)));
            } else if (order == 2.0) {
                return 1 + int(max(order, exp( - 0.8363 * log(tau) + 1.1127)));
            } else if (order == 3.0) {
                return 1 + int(max(order, exp( - 0.8753 * log(tau) + 1.5427)));
            } else if (order == 4.0) {
                return 1 + int(max(order, exp( - 0.897 * log(tau) + 1.8462)));
            } else {
                return 1 + int(max(order, exp( - 0.9108 * log(tau) + 2.0805)));
            }
        }

        std::shared_ptr<ICore> _makeEmpCore (const int order, const double tau) {
            if (order == 0) {
                return std::make_shared<CoreEmp0>(tau);
            } else if (order == 1.0) {
                return std::make_shared<CoreEmp1>(tau);
            } else if (order == 2.0) {
                return std::make_shared<CoreEmp2>(tau);
            } else if (order == 3.0) {
                return std::make_shared<CoreEmp3>(tau);
            } else if (order == 4.0) {
                return std::make_shared<CoreEmp4>(tau);
            } else {
                return std::make_shared<CoreEmp5>(tau);
            }
        }

        std::shared_ptr<RecursivePolynomialFilter> makeEmp (const int order, const double tau) {
            std::shared_ptr<ICore> core;
            core = _makeEmpCore(order, tau);
            return std::make_shared<RecursivePolynomialFilter>(order, tau, core);
        }

    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)