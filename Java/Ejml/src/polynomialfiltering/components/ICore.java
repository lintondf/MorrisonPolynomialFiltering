/***** /polynomialfiltering/components/ICore/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.components;
 
import java.util.stream.IntStream;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import polynomialfiltering.main.AbstractFilter;
import polynomialfiltering.main.AbstractFilterWithCovariance;
import static polynomialfiltering.main.Utility.*;

 
public abstract class ICore {
    
    public ICore () {
    }
    

    ///// @brief Get the number of input samples needed to start this core
    /// 
    ///  @return  sample count
    /// 
    
    abstract public int getSamplesToStart ();

    ///// @brief Get the innovation scale vector
    /// 
    /// 
    ///  @param		t	external time
    ///  @param		dtau	internal step
    /// 
    ///  @return  vector (order+1) of (observation-predict) multipliers
    /// 
    
    abstract public DMatrixRMaj getGamma (final double t, final double dtau);

    ///// @brief Get the variance reduction matrix
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  Square matrix (order+1) of input to output variance ratios
    /// 
    /// 
    
    abstract public DMatrixRMaj getVRF (final int n);

    ///// @brief Get the variance reduction factor for the 0th derivative
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  0th derivative input to output variance ratio
    /// 
    
    abstract public double getFirstVRF (final int n);

    ///// @brief Get the variance reduction factor for the 'order'th derivative
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  'order'th derivative input to output variance ratio
    /// 
    
    abstract public double getLastVRF (final int n);
} // class components

