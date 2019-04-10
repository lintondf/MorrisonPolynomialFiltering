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
                V(0, 0) = ( - t + 1) / (t + 1);
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
                V(0, 0) = ( - 5 * pow(t, 3) + pow(t, 2) + 3 * t + 1) / (pow(t, 3) + 3 * pow(t, 2) + 3 * t + 1);
                V(0, 1) = pow((t - 1), 2) * (3 * t + 1) / (u * pow((t + 1), 3));
                V(1, 0) = V(0, 1);
                V(1, 1) = 2 * pow(( - t + 1), 3) / (pow(u, 2) * pow((t + 1), 3));
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
                V(0, 0) = ( - 19 * pow(t, 5) - 5 * pow(t, 4) + 8 * pow(t, 3) + 10 * pow(t, 2) + 5 * t + 1) / (pow(t, 5) + 5 * pow(t, 4) + 10 * pow(t, 3) + 10 * pow(t, 2) + 5 * t + 1);
                V(0, 1) = (3.0 / 2.0) * (14 * pow(t, 5) - 13 * pow(t, 4) - 10 * pow(t, 3) + 4 * pow(t, 2) + 4 * t + 1) / (u * (pow(t, 5) + 5 * pow(t, 4) + 10 * pow(t, 3) + 10 * pow(t, 2) + 5 * t + 1));
                V(1, 0) = V(0, 1);
                V(0, 2) =  - pow((t - 1), 3) * (6 * pow(t, 2) + 3 * t * (t + 1) + pow((t + 1), 2)) / (pow(u, 2) * pow((t + 1), 5));
                V(2, 0) = V(0, 2);
                V(1, 1) =  - 1.0 / 2.0 * (49 * pow(t, 5) - 97 * pow(t, 4) + 10 * pow(t, 3) + 62 * pow(t, 2) - 11 * t - 13) / (pow(u, 2) * (pow(t, 5) + 5 * pow(t, 4) + 10 * pow(t, 3) + 10 * pow(t, 2) + 5 * t + 1));
                V(1, 2) = 3 * pow((t - 1), 3) * ( - ( - t + 1) * (3 * t + 1) + (t - 1) * (t + 1)) / (pow(u, 3) * pow((t + 1), 5));
                V(2, 1) = V(1, 2);
                V(2, 2) = 6 * pow(( - t + 1), 5) / (pow(u, 4) * pow((t + 1), 5));
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
                V(0, 0) = ( - 69 * pow(t, 7) - 35 * pow(t, 6) + 7 * pow(t, 5) + 33 * pow(t, 4) + 35 * pow(t, 3) + 21 * pow(t, 2) + 7 * t + 1) / (pow(t, 7) + 7 * pow(t, 6) + 21 * pow(t, 5) + 35 * pow(t, 4) + 35 * pow(t, 3) + 21 * pow(t, 2) + 7 * t + 1);
                V(0, 1) = (1.0 / 6.0) * (625 * pow(t, 7) - 289 * pow(t, 6) - 541 * pow(t, 5) - 211 * pow(t, 4) + 167 * pow(t, 3) + 169 * pow(t, 2) + 69 * t + 11) / (u * (pow(t, 7) + 7 * pow(t, 6) + 21 * pow(t, 5) + 35 * pow(t, 4) + 35 * pow(t, 3) + 21 * pow(t, 2) + 7 * t + 1));
                V(1, 0) = V(0, 1);
                V(0, 2) = ( - 90 * pow(t, 7) + 158 * pow(t, 6) + 10 * pow(t, 5) - 94 * pow(t, 4) - 10 * pow(t, 3) + 14 * pow(t, 2) + 10 * t + 2) / (pow(u, 2) * (pow(t, 7) + 7 * pow(t, 6) + 21 * pow(t, 5) + 35 * pow(t, 4) + 35 * pow(t, 3) + 21 * pow(t, 2) + 7 * t + 1));
                V(2, 0) = V(0, 2);
                V(0, 3) = pow((t - 1), 4) * (20 * pow(t, 3) + 10 * pow(t, 2) * (t + 1) + 4 * t * pow((t + 1), 2) + pow((t + 1), 3)) / (pow(u, 3) * pow((t + 1), 7));
                V(3, 0) = V(0, 3);
                V(1, 1) = (1.0 / 18.0) * ( - 2905 * pow(t, 7) + 3865 * pow(t, 6) + 2025 * pow(t, 5) - 1705 * pow(t, 4) - 2375 * pow(t, 3) + 135 * pow(t, 2) + 695 * t + 265) / (pow(u, 2) * (pow(t, 7) + 7 * pow(t, 6) + 21 * pow(t, 5) + 35 * pow(t, 4) + 35 * pow(t, 3) + 21 * pow(t, 2) + 7 * t + 1));
                V(1, 2) = (5.0 / 3.0) * (85 * pow(t, 7) - 219 * pow(t, 6) + 93 * pow(t, 5) + 133 * pow(t, 4) - 57 * pow(t, 3) - 57 * pow(t, 2) + 7 * t + 15) / (pow(u, 3) * (pow(t, 7) + 7 * pow(t, 6) + 21 * pow(t, 5) + 35 * pow(t, 4) + 35 * pow(t, 3) + 21 * pow(t, 2) + 7 * t + 1));
                V(2, 1) = V(1, 2);
                V(1, 3) = (1.0 / 3.0) * pow((t - 1), 4) * (15 * ( - t + 1) * (t + 1) * (3 * t + 1) + 10 * ( - t + 1) * (18 * pow(t, 2) + 9 * t * ( - t + 1) + 2 * pow(( - t + 1), 2)) - 12 * (t - 1) * pow((t + 1), 2)) / (pow(u, 4) * pow((t + 1), 7));
                V(3, 1) = V(1, 3);
                V(2, 2) = 2 * pow((t - 1), 4) * ((t + 1) * (3 * ( - t + 1) * (t + 1) - 5 * (t - 1) * (2 * t + 1)) + 5 * (2 * t + 1) * (( - t + 1) * (t + 1) - 2 * (t - 1) * (2 * t + 1))) / (pow(u, 4) * pow((t + 1), 7));
                V(2, 3) = pow((t - 1), 6) * (50 * t + 30) / (pow(u, 5) * pow((t + 1), 7));
                V(3, 2) = V(2, 3);
                V(3, 3) = 20 * pow(( - t + 1), 7) / (pow(u, 6) * pow((t + 1), 7));
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
                V(0, 0) = ( - 251 * pow(t, 9) - 159 * pow(t, 8) - 36 * pow(t, 7) + 66 * pow(t, 6) + 124 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1) / (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1);
                V(0, 1) = (5.0 / 12.0) * (1100 * pow(t, 9) - 182 * pow(t, 8) - 816 * pow(t, 7) - 707 * pow(t, 6) - 170 * pow(t, 5) + 285 * pow(t, 4) + 292 * pow(t, 3) + 151 * pow(t, 2) + 42 * t + 5) / (u * (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1));
                V(1, 0) = V(0, 1);
                V(0, 2) = (1.0 / 12.0) * ( - 6510 * pow(t, 9) + 8190 * pow(t, 8) + 4620 * pow(t, 7) - 2955 * pow(t, 6) - 4850 * pow(t, 5) - 425 * pow(t, 4) + 880 * pow(t, 3) + 755 * pow(t, 2) + 260 * t + 35) / (pow(u, 2) * (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1));
                V(2, 0) = V(0, 2);
                V(0, 3) = (5.0 / 2.0) * (154 * pow(t, 9) - 406 * pow(t, 8) + 204 * pow(t, 7) + 209 * pow(t, 6) - 136 * pow(t, 5) - 39 * pow(t, 4) - 4 * pow(t, 3) + 11 * pow(t, 2) + 6 * t + 1) / (pow(u, 3) * (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1));
                V(3, 0) = V(0, 3);
                V(0, 4) =  - pow((t - 1), 5) * (70 * pow(t, 4) + 35 * pow(t, 3) * (t + 1) + 15 * pow(t, 2) * pow((t + 1), 2) + 5 * t * pow((t + 1), 3) + pow((t + 1), 4)) / (pow(u, 4) * pow((t + 1), 9));
                V(4, 0) = V(0, 4);
                V(1, 1) = (1.0 / 72.0) * ( - 60995 * pow(t, 9) + 55045 * pow(t, 8) + 56220 * pow(t, 7) + 4940 * pow(t, 6) - 37730 * pow(t, 5) - 38370 * pow(t, 4) - 1540 * pow(t, 3) + 11980 * pow(t, 2) + 8205 * t + 2245) / (pow(u, 2) * (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1));
                V(1, 2) = (25.0 / 72.0) * (2913 * pow(t, 9) - 5710 * pow(t, 8) - 304 * pow(t, 7) + 3608 * pow(t, 6) + 2114 * pow(t, 5) - 1516 * pow(t, 4) - 1528 * pow(t, 3) - 184 * pow(t, 2) + 389 * t + 218) / (pow(u, 3) * (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1));
                V(2, 1) = V(1, 2);
                V(1, 3) =  - 1.0 / 12.0 * (8668 * pow(t, 9) - 28763 * pow(t, 8) + 24708 * pow(t, 7) + 9452 * pow(t, 6) - 16892 * pow(t, 5) - 858 * pow(t, 4) + 1148 * pow(t, 3) + 3292 * pow(t, 2) + 288 * t - 1043) / (pow(u, 4) * (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1));
                V(3, 1) = V(1, 3);
                V(1, 4) = (5.0 / 6.0) * (285 * pow(t, 9) - 1426 * pow(t, 8) + 2732 * pow(t, 7) - 2356 * pow(t, 6) + 710 * pow(t, 5) + 80 * pow(t, 4) - 4 * pow(t, 3) + 68 * pow(t, 2) - 139 * t + 50) / (pow(u, 5) * (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1));
                V(4, 1) = V(1, 4);
                V(2, 2) =  - 1.0 / 72.0 * (87647 * pow(t, 9) - 262227 * pow(t, 8) + 155652 * pow(t, 7) + 158508 * pow(t, 6) - 70518 * pow(t, 5) - 160482 * pow(t, 4) + 51492 * pow(t, 3) + 54348 * pow(t, 2) - 273 * t - 14147) / (pow(u, 4) * (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1));
                V(2, 3) = (175.0 / 3.0) * (15 * pow(t, 9) - 65 * pow(t, 8) + 91 * pow(t, 7) - 17 * pow(t, 6) - 59 * pow(t, 5) + 25 * pow(t, 4) + 25 * pow(t, 3) - 11 * pow(t, 2) - 8 * t + 4) / (pow(u, 5) * (pow(t, 9) + 9 * pow(t, 8) + 36 * pow(t, 7) + 84 * pow(t, 6) + 126 * pow(t, 5) + 126 * pow(t, 4) + 84 * pow(t, 3) + 36 * pow(t, 2) + 9 * t + 1));
                V(3, 2) = V(2, 3);
                V(2, 4) =  - pow((t - 1), 7) * (420 * pow(t, 2) - 280 * t * (t - 1) + (385.0 / 6.0) * pow((t - 1), 2) + 15 * pow((t + 1), 2) + 35 * (t + 1) * (2 * t + 1)) / (pow(u, 6) * pow((t + 1), 9));
                V(4, 2) = V(2, 4);
                V(3, 3) = (5.0 / 2.0) * pow((t - 1), 6) * ((t + 1) * (8 * ( - t + 1) * (t + 1) - 7 * (t - 1) * (5 * t + 3)) + 7 * (5 * t + 3) * (( - t + 1) * (t + 1) - (t - 1) * (5 * t + 3))) / (pow(u, 6) * pow((t + 1), 9));
                V(3, 4) = 35 * pow((t - 1), 7) * ( - ( - t + 1) * (t + 1) + (t - 1) * (5 * t + 3)) / (pow(u, 7) * pow((t + 1), 9));
                V(4, 3) = V(3, 4);
                V(4, 4) = 70 * pow(( - t + 1), 9) / (pow(u, 8) * pow((t + 1), 9));
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
                V(0, 1) = (1.0 / 60.0) * (114954 * pow(t, 11) + 3126 * pow(t, 10) - 64785 * pow(t, 9) - 80515 * pow(t, 8) - 52688 * pow(t, 7) - 6184 * pow(t, 6) + 29342 * pow(t, 5) + 30370 * pow(t, 4) + 18110 * pow(t, 3) + 6698 * pow(t, 2) + 1435 * t + 137) / (u * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(1, 0) = V(0, 1);
                V(0, 2) = (1.0 / 4.0) * ( - 11102 * pow(t, 11) + 10142 * pow(t, 10) + 9739 * pow(t, 9) + 821 * pow(t, 8) - 6402 * pow(t, 7) - 6238 * pow(t, 6) - 420 * pow(t, 5) + 1380 * pow(t, 4) + 1320 * pow(t, 3) + 600 * pow(t, 2) + 145 * t + 15) / (pow(u, 2) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(2, 0) = V(0, 2);
                V(0, 3) = (1.0 / 4.0) * (10878 * pow(t, 11) - 22866 * pow(t, 10) + 1923 * pow(t, 9) + 14243 * pow(t, 8) + 4810 * pow(t, 7) - 7750 * pow(t, 6) - 2308 * pow(t, 5) - 260 * pow(t, 4) + 680 * pow(t, 3) + 488 * pow(t, 2) + 145 * t + 17) / (pow(u, 3) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(3, 0) = V(0, 3);
                V(0, 4) = ( - 1638 * pow(t, 11) + 5814 * pow(t, 10) - 5985 * pow(t, 9) - 615 * pow(t, 8) + 3822 * pow(t, 7) - 1038 * pow(t, 6) - 252 * pow(t, 5) - 180 * pow(t, 4) + 48 * pow(t, 2) + 21 * t + 3) / (pow(u, 4) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(4, 0) = V(0, 4);
                V(0, 5) = pow((t - 1), 6) * (252 * pow(t, 5) + 126 * pow(t, 4) * (t + 1) + 56 * pow(t, 3) * pow((t + 1), 2) + 21 * pow(t, 2) * pow((t + 1), 3) + 6 * t * pow((t + 1), 4) + pow((t + 1), 5)) / (pow(u, 5) * pow((t + 1), 11));
                V(5, 0) = V(0, 5);
                V(1, 1) = (1.0 / 1800.0) * ( - 7199689 * pow(t, 11) + 4420549 * pow(t, 10) + 6468035 * pow(t, 9) + 3313065 * pow(t, 8) - 1376130 * pow(t, 7) - 4224822 * pow(t, 6) - 3806418 * pow(t, 5) - 455910 * pow(t, 4) + 1141035 * pow(t, 3) + 1090705 * pow(t, 2) + 507311 * t + 122269) / (pow(u, 2) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(1, 2) = (7.0 / 60.0) * (49903 * pow(t, 11) - 76423 * pow(t, 10) - 29891 * pow(t, 9) + 30961 * pow(t, 8) + 47708 * pow(t, 7) + 17824 * pow(t, 6) - 21752 * pow(t, 5) - 22144 * pow(t, 4) - 6371 * pow(t, 3) + 3807 * pow(t, 2) + 4563 * t + 1815) / (pow(u, 3) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(2, 1) = V(1, 2);
                V(1, 3) =  - 1.0 / 60.0 * (343574 * pow(t, 11) - 929243 * pow(t, 10) + 402164 * pow(t, 9) + 570549 * pow(t, 8) - 64596 * pow(t, 7) - 436254 * pow(t, 6) - 15960 * pow(t, 5) + 34986 * pow(t, 4) + 92526 * pow(t, 3) + 38521 * pow(t, 2) - 15820 * t - 20447) / (pow(u, 4) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(3, 1) = V(1, 3);
                V(1, 4) = (7.0 / 5.0) * (2471 * pow(t, 11) - 10235 * pow(t, 10) + 13565 * pow(t, 9) - 2375 * pow(t, 8) - 7780 * pow(t, 7) + 4048 * pow(t, 6) + 520 * pow(t, 5) - 40 * pow(t, 4) + 325 * pow(t, 3) - 445 * pow(t, 2) - 269 * t + 215) / (pow(u, 5) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(4, 1) = V(1, 4);
                V(1, 5) = (1.0 / 15.0) * ( - 14671 * pow(t, 11) + 86146 * pow(t, 10) - 203995 * pow(t, 9) + 242400 * pow(t, 8) - 142050 * pow(t, 7) + 30072 * pow(t, 6) + 798 * pow(t, 5) + 2820 * pow(t, 4) - 4575 * pow(t, 3) + 7750 * pow(t, 2) - 6451 * t + 1756) / (pow(u, 6) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(5, 1) = V(1, 5);
                V(2, 2) =  - 1.0 / 72.0 * (613067 * pow(t, 11) - 1489103 * pow(t, 10) + 320495 * pow(t, 9) + 990885 * pow(t, 8) + 350070 * pow(t, 7) - 539070 * pow(t, 6) - 738570 * pow(t, 5) + 181650 * pow(t, 4) + 313215 * pow(t, 3) + 99085 * pow(t, 2) - 51877 * t - 49847) / (pow(u, 4) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(2, 3) = (7.0 / 8.0) * (9611 * pow(t, 11) - 34481 * pow(t, 10) + 31793 * pow(t, 9) + 13037 * pow(t, 8) - 18914 * pow(t, 7) - 16762 * pow(t, 6) + 10706 * pow(t, 5) + 10762 * pow(t, 4) - 1657 * pow(t, 3) - 4581 * pow(t, 2) - 819 * t + 1305) / (pow(u, 5) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(3, 2) = V(2, 3);
                V(2, 4) =  - 1.0 / 6.0 * (30589 * pow(t, 11) - 153409 * pow(t, 10) + 270817 * pow(t, 9) - 142797 * pow(t, 8) - 114486 * pow(t, 7) + 134862 * pow(t, 6) - 4326 * pow(t, 5) + 78 * pow(t, 4) - 37383 * pow(t, 3) + 6131 * pow(t, 2) + 16069 * t - 6145) / (pow(u, 6) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(4, 2) = V(2, 4);
                V(2, 5) = (7.0 / 2.0) * pow((t - 1), 8) * (720 * pow(t, 3) + 720 * pow(t, 2) * ( - t + 1) + 330 * t * pow((t - 1), 2) - 60 * pow((t - 1), 3) + 6 * pow((t + 1), 3) + 16 * pow((t + 1), 2) * (2 * t + 1) + 3 * (t + 1) * (72 * pow(t, 2) + 48 * t * ( - t + 1) + 11 * pow((t - 1), 2))) / (pow(u, 7) * pow((t + 1), 11));
                V(5, 2) = V(2, 5);
                V(3, 3) =  - 1.0 / 4.0 * (33351 * pow(t, 11) - 157929 * pow(t, 10) + 246453 * pow(t, 9) - 68427 * pow(t, 8) - 151722 * pow(t, 7) + 32886 * pow(t, 6) + 157626 * pow(t, 5) - 75078 * pow(t, 4) - 44973 * pow(t, 3) + 18147 * pow(t, 2) + 17313 * t - 7647) / (pow(u, 6) * (pow(t, 11) + 11 * pow(t, 10) + 55 * pow(t, 9) + 165 * pow(t, 8) + 330 * pow(t, 7) + 462 * pow(t, 6) + 462 * pow(t, 5) + 330 * pow(t, 4) + 165 * pow(t, 3) + 55 * pow(t, 2) + 11 * t + 1));
                V(3, 4) = 7 * pow(( - t + 1), 8) * ((1.0 / 2.0) * (t + 1) * (360 * pow(t, 2) + 270 * t * ( - t + 1) + 63 * pow((t - 1), 2) + 10 * pow((t + 1), 2) + 10 * (t + 1) * (5 * t + 3)) + (3 * t + 2) * (360 * pow(t, 2) + 270 * t * ( - t + 1) + 63 * pow((t - 1), 2) + 8 * pow((t + 1), 2) + 9 * (t + 1) * (5 * t + 3))) / (pow(u, 7) * pow((t + 1), 11));
                V(4, 3) = V(3, 4);
                V(3, 5) =  - pow((t - 1), 9) * (2520 * pow(t, 2) - 1890 * t * (t - 1) + 441 * pow((t - 1), 2) + 56 * pow((t + 1), 2) + 63 * (t + 1) * (5 * t + 3)) / (pow(u, 8) * pow((t + 1), 11));
                V(5, 3) = V(3, 5);
                V(4, 4) = 14 * pow((t - 1), 8) * ((t + 1) * (5 * ( - t + 1) * (t + 1) - 9 * (t - 1) * (3 * t + 2)) + 9 * (3 * t + 2) * (( - t + 1) * (t + 1) - 2 * (t - 1) * (3 * t + 2))) / (pow(u, 8) * pow((t + 1), 11));
                V(4, 5) = pow((t - 1), 10) * (882 * t + 630) / (pow(u, 9) * pow((t + 1), 11));
                V(5, 4) = V(4, 5);
                V(5, 5) = 252 * pow(( - t + 1), 11) / (pow(u, 10) * pow((t + 1), 11));
                return V;
            }

        std::shared_ptr<FMPBase> makeFMP (const int order, const double theta, const double tau) {
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