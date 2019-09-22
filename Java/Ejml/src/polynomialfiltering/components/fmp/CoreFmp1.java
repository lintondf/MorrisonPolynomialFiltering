/***** /polynomialfiltering/components/Fmp/CoreFmp1/
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

 
public class CoreFmp1 extends AbstractCoreFmp {
    
    public CoreFmp1() {}  // auto-generated null constructor

    
    public CoreFmp1 (final double tau, final double theta) {
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
        double t2;
        double mt2;
        double t;
                
        t = this.theta;
                
        t2 = t * t;
                
        mt2 = (1 - t) * (1 - t);
        return (new DMatrixRMaj(new double[] {1. - t2, mt2}));
    }
    
    
    protected DMatrixRMaj _getVRF (final double u, final double t) {
        DMatrixRMaj V = new DMatrixRMaj(2, 2);
        double s;
                
        //  V = zeros(1 + 1, 1 + 1)
        CommonOps_DDRM.fill( V, 0.0 );
        if (t < 0.5) {
                        
            V.unsafe_set(0, 0, (1.0 + t * (3.0 + (1.0 - 5.0 * t) * t)) / (1.0 + t * (3.0 + t * (3.0 + t))));
                        
            V.unsafe_set(0, 1, (1.0 + t * (1.0 + t * (-5.0 + 3.0 * t))) / ((1.0 + t * (3.0 + t * (3.0 + t))) * u));
                        
            //  V(1, 0) = V(0, 1)
            double     td30 = V.get(0, 1);
            V.unsafe_set(1, 0, td30);
                        
            V.unsafe_set(1, 1, (2.0 + t * (-6.0 + (6.0 - 2.0 * t) * t)) / ((1.0 + t * (3.0 + t * (3.0 + t))) * Math.pow(u, 2)));
        } else {
                        
            s = 1.0 - t;
                        
            V.unsafe_set(0, 0, (s * (-10.0 + (14.0 - 5.0 * s) * s)) / (-8.0 + s * (12.0 + (-6.0 + s) * s)));
                        
            V.unsafe_set(0, 1, (Math.pow(s, 2) * (-4.0 + 3.0 * s)) / ((-8.0 + s * (12.0 + (-6.0 + s) * s)) * u));
                        
            //  V(1, 0) = V(0, 1)
            double     td75 = V.get(0, 1);
            V.unsafe_set(1, 0, td75);
                        
            V.unsafe_set(1, 1, (-2.0 * Math.pow(s, 3)) / ((-8.0 + s * (12.0 + (-6.0 + s) * s)) * Math.pow(u, 2)));
        }
        return V;
    }
    
} // class Fmp

