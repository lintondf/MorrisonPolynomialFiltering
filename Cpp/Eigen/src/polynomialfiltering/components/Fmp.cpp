/***** /polynomialfiltering/components/Fmp/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */

#include "polynomialfiltering/components/Fmp.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        using namespace Eigen;
        
            double AbstractCoreFmp::theta;
            RealMatrix AbstractCoreFmp::VRF;
            AbstractCoreFmp::AbstractCoreFmp (const double tau, const double theta) {
                this->theta = theta;
            }

            RealMatrix AbstractCoreFmp::getVRF (const int n) {
                return this->VRF;
            }

            double AbstractCoreFmp::getFirstVRF (const int n) {
                return this->VRF(0, 0);
            }

            double AbstractCoreFmp::getLastVRF (const int n) {
                return this->VRF(VRF->rows()-1, VRF->columns()-1);
            }

            RealMatrix AbstractCoreFmp::getDiagonalVRF (const int n) {
                return diag(diag(this->VRF));
            }

            CoreFmp0::CoreFmp0 (const double tau, const double theta) : AbstractCoreFmp(tau,theta) {
                this->VRF = this->_getVRF(tau, theta);
            }

            RealVector CoreFmp0::getGamma (const double time, const double dtau) {
                return (RealVector1() << 1. - this->theta).finished();
            }

            RealMatrix CoreFmp0::_getVRF (const double u, const double t) {
                RealMatrix V;
                V = ArrayXXd::Zero(0 + 1, 0 + 1);
                V(0, 0) = ( - t + 1.0) / (t + 1.0);
                return V;
            }

            CoreFmp1::CoreFmp1 (const double tau, const double theta) : AbstractCoreFmp(tau,theta) {
                this->VRF = this->_getVRF(tau, theta);
            }

            RealVector CoreFmp1::getGamma (const double time, const double dtau) {
                double t2;
                double mt2;
                double t;
                t = this->theta;
                t2 = t * t;
                mt2 = (1 - t) * (1 - t);
                return (RealVector2() << 1. - t2, mt2).finished();
            }

            RealMatrix CoreFmp1::_getVRF (const double u, const double t) {
                RealMatrix V;
                V = ArrayXXd::Zero(1 + 1, 1 + 1);
                V(0, 0) = ( - 5.0 * pow(t, 3) + pow(t, 2) + 3.0 * t + 1.0) / (pow(t, 3) + 3.0 * pow(t, 2) + 3.0 * t + 1.0);
                V(0, 1) = pow((t - 1.0), 2) * (3.0 * t + 1.0) / (u * pow((t + 1.0), 3));
                V(1, 0) = V(0, 1);
                V(1, 1) = 2.0 * pow(( - t + 1.0), 3) / (pow(u, 2) * pow((t + 1.0), 3));
                return V;
            }

            CoreFmp2::CoreFmp2 (const double tau, const double theta) : AbstractCoreFmp(tau,theta) {
                this->VRF = this->_getVRF(tau, theta);
            }

            RealVector CoreFmp2::getGamma (const double time, const double dtau) {
                double t;
                t = this->theta;
                double t2;
                double t3;
                double mt2;
                double mt3;
                t2 = t * t;
                t3 = t2 * t;
                mt2 = (1 - t) * (1 - t);
                mt3 = (1 - t) * mt2;
                return (RealVector3() << 1. - t3, 3.0 / 2.0 * mt2 * (1. + t), (2. * 1.) * 1.0 / 2.0 * mt3).finished();
            }

            RealMatrix CoreFmp2::_getVRF (const double u, const double t) {
                RealMatrix V;
                V = ArrayXXd::Zero(2 + 1, 2 + 1);
                V(0, 0) = ( - 19.0 * pow(t, 5) - 5.0 * pow(t, 4) + 8.0 * pow(t, 3) + 10.0 * pow(t, 2) + 5.0 * t + 1.0) / (pow(t, 5) + 5.0 * pow(t, 4) + 10.0 * pow(t, 3) + 10.0 * pow(t, 2) + 5.0 * t + 1.0);
                V(0, 1) = (3.0 / 2.0) * (14.0 * pow(t, 5) - 13.0 * pow(t, 4) - 10.0 * pow(t, 3) + 4.0 * pow(t, 2) + 4.0 * t + 1.0) / (u * (pow(t, 5) + 5.0 * pow(t, 4) + 10.0 * pow(t, 3) + 10.0 * pow(t, 2) + 5.0 * t + 1.0));
                V(1, 0) = V(0, 1);
                V(0, 2) =  - pow((t - 1.0), 3) * (6.0 * pow(t, 2) + 3.0 * t * (t + 1.0) + pow((t + 1.0), 2)) / (pow(u, 2) * pow((t + 1.0), 5));
                V(2, 0) = V(0, 2);
                V(1, 1) =  - 1.0 / 2.0 * (49.0 * pow(t, 5) - 97.0 * pow(t, 4) + 10.0 * pow(t, 3) + 62.0 * pow(t, 2) - 11.0 * t - 13.0) / (pow(u, 2) * (pow(t, 5) + 5.0 * pow(t, 4) + 10.0 * pow(t, 3) + 10.0 * pow(t, 2) + 5.0 * t + 1.0));
                V(1, 2) = 3.0 * pow((t - 1.0), 3) * ( - ( - t + 1.0) * (3.0 * t + 1.0) + (t - 1.0) * (t + 1.0)) / (pow(u, 3) * pow((t + 1.0), 5));
                V(2, 1) = V(1, 2);
                V(2, 2) = 6.0 * pow(( - t + 1.0), 5) / (pow(u, 4) * pow((t + 1.0), 5));
                return V;
            }

            CoreFmp3::CoreFmp3 (const double tau, const double theta) : AbstractCoreFmp(tau,theta) {
                this->VRF = this->_getVRF(tau, theta);
            }

            RealVector CoreFmp3::getGamma (const double time, const double dtau) {
                double t;
                t = this->theta;
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
                return (RealVector4() << 1. - t4, 1.0 / 6.0 * mt2 * (11. + 14. * t + 11. * t2), (2. * 1.) * mt3 * (1. + t), (3. * 2. * 1.) * 1.0 / 6.0 * mt4).finished();
            }

            RealMatrix CoreFmp3::_getVRF (const double u, const double t) {
                RealMatrix V;
                V = ArrayXXd::Zero(3 + 1, 3 + 1);
                V(0, 0) = ( - 69.0 * pow(t, 7) - 35.0 * pow(t, 6) + 7.0 * pow(t, 5) + 33.0 * pow(t, 4) + 35.0 * pow(t, 3) + 21.0 * pow(t, 2) + 7.0 * t + 1.0) / (pow(t, 7) + 7.0 * pow(t, 6) + 21.0 * pow(t, 5) + 35.0 * pow(t, 4) + 35.0 * pow(t, 3) + 21.0 * pow(t, 2) + 7.0 * t + 1.0);
                V(0, 1) = (1.0 / 6.0) * (625.0 * pow(t, 7) - 289.0 * pow(t, 6) - 541.0 * pow(t, 5) - 211.0 * pow(t, 4) + 167.0 * pow(t, 3) + 169.0 * pow(t, 2) + 69.0 * t + 11.0) / (u * (pow(t, 7) + 7.0 * pow(t, 6) + 21.0 * pow(t, 5) + 35.0 * pow(t, 4) + 35.0 * pow(t, 3) + 21.0 * pow(t, 2) + 7.0 * t + 1.0));
                V(1, 0) = V(0, 1);
                V(0, 2) = ( - 90.0 * pow(t, 7) + 158.0 * pow(t, 6) + 10.0 * pow(t, 5) - 94.0 * pow(t, 4) - 10.0 * pow(t, 3) + 14.0 * pow(t, 2) + 10.0 * t + 2.0) / (pow(u, 2) * (pow(t, 7) + 7.0 * pow(t, 6) + 21.0 * pow(t, 5) + 35.0 * pow(t, 4) + 35.0 * pow(t, 3) + 21.0 * pow(t, 2) + 7.0 * t + 1.0));
                V(2, 0) = V(0, 2);
                V(0, 3) = pow((t - 1.0), 4) * (20.0 * pow(t, 3) + 10.0 * pow(t, 2) * (t + 1.0) + 4.0 * t * pow((t + 1.0), 2) + pow((t + 1.0), 3)) / (pow(u, 3) * pow((t + 1.0), 7));
                V(3, 0) = V(0, 3);
                V(1, 1) = (1.0 / 18.0) * ( - 2905.0 * pow(t, 7) + 3865.0 * pow(t, 6) + 2025.0 * pow(t, 5) - 1705.0 * pow(t, 4) - 2375.0 * pow(t, 3) + 135.0 * pow(t, 2) + 695.0 * t + 265.0) / (pow(u, 2) * (pow(t, 7) + 7.0 * pow(t, 6) + 21.0 * pow(t, 5) + 35.0 * pow(t, 4) + 35.0 * pow(t, 3) + 21.0 * pow(t, 2) + 7.0 * t + 1.0));
                V(1, 2) = (5.0 / 3.0) * (85.0 * pow(t, 7) - 219.0 * pow(t, 6) + 93.0 * pow(t, 5) + 133.0 * pow(t, 4) - 57.0 * pow(t, 3) - 57.0 * pow(t, 2) + 7.0 * t + 15.0) / (pow(u, 3) * (pow(t, 7) + 7.0 * pow(t, 6) + 21.0 * pow(t, 5) + 35.0 * pow(t, 4) + 35.0 * pow(t, 3) + 21.0 * pow(t, 2) + 7.0 * t + 1.0));
                V(2, 1) = V(1, 2);
                V(1, 3) = (1.0 / 3.0) * pow((t - 1.0), 4) * (15.0 * ( - t + 1.0) * (t + 1.0) * (3.0 * t + 1.0) + 10.0 * ( - t + 1.0) * (18.0 * pow(t, 2) + 9.0 * t * ( - t + 1.0) + 2.0 * pow(( - t + 1.0), 2)) - 12.0 * (t - 1.0) * pow((t + 1.0), 2)) / (pow(u, 4) * pow((t + 1.0), 7));
                V(3, 1) = V(1, 3);
                V(2, 2) = 2.0 * pow((t - 1.0), 4) * ((t + 1.0) * (3.0 * ( - t + 1.0) * (t + 1.0) - 5.0 * (t - 1.0) * (2.0 * t + 1.0)) + 5.0 * (2.0 * t + 1.0) * (( - t + 1.0) * (t + 1.0) - 2.0 * (t - 1.0) * (2.0 * t + 1.0))) / (pow(u, 4) * pow((t + 1.0), 7));
                V(2, 3) = pow((t - 1.0), 6) * (50.0 * t + 30.0) / (pow(u, 5) * pow((t + 1.0), 7));
                V(3, 2) = V(2, 3);
                V(3, 3) = 20.0 * pow(( - t + 1.0), 7) / (pow(u, 6) * pow((t + 1.0), 7));
                return V;
            }

            CoreFmp4::CoreFmp4 (const double tau, const double theta) : AbstractCoreFmp(tau,theta) {
                this->VRF = this->_getVRF(tau, theta);
            }

            RealVector CoreFmp4::getGamma (const double time, const double dtau) {
                double t;
                t = this->theta;
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
                return (RealVector5() << 1. - t5, 5.0 / 12.0 * mt2 * (5. + 7. * t + 7. * t2 + 5. * t3), (2. * 1.) * 5.0 / 24.0 * mt3 * (7. + 10. * t + 7. * t2), (3. * 2. * 1.) * 5.0 / 12.0 * mt4 * (1. + t), (4. * 3. * 2. * 1.) * 1.0 / 24.0 * mt5).finished();
            }

            RealMatrix CoreFmp4::_getVRF (const double u, const double t) {
                RealMatrix V;
                V = ArrayXXd::Zero(4 + 1, 4 + 1);
                V(0, 0) = ( - 251.0 * pow(t, 9) - 159.0 * pow(t, 8) - 36.0 * pow(t, 7) + 66.0 * pow(t, 6) + 124.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0) / (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0);
                V(0, 1) = (5.0 / 12.0) * (1100.0 * pow(t, 9) - 182.0 * pow(t, 8) - 816.0 * pow(t, 7) - 707.0 * pow(t, 6) - 170.0 * pow(t, 5) + 285.0 * pow(t, 4) + 292.0 * pow(t, 3) + 151.0 * pow(t, 2) + 42.0 * t + 5.0) / (u * (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0));
                V(1, 0) = V(0, 1);
                V(0, 2) = (1.0 / 12.0) * ( - 6510.0 * pow(t, 9) + 8190.0 * pow(t, 8) + 4620.0 * pow(t, 7) - 2955.0 * pow(t, 6) - 4850.0 * pow(t, 5) - 425.0 * pow(t, 4) + 880.0 * pow(t, 3) + 755.0 * pow(t, 2) + 260.0 * t + 35.0) / (pow(u, 2) * (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0));
                V(2, 0) = V(0, 2);
                V(0, 3) = (5.0 / 2.0) * (154.0 * pow(t, 9) - 406.0 * pow(t, 8) + 204.0 * pow(t, 7) + 209.0 * pow(t, 6) - 136.0 * pow(t, 5) - 39.0 * pow(t, 4) - 4.0 * pow(t, 3) + 11.0 * pow(t, 2) + 6.0 * t + 1.0) / (pow(u, 3) * (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0));
                V(3, 0) = V(0, 3);
                V(0, 4) =  - pow((t - 1.0), 5) * (70.0 * pow(t, 4) + 35.0 * pow(t, 3) * (t + 1.0) + 15.0 * pow(t, 2) * pow((t + 1.0), 2) + 5.0 * t * pow((t + 1.0), 3) + pow((t + 1.0), 4)) / (pow(u, 4) * pow((t + 1.0), 9));
                V(4, 0) = V(0, 4);
                V(1, 1) = (1.0 / 72.0) * ( - 60995.0 * pow(t, 9) + 55045.0 * pow(t, 8) + 56220.0 * pow(t, 7) + 4940.0 * pow(t, 6) - 37730.0 * pow(t, 5) - 38370.0 * pow(t, 4) - 1540.0 * pow(t, 3) + 11980.0 * pow(t, 2) + 8205.0 * t + 2245.0) / (pow(u, 2) * (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0));
                V(1, 2) = (25.0 / 72.0) * (2913.0 * pow(t, 9) - 5710.0 * pow(t, 8) - 304.0 * pow(t, 7) + 3608.0 * pow(t, 6) + 2114.0 * pow(t, 5) - 1516.0 * pow(t, 4) - 1528.0 * pow(t, 3) - 184.0 * pow(t, 2) + 389.0 * t + 218.0) / (pow(u, 3) * (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0));
                V(2, 1) = V(1, 2);
                V(1, 3) =  - 1.0 / 12.0 * (8668.0 * pow(t, 9) - 28763.0 * pow(t, 8) + 24708.0 * pow(t, 7) + 9452.0 * pow(t, 6) - 16892.0 * pow(t, 5) - 858.0 * pow(t, 4) + 1148.0 * pow(t, 3) + 3292.0 * pow(t, 2) + 288.0 * t - 1043.0) / (pow(u, 4) * (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0));
                V(3, 1) = V(1, 3);
                V(1, 4) = (5.0 / 6.0) * (285.0 * pow(t, 9) - 1426.0 * pow(t, 8) + 2732.0 * pow(t, 7) - 2356.0 * pow(t, 6) + 710.0 * pow(t, 5) + 80.0 * pow(t, 4) - 4.0 * pow(t, 3) + 68.0 * pow(t, 2) - 139.0 * t + 50.0) / (pow(u, 5) * (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0));
                V(4, 1) = V(1, 4);
                V(2, 2) =  - 1.0 / 72.0 * (87647.0 * pow(t, 9) - 262227.0 * pow(t, 8) + 155652.0 * pow(t, 7) + 158508.0 * pow(t, 6) - 70518.0 * pow(t, 5) - 160482.0 * pow(t, 4) + 51492.0 * pow(t, 3) + 54348.0 * pow(t, 2) - 273.0 * t - 14147.0) / (pow(u, 4) * (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0));
                V(2, 3) = (175.0 / 3.0) * (15.0 * pow(t, 9) - 65.0 * pow(t, 8) + 91.0 * pow(t, 7) - 17.0 * pow(t, 6) - 59.0 * pow(t, 5) + 25.0 * pow(t, 4) + 25.0 * pow(t, 3) - 11.0 * pow(t, 2) - 8.0 * t + 4.0) / (pow(u, 5) * (pow(t, 9) + 9.0 * pow(t, 8) + 36.0 * pow(t, 7) + 84.0 * pow(t, 6) + 126.0 * pow(t, 5) + 126.0 * pow(t, 4) + 84.0 * pow(t, 3) + 36.0 * pow(t, 2) + 9.0 * t + 1.0));
                V(3, 2) = V(2, 3);
                V(2, 4) =  - pow((t - 1.0), 7) * (420.0 * pow(t, 2) - 280.0 * t * (t - 1.0) + (385.0 / 6.0) * pow((t - 1.0), 2) + 15.0 * pow((t + 1.0), 2) + 35.0 * (t + 1.0) * (2.0 * t + 1.0)) / (pow(u, 6) * pow((t + 1.0), 9));
                V(4, 2) = V(2, 4);
                V(3, 3) = (5.0 / 2.0) * pow((t - 1.0), 6) * ((t + 1.0) * (8.0 * ( - t + 1.0) * (t + 1.0) - 7.0 * (t - 1.0) * (5.0 * t + 3.0)) + 7.0 * (5.0 * t + 3.0) * (( - t + 1.0) * (t + 1.0) - (t - 1.0) * (5.0 * t + 3.0))) / (pow(u, 6) * pow((t + 1.0), 9));
                V(3, 4) = 35.0 * pow((t - 1.0), 7) * ( - ( - t + 1.0) * (t + 1.0) + (t - 1.0) * (5.0 * t + 3.0)) / (pow(u, 7) * pow((t + 1.0), 9));
                V(4, 3) = V(3, 4);
                V(4, 4) = 70.0 * pow(( - t + 1.0), 9) / (pow(u, 8) * pow((t + 1.0), 9));
                return V;
            }

            CoreFmp5::CoreFmp5 (const double tau, const double theta) : AbstractCoreFmp(tau,theta) {
                this->VRF = this->_getVRF(tau, theta);
            }

            RealVector CoreFmp5::getGamma (const double time, const double dtau) {
                double t;
                t = this->theta;
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
                return (RealVector6() << 1. - t6, 1.0 / 60.0 * mt2 * (137. + 202. * t + 222. * t2 + 202. * t3 + 137. * t4), 5.0 / 8.0 * mt3 * (3. + 5. * t + 5. * t2 + 3. * t3), 1.0 / 24.0 * mt4 * (17. + 26. * t + 17. * t2), 1.0 / 8.0 * mt5 * (1. + t), mt6 / 120.0).finished();
            }

            RealMatrix CoreFmp5::_getVRF (const double u, const double t) {
                RealMatrix V;
                V = ArrayXXd::Zero(5 + 1, 5 + 1);
                V(0, 0) = ( - 923.0 * pow(t, 11) - 649.0 * pow(t, 10) - 275.0 * pow(t, 9) + 55.0 * pow(t, 8) + 308.0 * pow(t, 7) + 460.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0) / (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0);
                V(0, 1) = (1.0 / 60.0) * (114954.0 * pow(t, 11) + 3126.0 * pow(t, 10) - 64785.0 * pow(t, 9) - 80515.0 * pow(t, 8) - 52688.0 * pow(t, 7) - 6184.0 * pow(t, 6) + 29342.0 * pow(t, 5) + 30370.0 * pow(t, 4) + 18110.0 * pow(t, 3) + 6698.0 * pow(t, 2) + 1435.0 * t + 137.0) / (u * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(1, 0) = V(0, 1);
                V(0, 2) = (1.0 / 4.0) * ( - 11102.0 * pow(t, 11) + 10142.0 * pow(t, 10) + 9739.0 * pow(t, 9) + 821.0 * pow(t, 8) - 6402.0 * pow(t, 7) - 6238.0 * pow(t, 6) - 420.0 * pow(t, 5) + 1380.0 * pow(t, 4) + 1320.0 * pow(t, 3) + 600.0 * pow(t, 2) + 145.0 * t + 15.0) / (pow(u, 2) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(2, 0) = V(0, 2);
                V(0, 3) = (1.0 / 4.0) * (10878.0 * pow(t, 11) - 22866.0 * pow(t, 10) + 1923.0 * pow(t, 9) + 14243.0 * pow(t, 8) + 4810.0 * pow(t, 7) - 7750.0 * pow(t, 6) - 2308.0 * pow(t, 5) - 260.0 * pow(t, 4) + 680.0 * pow(t, 3) + 488.0 * pow(t, 2) + 145.0 * t + 17.0) / (pow(u, 3) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(3, 0) = V(0, 3);
                V(0, 4) = ( - 1638.0 * pow(t, 11) + 5814.0 * pow(t, 10) - 5985.0 * pow(t, 9) - 615.0 * pow(t, 8) + 3822.0 * pow(t, 7) - 1038.0 * pow(t, 6) - 252.0 * pow(t, 5) - 180.0 * pow(t, 4) + 48.0 * pow(t, 2) + 21.0 * t + 3.0) / (pow(u, 4) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(4, 0) = V(0, 4);
                V(0, 5) = pow((t - 1.0), 6) * (252.0 * pow(t, 5) + 126.0 * pow(t, 4) * (t + 1.0) + 56.0 * pow(t, 3) * pow((t + 1.0), 2) + 21.0 * pow(t, 2) * pow((t + 1.0), 3) + 6.0 * t * pow((t + 1.0), 4) + pow((t + 1.0), 5)) / (pow(u, 5) * pow((t + 1.0), 11));
                V(5, 0) = V(0, 5);
                V(1, 1) = (1.0 / 1800.0) * ( - 7199689.0 * pow(t, 11) + 4420549.0 * pow(t, 10) + 6468035.0 * pow(t, 9) + 3313065.0 * pow(t, 8) - 1376130.0 * pow(t, 7) - 4224822.0 * pow(t, 6) - 3806418.0 * pow(t, 5) - 455910.0 * pow(t, 4) + 1141035.0 * pow(t, 3) + 1090705.0 * pow(t, 2) + 507311.0 * t + 122269.0) / (pow(u, 2) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(1, 2) = (7.0 / 60.0) * (49903.0 * pow(t, 11) - 76423.0 * pow(t, 10) - 29891.0 * pow(t, 9) + 30961.0 * pow(t, 8) + 47708.0 * pow(t, 7) + 17824.0 * pow(t, 6) - 21752.0 * pow(t, 5) - 22144.0 * pow(t, 4) - 6371.0 * pow(t, 3) + 3807.0 * pow(t, 2) + 4563.0 * t + 1815.0) / (pow(u, 3) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(2, 1) = V(1, 2);
                V(1, 3) =  - 1.0 / 60.0 * (343574.0 * pow(t, 11) - 929243.0 * pow(t, 10) + 402164.0 * pow(t, 9) + 570549.0 * pow(t, 8) - 64596.0 * pow(t, 7) - 436254.0 * pow(t, 6) - 15960.0 * pow(t, 5) + 34986.0 * pow(t, 4) + 92526.0 * pow(t, 3) + 38521.0 * pow(t, 2) - 15820.0 * t - 20447.0) / (pow(u, 4) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(3, 1) = V(1, 3);
                V(1, 4) = (7.0 / 5.0) * (2471.0 * pow(t, 11) - 10235.0 * pow(t, 10) + 13565.0 * pow(t, 9) - 2375.0 * pow(t, 8) - 7780.0 * pow(t, 7) + 4048.0 * pow(t, 6) + 520.0 * pow(t, 5) - 40.0 * pow(t, 4) + 325.0 * pow(t, 3) - 445.0 * pow(t, 2) - 269.0 * t + 215.0) / (pow(u, 5) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(4, 1) = V(1, 4);
                V(1, 5) = (1.0 / 15.0) * ( - 14671.0 * pow(t, 11) + 86146.0 * pow(t, 10) - 203995.0 * pow(t, 9) + 242400.0 * pow(t, 8) - 142050.0 * pow(t, 7) + 30072.0 * pow(t, 6) + 798.0 * pow(t, 5) + 2820.0 * pow(t, 4) - 4575.0 * pow(t, 3) + 7750.0 * pow(t, 2) - 6451.0 * t + 1756.0) / (pow(u, 6) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(5, 1) = V(1, 5);
                V(2, 2) =  - 1.0 / 72.0 * (613067.0 * pow(t, 11) - 1489103.0 * pow(t, 10) + 320495.0 * pow(t, 9) + 990885.0 * pow(t, 8) + 350070.0 * pow(t, 7) - 539070.0 * pow(t, 6) - 738570.0 * pow(t, 5) + 181650.0 * pow(t, 4) + 313215.0 * pow(t, 3) + 99085.0 * pow(t, 2) - 51877.0 * t - 49847.0) / (pow(u, 4) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(2, 3) = (7.0 / 8.0) * (9611.0 * pow(t, 11) - 34481.0 * pow(t, 10) + 31793.0 * pow(t, 9) + 13037.0 * pow(t, 8) - 18914.0 * pow(t, 7) - 16762.0 * pow(t, 6) + 10706.0 * pow(t, 5) + 10762.0 * pow(t, 4) - 1657.0 * pow(t, 3) - 4581.0 * pow(t, 2) - 819.0 * t + 1305.0) / (pow(u, 5) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(3, 2) = V(2, 3);
                V(2, 4) =  - 1.0 / 6.0 * (30589.0 * pow(t, 11) - 153409.0 * pow(t, 10) + 270817.0 * pow(t, 9) - 142797.0 * pow(t, 8) - 114486.0 * pow(t, 7) + 134862.0 * pow(t, 6) - 4326.0 * pow(t, 5) + 78.0 * pow(t, 4) - 37383.0 * pow(t, 3) + 6131.0 * pow(t, 2) + 16069.0 * t - 6145.0) / (pow(u, 6) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(4, 2) = V(2, 4);
                V(2, 5) = (7.0 / 2.0) * pow((t - 1.0), 8) * (720.0 * pow(t, 3) + 720.0 * pow(t, 2) * ( - t + 1.0) + 330.0 * t * pow((t - 1.0), 2) - 60.0 * pow((t - 1.0), 3) + 6.0 * pow((t + 1.0), 3) + 16.0 * pow((t + 1.0), 2) * (2.0 * t + 1.0) + 3.0 * (t + 1.0) * (72.0 * pow(t, 2) + 48.0 * t * ( - t + 1.0) + 11.0 * pow((t - 1.0), 2))) / (pow(u, 7) * pow((t + 1.0), 11));
                V(5, 2) = V(2, 5);
                V(3, 3) =  - 1.0 / 4.0 * (33351.0 * pow(t, 11) - 157929.0 * pow(t, 10) + 246453.0 * pow(t, 9) - 68427.0 * pow(t, 8) - 151722.0 * pow(t, 7) + 32886.0 * pow(t, 6) + 157626.0 * pow(t, 5) - 75078.0 * pow(t, 4) - 44973.0 * pow(t, 3) + 18147.0 * pow(t, 2) + 17313.0 * t - 7647.0) / (pow(u, 6) * (pow(t, 11) + 11.0 * pow(t, 10) + 55.0 * pow(t, 9) + 165.0 * pow(t, 8) + 330.0 * pow(t, 7) + 462.0 * pow(t, 6) + 462.0 * pow(t, 5) + 330.0 * pow(t, 4) + 165.0 * pow(t, 3) + 55.0 * pow(t, 2) + 11.0 * t + 1.0));
                V(3, 4) = 7.0 * pow(( - t + 1.0), 8) * ((1.0 / 2.0) * (t + 1.0) * (360.0 * pow(t, 2) + 270.0 * t * ( - t + 1.0) + 63.0 * pow((t - 1.0), 2) + 10.0 * pow((t + 1.0), 2) + 10.0 * (t + 1.0) * (5.0 * t + 3.0)) + (3.0 * t + 2.0) * (360.0 * pow(t, 2) + 270.0 * t * ( - t + 1.0) + 63.0 * pow((t - 1.0), 2) + 8.0 * pow((t + 1.0), 2) + 9.0 * (t + 1.0) * (5.0 * t + 3.0))) / (pow(u, 7) * pow((t + 1.0), 11));
                V(4, 3) = V(3, 4);
                V(3, 5) =  - pow((t - 1.0), 9) * (2520.0 * pow(t, 2) - 1890.0 * t * (t - 1.0) + 441.0 * pow((t - 1.0), 2) + 56.0 * pow((t + 1.0), 2) + 63.0 * (t + 1.0) * (5.0 * t + 3.0)) / (pow(u, 8) * pow((t + 1.0), 11));
                V(5, 3) = V(3, 5);
                V(4, 4) = 14.0 * pow((t - 1.0), 8) * ((t + 1.0) * (5.0 * ( - t + 1.0) * (t + 1.0) - 9.0 * (t - 1.0) * (3.0 * t + 2.0)) + 9.0 * (3.0 * t + 2.0) * (( - t + 1.0) * (t + 1.0) - 2.0 * (t - 1.0) * (3.0 * t + 2.0))) / (pow(u, 8) * pow((t + 1.0), 11));
                V(4, 5) = pow((t - 1.0), 10) * (882.0 * t + 630.0) / (pow(u, 9) * pow((t + 1.0), 11));
                V(5, 4) = V(4, 5);
                V(5, 5) = 252.0 * pow(( - t + 1.0), 11) / (pow(u, 10) * pow((t + 1.0), 11));
                return V;
            }

        std::shared_ptr<ICore> _makeFmpCore (const int order, const double tau, const double theta) {
            if (order == 0) {
                return std::make_shared<CoreFmp0>(tau, theta);
            } else if (order == 1.0) {
                return std::make_shared<CoreFmp1>(tau, theta);
            } else if (order == 2.0) {
                return std::make_shared<CoreFmp2>(tau, theta);
            } else if (order == 3.0) {
                return std::make_shared<CoreFmp3>(tau, theta);
            } else if (order == 4.0) {
                return std::make_shared<CoreFmp4>(tau, theta);
            } else {
                return std::make_shared<CoreFmp5>(tau, theta);
            }
        }

        std::shared_ptr<RecursivePolynomialFilter> makeFmp (const int order, const double tau, const double theta) {
            std::shared_ptr<ICore> core;
            core = _makeFmpCore(order, tau, theta);
            return std::make_shared<RecursivePolynomialFilter>(order, tau, core);
        }

    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)