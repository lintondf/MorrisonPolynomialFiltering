/***** /PolynomialFiltering/Components/EmpFmpPair/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_EMPFMPPAIR_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_EMPFMPPAIR_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>
#include <polynomialfiltering/components/ExpandingMemoryPolynomialFilter.hpp>
#include <polynomialfiltering/components/FadingMemoryPolynomialFilter.hpp>


namespace PolynomialFiltering {
    namespace Components {

        ///// @class EmpFmpPair
        /// @brief Filter composed of an expanding memory and a fading memory filter of the same order.
        /// 
        /// The EMP filter is used to initialize and after the sample number when the 0th order
        /// variance of the EMP filter matches that variance of the FMP at the configured theta
        /// fading factor, we switch to the FMP filter. See Morrison 1969, Section 13.8
        /// 
        class EmpFmpPair : public AbstractRecursiveFilter {
            public:

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		order	integer polynomial orer
                ///  @param		theta	fading factor
                ///  @param		tau	nominal time step
                /// 
                EmpFmpPair(const int order, const double theta, const double tau);

                ///// @brief Start or restart the filter
                /// 
                /// 
                ///  @param		t	external start time
                ///  @param		Z	state vector in external units
                /// 
                ///  @return   @return		None
                /// 
                /// 
                void start(const double t, const RealVector& Z);

                ///// @brief Predict the filter state (Z*) at time t
                /// 
                /// 
                ///  @param		t	target time
                /// 
                ///  @return  predicted state INTERNAL UNITS
                /// 
                /// 
                RealVector predict(const double t);

                ///// @brief Update the filter state from using the prediction error e
                /// 
                /// 
                ///  @param		t	update time
                ///  @param		Zstar	predicted NORMALIZED state at update time
                ///  @param		e	prediction error (observation - predicted state)
                /// 
                ///  @return  innovation vector
                /// 
                ///  @par Examples
                /// Zstar = self.predict(t)
                /// e = observation[0] - Zstar[0]
                /// self.update(t, Zstar, e )
                /// 
                RealVector update(const double t, const RealVector& Zstar, const double e);

                ///// @brief Return the number of processed observations since start
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Count of processed observations
                /// 
                /// 
                int getN();

                ///// @brief Return the nominal time step for the filter
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Nominal time step (tau) in external units
                /// 
                /// 
                double getTau();

                ///// @brief Return the time of the last processed observation or filter start
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Time in external units
                /// 
                /// 
                double getTime();

                ///// @brief Get the current filter state vector
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  State vector in external units
                /// 
                /// 
                RealVector getState();

                ///// @brief Get the variance reduction factor matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix getVRF();
            protected:
                std::shared_ptr<ExpandingMemoryPolynomialFilter::EMPBase> emp;
                std::shared_ptr<FadingMemoryPolynomialFilter::FMPBase> fmp;
                std::shared_ptr<AbstractRecursiveFilter> current;
                double _gammaParameter(const double t, const double dtau);
                RealVector _gamma(const double n);
                RealMatrix _VRF();
        }; // class EmpFmpPair 

    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_EMPFMPPAIR_HPP