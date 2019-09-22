/***** /polynomialfiltering/components/Fmp/CoreFmp2/
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

 
public class CoreFmp2 extends AbstractCoreFmp {
    
    public CoreFmp2() {}  // auto-generated null constructor

    
    public CoreFmp2 (final double tau, final double theta) {
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
        double t;
                
        t = this.theta;
        double t2;
        double t3;
        double mt2;
        double mt3;
                
        t2 = t * t;
                
        t3 = t2 * t;
                
        mt2 = (1 - t) * (1 - t);
                
        mt3 = (1 - t) * mt2;
        return (new DMatrixRMaj(new double[] {1. - t3, 3.0 / 2.0 * mt2 * (1. + t), (2. * 1.) * 1.0 / 2.0 * mt3}));
    }
    
    
    protected DMatrixRMaj _getVRF (final double u, final double t) {
        DMatrixRMaj V = new DMatrixRMaj(3, 3);
        double s;
                
        //  V = zeros(2 + 1, 2 + 1)
        CommonOps_DDRM.fill( V, 0.0 );
        if (t < 0.5) {
                        
            V.unsafe_set(0, 0, (1.0 + t * (5.0 + t * (10.0 + t * (8.0 + (-5.0 - 19.0 * t) * t)))) / (1.0 + t * (5.0 + t * (10.0 + t * (10.0 + t * (5.0 + t))))));
                        
            V.unsafe_set(0, 1, (1.5 + t * (6. + t * (6. + t * (-15. + t * (-19.5 + 21. * t))))) / ((1. + t * (5. + t * (10. + t * (10. + t * (5. + t))))) * u));
                        
            //  V(1, 0) = V(0, 1)
            double     td48 = V.get(0, 1);
            V.unsafe_set(1, 0, td48);
                        
            V.unsafe_set(0, 2, (1.0 + t * (2.0 + t * (-2.0 + t * (-16.0 + (25.0 - 10.0 * t) * t)))) / ((1.0 + t * (5.0 + t * (10.0 + t * (10.0 + t * (5.0 + t))))) * Math.pow(u, 2)));
                        
            //  V(2, 0) = V(0, 2)
            double     td73 = V.get(0, 2);
            V.unsafe_set(2, 0, td73);
                        
            V.unsafe_set(1, 1, (6.5 + t * (5.5 + t * (-31. + t * (-5. + (48.5 - 24.5 * t) * t)))) / ((1. + t * (5. + t * (10. + t * (10. + t * (5. + t))))) * Math.pow(u, 2)));
                        
            V.unsafe_set(1, 2, (6.0 + t * (-12.0 + t * (-12.0 + t * (48.0 + t * (-42.0 + 12.0 * t))))) / ((1.0 + t * (5.0 + t * (10.0 + t * (10.0 + t * (5.0 + t))))) * Math.pow(u, 3)));
                        
            //  V(2, 1) = V(1, 2)
            double     td123 = V.get(1, 2);
            V.unsafe_set(2, 1, td123);
                        
            V.unsafe_set(2, 2, (6.0 + t * (-30.0 + t * (60.0 + t * (-60.0 + (30.0 - 6.0 * t) * t)))) / ((1.0 + t * (5.0 + t * (10.0 + t * (10.0 + t * (5.0 + t))))) * Math.pow(u, 4)));
        } else {
                        
            s = 1.0 - t;
                        
            V.unsafe_set(0, 0, (s * (-66.0 + s * (186.0 + s * (-202.0 + (100.0 - 19.0 * s) * s)))) / (-32.0 + s * (80.0 + s * (-80.0 + s * (40.0 + (-10.0 + s) * s)))));
                        
            V.unsafe_set(0, 1, (Math.pow(s, 2) * (-54.00000000000001 + s * (117. + s * (-85.5 + 21. * s)))) / ((-32. + s * (80. + s * (-80. + s * (40. + (-10. + s) * s)))) * u));
                        
            //  V(1, 0) = V(0, 1)
            double     td197 = V.get(0, 1);
            V.unsafe_set(1, 0, td197);
                        
            V.unsafe_set(0, 2, (Math.pow(s, 3) * (-16.0 + (25.0 - 10.0 * s) * s)) / ((-32.0 + s * (80.0 + s * (-80.0 + s * (40.0 + (-10.0 + s) * s)))) * Math.pow(u, 2)));
                        
            //  V(2, 0) = V(0, 2)
            double     td220 = V.get(0, 2);
            V.unsafe_set(2, 0, td220);
                        
            V.unsafe_set(1, 1, (Math.pow(s, 3) * (-56. + (74. - 24.5 * s) * s)) / ((-32. + s * (80. + s * (-80. + s * (40. + (-10. + s) * s)))) * Math.pow(u, 2)));
                        
            V.unsafe_set(1, 2, (Math.pow(s, 4) * (-18.0 + 12.0 * s)) / ((-32.0 + s * (80.0 + s * (-80.0 + s * (40.0 + (-10.0 + s) * s)))) * Math.pow(u, 3)));
                        
            //  V(2, 1) = V(1, 2)
            double     td263 = V.get(1, 2);
            V.unsafe_set(2, 1, td263);
                        
            V.unsafe_set(2, 2, (-6.0 * Math.pow(s, 5)) / ((-32.0 + s * (80.0 + s * (-80.0 + s * (40.0 + (-10.0 + s) * s)))) * Math.pow(u, 4)));
        }
        return V;
    }
    
} // class Fmp

