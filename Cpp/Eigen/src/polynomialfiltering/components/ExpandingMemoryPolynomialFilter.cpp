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
                return Map<RowVectorXd>( new double[1] {1 / (1 + n)}, 1);
            }

            double EMP0::nSwitch (const double theta) {
                return 2.0 / (1.0 - theta);
            }

            RealMatrix EMP0::VRF () {
                long n;
                RealMatrix V;
                n = this->n;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                if (n < this->order) {
                    return V;
                }
                V(0, 0) = 1 / (1 + n);
                return V;
            }

            EMP1::EMP1 (const double tau) : EMPBase(1,tau) {
            }

            RealVector EMP1::_gamma (const double n) {
                double denom;
                denom = 1.0 / ((n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[2] {2 * (2 * n + 1), 6}, 2);
            }

            double EMP1::nSwitch (const double theta) {
                return 3.2 / (1.0 - theta);
            }

            RealMatrix EMP1::VRF () {
                long n;
                double u;
                RealMatrix V;
                n = this->n;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                if (n < this->order) {
                    return V;
                }
                u = this->tau;
                V(0, 0) = (2 + 4 * n) / (2 + 3 * n + ((n) * (n)));
                V(0, 1) = 6 / ((2 + 3 * n + ((n) * (n))) * u);
                V(1, 0) = V(0, 1);
                V(1, 1) = 12 / (n * (2 + 3 * n + ((n) * (n))) * ((u) * (u)));
                return V;
            }

            EMP2::EMP2 (const double tau) : EMPBase(2,tau) {
            }

            RealVector EMP2::_gamma (const double n) {
                double n2;
                double denom;
                n2 = n * n;
                denom = 1.0 / ((n + 3) * (n + 2) * (n + 1));
                return denom * Map<RowVectorXd>( new double[3] {3 * (3 * n2 + 3 * n + 2), 18 * (2 * n + 1), (2 * 1) * 30}, 3);
            }

            double EMP2::nSwitch (const double theta) {
                return 4.3636 / (1.0 - theta);
            }

            RealMatrix EMP2::VRF () {
                long n;
                double u;
                RealMatrix V;
                n = this->n;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                if (n < this->order) {
                    return V;
                }
                u = this->tau;
                V(0, 0) = (6 + 9 * n * (1 + n)) / ((1 + n) * (2 + n) * (3 + n));
                V(0, 1) = (18 + 36 * n) / ((6 + 11 * n + 6 * ((n) * (n)) + ((n) * (n) * (n))) * u);
                V(1, 0) = V(0, 1);
                V(0, 2) = 60 / ((6 + 11 * n + 6 * ((n) * (n)) + ((n) * (n) * (n))) * ((u) * (u)));
                V(2, 0) = V(0, 2);
                V(1, 1) = (12 * ( - 3 + 2 * n + 16 * ((n) * (n)))) / (n * ( - 6 - 5 * n + 5 * ((n) * (n)) + 5 * ((n) * (n) * (n)) + ((n) * (n) * (n) * (n))) * ((u) * (u)));
                V(1, 2) = 360 / (( - 6 - 5 * n + 5 * ((n) * (n)) + 5 * ((n) * (n) * (n)) + ((n) * (n) * (n) * (n))) * ((u) * (u) * (u)));
                V(2, 1) = V(1, 2);
                V(2, 2) = 720 / (n * ( - 6 - 5 * n + 5 * ((n) * (n)) + 5 * ((n) * (n) * (n)) + ((n) * (n) * (n) * (n))) * ((u) * (u) * (u) * (u)));
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
                return denom * Map<RowVectorXd>( new double[4] {8 * (2 * n3 + 3 * n2 + 7 * n + 3), 20 * (6 * n2 + 6 * n + 5), (2 * 1) * 120 * (2 * n + 1), (3 * 2 * 1) * 140}, 4);
            }

            double EMP3::nSwitch (const double theta) {
                return 5.50546 / (1.0 - theta);
            }

            RealMatrix EMP3::VRF () {
                long n;
                double u;
                RealMatrix V;
                n = this->n;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                if (n < this->order) {
                    return V;
                }
                u = this->tau;
                V(0, 0) = (8 * (1 + 2 * n) * (3 + n + ((n) * (n)))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n));
                V(0, 1) = (20 * (5 + 6 * n * (1 + n))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * u);
                V(1, 0) = V(0, 1);
                V(0, 2) = (240 * (1 + 2 * n)) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * ((u) * (u)));
                V(2, 0) = V(0, 2);
                V(0, 3) = 840 / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * ((u) * (u) * (u)));
                V(3, 0) = V(0, 3);
                V(1, 1) = (200 * (2 + 3 * n * ( - 1 + ( - 1 + n) * n * (1 + 2 * n)))) / (( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * ((u) * (u)));
                V(1, 2) = (600 * ( - 2 + 3 * n) * (1 + 3 * n)) / (( - 2 + n) * ( - 1 + n) * (1 + n) * (2 + n) * (3 + n) * (4 + n) * ((u) * (u) * (u)));
                V(2, 1) = V(1, 2);
                V(1, 3) = (1680 * (2 - 3 * n + 6 * ((n) * (n)))) / (n * (48 + 28 * n - 56 * ((n) * (n)) - 35 * ((n) * (n) * (n)) + 7 * ((n) * (n) * (n) * (n)) + 7 * ((n) * (n) * (n) * (n) * (n)) + ((n) * (n) * (n) * (n) * (n) * (n))) * ((u) * (u) * (u) * (u)));
                V(3, 1) = V(1, 3);
                V(2, 2) = (1440 * ( - 4 + n + 18 * ((n) * (n)))) / (n * (48 + 28 * n - 56 * ((n) * (n)) - 35 * ((n) * (n) * (n)) + 7 * ((n) * (n) * (n) * (n)) + 7 * ((n) * (n) * (n) * (n) * (n)) + ((n) * (n) * (n) * (n) * (n) * (n))) * ((u) * (u) * (u) * (u)));
                V(2, 3) = 50400 / ((48 + 28 * n - 56 * ((n) * (n)) - 35 * ((n) * (n) * (n)) + 7 * ((n) * (n) * (n) * (n)) + 7 * ((n) * (n) * (n) * (n) * (n)) + ((n) * (n) * (n) * (n) * (n) * (n))) * ((u) * (u) * (u) * (u) * (u)));
                V(3, 2) = V(2, 3);
                V(3, 3) = 100800 / (n * (48 + 28 * n - 56 * ((n) * (n)) - 35 * ((n) * (n) * (n)) + 7 * ((n) * (n) * (n) * (n)) + 7 * ((n) * (n) * (n) * (n) * (n)) + ((n) * (n) * (n) * (n) * (n) * (n))) * ((u) * (u) * (u) * (u) * (u) * (u)));
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
                return denom * Map<RowVectorXd>( new double[5] {5 * (5 * n4 + 10 * n3 + 55 * n2 + 50 * n + 24), 25 * (12 * n3 + 18 * n2 + 46 * n + 20), (2 * 1) * 1050 * (n2 + n + 1), (3 * 2 * 1) * 700 * (2 * n + 1), (4 * 3 * 2 * 1) * 630}, 5);
            }

            double EMP4::nSwitch (const double theta) {
                return 6.6321 / (1.0 - theta);
            }

            RealMatrix EMP4::VRF () {
                long n;
                double u;
                RealMatrix V;
                n = this->n;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                if (n < this->order) {
                    return V;
                }
                u = this->tau;
                V(0, 0) = (5 * (24 + 5 * n * (1 + n) * (10 + n + ((n) * (n))))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n));
                V(0, 1) = (50 * (1 + 2 * n) * (10 + 3 * n * (1 + n))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * u);
                V(1, 0) = V(0, 1);
                V(0, 2) = (2100 * (1 + n + ((n) * (n)))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u)));
                V(2, 0) = V(0, 2);
                V(0, 3) = (4200 * (1 + 2 * n)) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u)));
                V(3, 0) = V(0, 3);
                V(0, 4) = 15120 / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u) * (u)));
                V(4, 0) = V(0, 4);
                V(1, 1) = (100 * (1 + 2 * n) * ( - 60 + n * (218 + 3 * n * ( - 43 + n * (20 + n * ( - 19 + 8 * n)))))) / (( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u)));
                V(1, 2) = (4200 * (15 + n * ( - 7 + n * (7 + 3 * n * ( - 4 + 3 * n))))) / (( - 3 + n) * ( - 2 + n) * ( - 1 + n) * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u)));
                V(2, 1) = V(1, 2);
                V(1, 3) = (1680 * (1 + 2 * n) * ( - 30 + n * (109 - 87 * n + 48 * ((n) * (n))))) / (( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u) * (u)));
                V(3, 1) = V(1, 3);
                V(1, 4) = (151200 * (5 + n * ( - 3 + 2 * n))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ( - 6 + 11 * n - 6 * ((n) * (n)) + ((n) * (n) * (n))) * ((u) * (u) * (u) * (u) * (u)));
                V(4, 1) = V(1, 4);
                V(2, 2) = (35280 * (5 + ( - 1 + n) * n * (4 + n * (5 + 9 * n)))) / (( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u) * (u)));
                V(2, 3) = (352800 * n * ( - 1 + 4 * n)) / (( - 3 + n) * ( - 2 + n) * ( - 1 + n) * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u) * (u) * (u)));
                V(3, 2) = V(2, 3);
                V(2, 4) = (302400 * (5 - 3 * n + 9 * ((n) * (n)))) / (( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u) * (u) * (u) * (u)));
                V(4, 2) = V(2, 4);
                V(3, 3) = (100800 * ( - 15 + 2 * n + 64 * ((n) * (n)))) / (( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u) * (u) * (u) * (u)));
                V(3, 4) = 12700800 / (( - 3 + n) * ( - 2 + n) * ( - 1 + n) * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u) * (u) * (u) * (u) * (u)));
                V(4, 3) = V(3, 4);
                V(4, 4) = 25401600 / (( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * ((u) * (u) * (u) * (u) * (u) * (u) * (u) * (u)));
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
                return denom * Map<RowVectorXd>( new double[6] {6 * (2 * n + 1) * (3 * n4 + 6 * n3 + 77 * n2 + 74 * n + 120), 126 * (5 * n4 + 10 * n3 + 55 * n2 + 50 * n + 28), (2 * 1) * 420 * (2 * n + 1) * (4 * n2 + 4 * n + 15), (3 * 2 * 1) * 1260 * (6 * n2 + 6 * n + 7), (4 * 3 * 2 * 1) * 3780 * (2 * n + 1), (5 * 4 * 3 * 2 * 1) * 2772}, 6);
            }

            double EMP5::nSwitch (const double theta) {
                return 7.7478 / (1.0 - theta);
            }

            RealMatrix EMP5::VRF () {
                long n;
                double u;
                RealMatrix V;
                n = this->n;
                V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                if (n < this->order) {
                    return V;
                }
                u = this->tau;
                V(0, 0) = (6 * (1 + 2 * n) * (120 + n * (1 + n) * (74 + 3 * n * (1 + n)))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n));
                V(0, 1) = (126 * (28 + 5 * n * (1 + n) * (10 + n + ((n) * (n))))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * u);
                V(1, 0) = V(0, 1);
                V(0, 2) = (840 * (1 + 2 * n) * (15 + 4 * n * (1 + n))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u)));
                V(2, 0) = V(0, 2);
                V(0, 3) = (7560 * (7 + 6 * n * (1 + n))) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u)));
                V(3, 0) = V(0, 3);
                V(0, 4) = (90720 * (1 + 2 * n)) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u)));
                V(4, 0) = V(0, 4);
                V(0, 5) = 332640 / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u)));
                V(5, 0) = V(0, 5);
                V(1, 1) = (588 * (288 + 5 * n * ( - 120 + n * ( - 108 + n * ( - 56 + n * (317 + 5 * n * ( - 28 + n * (10 + ( - 4 + n) * n)))))))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u)));
                V(1, 2) = (17640 * ( - 48 + n * ( - 44 + n * (219 + 5 * n * ( - 20 + n * (13 + 2 * ( - 3 + n) * n)))))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u)));
                V(2, 1) = V(1, 2);
                V(1, 3) = (105840 * (24 + n * ( - 50 + n * (50 + 3 * n * ( - 10 + n * (25 + n * ( - 11 + 4 * n))))))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u)));
                V(3, 1) = V(1, 3);
                V(1, 4) = (211680 * ( - 48 + 5 * n * ( - 4 + n * (37 + n * ( - 14 + 5 * n))))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u)));
                V(4, 1) = V(1, 4);
                V(1, 5) = (665280 * (24 + 5 * n * ( - 10 + n * (28 + 3 * ( - 3 + n) * n)))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u) * (u)));
                V(5, 1) = V(1, 5);
                V(2, 2) = (70560 * (1 + 2 * n) * ( - 60 + n * (173 + 8 * n * ( - 11 + n * (7 + 2 * ( - 2 + n) * n))))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u)));
                V(2, 3) = (1058400 * (33 + 2 * n * ( - 7 + n * (13 + 8 * ( - 1 + n) * n)))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u)));
                V(3, 2) = V(2, 3);
                V(2, 4) = (604800 * (1 + 2 * n) * ( - 60 + n * (161 + 12 * n * ( - 7 + 5 * n)))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u) * (u)));
                V(4, 2) = V(2, 4);
                V(2, 5) = (139708800 * (3 + ( - 1 + n) * n)) / ((1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * (24 - 50 * n + 35 * ((n) * (n)) - 10 * ((n) * (n) * (n)) + ((n) * (n) * (n) * (n))) * ((u) * (u) * (u) * (u) * (u) * (u) * (u)));
                V(5, 2) = V(2, 5);
                V(3, 3) = (2721600 * (39 + 2 * n * ( - 10 + n * (7 + 3 * n * ( - 3 + 8 * n))))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u) * (u)));
                V(3, 4) = (114307200 * (1 + n * ( - 1 + 5 * n))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u) * (u) * (u)));
                V(4, 3) = V(3, 4);
                V(3, 5) = (279417600 * (3 + n * ( - 1 + 4 * n))) / (n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * (24 - 50 * n + 35 * ((n) * (n)) - 10 * ((n) * (n) * (n)) + ((n) * (n) * (n) * (n))) * ((u) * (u) * (u) * (u) * (u) * (u) * (u) * (u)));
                V(5, 3) = V(3, 5);
                V(4, 4) = (50803200 * ( - 12 + n + 50 * ((n) * (n)))) / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u) * (u) * (u) * (u)));
                V(4, 5) = 5029516800 / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u) * (u) * (u) * (u) * (u)));
                V(5, 4) = V(4, 5);
                V(5, 5) = 10059033600 / (( - 4 + n) * ( - 3 + n) * ( - 2 + n) * ( - 1 + n) * n * (1 + n) * (2 + n) * (3 + n) * (4 + n) * (5 + n) * (6 + n) * ((u) * (u) * (u) * (u) * (u) * (u) * (u) * (u) * (u) * (u)));
                return V;
            }

        std::shared_ptr<EMPBase> makeEMP (const long order, const double tau) {
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

