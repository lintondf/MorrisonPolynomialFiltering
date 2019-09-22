/***** /polynomialfiltering/components/Fmp/CoreFmp0/
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
import polynomialfiltering.components.fmp.AbstractCoreFmp;

 
public class CoreFmp0 extends AbstractCoreFmp {
    
    public CoreFmp0() {}  // auto-generated null constructor

    
    public CoreFmp0 (final double tau, final double theta) {
        super(tau,theta);
                
        this.VRF = this._getVRF(tau, theta);
    }
    

    ///// @brief Get the innovation scale vector
    /// 
    /// 
    ///  @param		t	external time
    ///  @param		dtau	internal step
    /// 
    ///  @return  vector (order+1) of (observation-predict) multipliers
    /// 
    
    public DMatrixRMaj getGamma (final double time, final double dtau) {
        return (new DMatrixRMaj(new double[] {1. - this.theta}));
    }
    
    
    protected DMatrixRMaj _getVRF (final double u, final double t) {
        DMatrixRMaj V = new DMatrixRMaj(1, 1);
                
        //  V = zeros(0 + 1, 0 + 1)
        CommonOps_DDRM.fill( V, 0.0 );
                
        V.unsafe_set(0, 0, (-t + 1.0) / (t + 1.0));
        return V;
    }
    
} // class Fmp

