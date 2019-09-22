/***** /polynomialfiltering/components/RecursivePolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_RECURSIVEPOLYNOMIALFILTER_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_RECURSIVEPOLYNOMIALFILTER_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>


#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/ICore.hpp>


namespace polynomialfiltering {
    namespace components {

        ///// @class /polynomialfiltering/components/::RecursivePolynomialFilter : <CLASS>; supers(AbstractFilter,)
        /// @brief Base class for both expanding and fading polynomial filter and their combinations.
        /// 
        class RecursivePolynomialFilter : public AbstractFilter {
            public:

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		order	integer polynomial orer
                ///  @param		tau	nominal time step
                /// 
                RecursivePolynomialFilter(const int order, const double tau, const std::shared_ptr<ICore> core);

                ///// @brief Estimate of the FMP fading factor theta to match 0th variance of an EMP
                /// 
                /// 
                ///  @param		order	integer polynomial order
                ///  @param		n	float sample number
                /// 
                double effectiveTheta(const int order, const double n);

                ///// @brief Copy the state of another filter into this filter.
                /// 
                void copyState(const std::shared_ptr<RecursivePolynomialFilter> that);

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
                std::shared_ptr<ICore> getCore();

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
                double getFirstVRF();
                double getLastVRF();

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
                int n; ///<  number of samples
                double dtau; ///<  delta nominal scaled time step
                double t0; ///<  filter start time
                double tau; ///<  nominal scaled time step
                double t; ///<   time of the last input
                RealVector Z; ///<  NORMALIZED state vector at time of last input
                RealVector D; ///<  noralization/denormalization scaling vector; D(tau) = [tau^-0, tau^-1,...tau^-order]
                std::shared_ptr<ICore> core; ///<  provider of core expanding / fading functions
                
                ///// @brief Matches an input state vector to the filter order
                /// 
                /// Longer state vectors are truncated and short ones are zero filled
                /// 
                /// 
                ///  @param		state	arbitrary length input state vector
                /// 
                ///  @return  conformed state vector with order+1 elements
                /// 
                /// 
                RealVector _conformState(const RealVector& state);
                
                ///// @brief Convert an external time to internal (tau) units
                /// 
                /// 
                ///  @param		t	external time (e.g. seconds)
                /// 
                ///  @return  time in internal units (tau steps since t0)
                /// 
                /// 
                double _normalizeTime(const double t);
                
                ///// @brief Converts external delta time to internal (tau) step units
                /// 
                /// 
                ///  @param		dt	external time step (e.g. seconds)
                /// 
                ///  @return  time step in internal units
                /// 
                /// 
                double _normalizeDeltaTime(const double dt);
                
                ///// @brief Normalize a state vector
                /// 
                /// Multiplies the input state vector by the normalization vector D
                /// 
                /// 
                ///  @param		Z	state vector in external units
                /// 
                ///  @return  state vector in internal units
                /// 
                /// 
                RealVector _normalizeState(const RealVector& Z);
                
                ///// @brief Denormalize a state vector
                /// 
                /// Divides the input state vector by the normalization vector D
                /// 
                /// 
                ///  @param		Z	state vector in internal units
                /// 
                ///  @return  state vector in external units
                /// 
                /// 
                RealVector _denormalizeState(const RealVector& Z);
        }; // class RecursivePolynomialFilter 

    }; // namespace components
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_RECURSIVEPOLYNOMIALFILTER_HPP