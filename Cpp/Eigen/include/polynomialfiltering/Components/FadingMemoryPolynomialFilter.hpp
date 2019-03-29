/***** /PolynomialFiltering/Components/FadingMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_FADINGMEMORYPOLYNOMIALFILTER_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_FADINGMEMORYPOLYNOMIALFILTER_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>


namespace PolynomialFiltering {
    namespace Components {
        class FMPBase : public AbstractRecursiveFilter {
            public:
                FMPBase(const long order, const double theta, const double tau);
                double getTheta();
            protected:
                long n0;
                double theta;
                double _gammaParameter(const double t, const double dtau);
                virtual RealMatrix _VRF() = 0;
        }; // class FMPBase 

        class FMP0 : public FMPBase {
            public:
                FMP0(const double theta, const double tau);
            protected:
                RealVector _gamma(const double t);
                RealMatrix _VRF();
        }; // class FMP0 

        class FMP1 : public FMPBase {
            public:
                FMP1(const double theta, const double tau);
            protected:
                RealVector _gamma(const double t);
                RealMatrix _VRF();
        }; // class FMP1 

        class FMP2 : public FMPBase {
            public:
                FMP2(const double theta, const double tau);
            protected:
                RealVector _gamma(const double t);
                RealMatrix _VRF();
        }; // class FMP2 

        class FMP3 : public FMPBase {
            public:
                FMP3(const double theta, const double tau);
            protected:
                RealVector _gamma(const double t);
                RealMatrix _VRF();
        }; // class FMP3 

        class FMP4 : public FMPBase {
            public:
                FMP4(const double theta, const double tau);
            protected:
                RealVector _gamma(const double t);
                RealMatrix _VRF();
        }; // class FMP4 

        class FMP5 : public FMPBase {
            public:
                FMP5(const double theta, const double tau);
            protected:
                RealVector _gamma(const double t);
                RealMatrix _VRF();
        }; // class FMP5 

        shared_ptr<FMPBase> makeFMP(const long order, const double theta, const double tau);
        double thetaFromVrf(const long order, const double tau, const double vrf);
    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_FADINGMEMORYPOLYNOMIALFILTER_HPP