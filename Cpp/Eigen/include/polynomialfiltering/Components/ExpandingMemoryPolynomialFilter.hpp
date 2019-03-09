/***** /PolynomialFiltering/Components/ExpandingMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_EXPANDINGMEMORYPOLYNOMIALFILTER_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_EXPANDINGMEMORYPOLYNOMIALFILTER_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>


namespace PolynomialFiltering {
    namespace Components {
        class EMPBase : public AbstractRecursiveFilter {
            public:
                EMPBase(const long order, const double tau);
                virtual double nSwitch(const double theta) = 0;
            protected:
                double _gammaParameter(const double t, const double dtau);
                static RealMatrix _scaleVRF(const RealMatrix V, const double t, const double n);
                virtual RealMatrix _VRF() = 0;
        }; // class EMPBase 

        class EMP0 : public EMPBase {
            public:
                EMP0(const double tau);
                double nSwitch(const double theta);
            protected:
                RealVector _gamma(const double n);
                RealMatrix _VRF();
        }; // class EMP0 

        class EMP1 : public EMPBase {
            public:
                EMP1(const double tau);
                double nSwitch(const double theta);
            protected:
                RealVector _gamma(const double n);
                RealMatrix _VRF();
        }; // class EMP1 

        class EMP2 : public EMPBase {
            public:
                EMP2(const double tau);
                double nSwitch(const double theta);
            protected:
                RealVector _gamma(const double n);
                RealMatrix _VRF();
        }; // class EMP2 

        class EMP3 : public EMPBase {
            public:
                EMP3(const double tau);
                double nSwitch(const double theta);
            protected:
                RealVector _gamma(const double n);
                RealMatrix _VRF();
        }; // class EMP3 

        class EMP4 : public EMPBase {
            public:
                EMP4(const double tau);
                double nSwitch(const double theta);
            protected:
                RealVector _gamma(const double n);
                RealMatrix _VRF();
        }; // class EMP4 

        class EMP5 : public EMPBase {
            public:
                EMP5(const double tau);
                double nSwitch(const double theta);
            protected:
                RealVector _gamma(const double n);
                RealMatrix _VRF();
        }; // class EMP5 

        std::shared_ptr<EMPBase> makeEMP(const long order, const double tau);
    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_EXPANDINGMEMORYPOLYNOMIALFILTER_HPP