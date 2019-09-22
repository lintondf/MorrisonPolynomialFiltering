/***** /polynomialfiltering/components/Fmp/AbstractCoreFmp/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.components.fmp;
 
import java.util.stream.IntStream;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import polynomialfiltering.main.AbstractFilter;
import polynomialfiltering.main.AbstractFilterWithCovariance;
import static polynomialfiltering.main.Utility.*;
import polynomialfiltering.components.ICore;

 
public abstract class AbstractCoreFmp extends ICore {
    protected  double theta;
    protected  DMatrixRMaj VRF = new DMatrixRMaj();
    
    public AbstractCoreFmp() {}  // auto-generated null constructor

    
    public AbstractCoreFmp (final double tau, final double theta) {
                
        this.theta = theta;
    }
    
    
    public int getSamplesToStart () {
        return 1;
    }
    

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
    
    public DMatrixRMaj getVRF (final int n) {
        
        return  new DMatrixRMaj(this.VRF);
    }
    

    ///// @brief Get the variance reduction factor for the 0th derivative
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  0th derivative input to output variance ratio
    /// 
    
    public double getFirstVRF (final int n) {
        
        return  this.VRF.get(0, 0);
    }
    

    ///// @brief Get the variance reduction factor for the 'order'th derivative
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  'order'th derivative input to output variance ratio
    /// 
    
    public double getLastVRF (final int n) {
        
        //  this.VRF(numRows(this.VRF)-1, numCols(this.VRF)-1)
        int        ti1 = this.VRF.getNumRows();
        int        ti2 = this.VRF.getNumCols();
        return  this.VRF.get(ti1 - 1, ti2 - 1);
    }
    
    
    abstract protected DMatrixRMaj _getVRF (final double tau, final double theta);
} // class Fmp

