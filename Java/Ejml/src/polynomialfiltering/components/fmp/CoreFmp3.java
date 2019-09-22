/***** /polynomialfiltering/components/Fmp/CoreFmp3/
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

 
public class CoreFmp3 extends AbstractCoreFmp {
    
    public CoreFmp3() {}  // auto-generated null constructor

    
    public CoreFmp3 (final double tau, final double theta) {
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
        double t4;
        double mt2;
        double mt3;
        double mt4;
                
        t2 = t * t;
                
        t3 = t2 * t;
                
        t4 = t3 * t;
                
        mt2 = (1 - t) * (1 - t);
                
        mt3 = (1 - t) * mt2;
                
        mt4 = mt2 * mt2;
        return (new DMatrixRMaj(new double[] {1. - t4, 1.0 / 6.0 * mt2 * (11. + 14. * t + 11. * t2), (2. * 1.) * mt3 * (1. + t), (3. * 2. * 1.) * 1.0 / 6.0 * mt4}));
    }
    
    
    protected DMatrixRMaj _getVRF (final double u, final double t) {
        DMatrixRMaj V = new DMatrixRMaj(4, 4);
        double s;
                
        //  V = zeros(3 + 1, 3 + 1)
        CommonOps_DDRM.fill( V, 0.0 );
        if (t < 0.5) {
                        
            V.unsafe_set(0, 0, (1.0 + t * (7.0 + t * (21.0 + t * (35.0 + t * (33.0 + t * (7.0 + (-35.0 - 69.0 * t) * t)))))) / (1.0 + t * (7.0 + t * (21.0 + t * (35.0 + t * (35.0 + t * (21.0 + t * (7.0 + t))))))));
                        
            V.unsafe_set(0, 1, (1.8333333333333333 + t * (11.5 + t * (28.166666666666668 + t * (27.83333333333333 + t * (-35.166666666666664 + t * (-90.16666666666666 + t * (-48.166666666666664 + 104.16666666666666 * t))))))) / ((1. + t * (7. + t * (21. + t * (35. + t * (35. + t * (21. + t * (7. + t))))))) * u));
                        
            //  V(1, 0) = V(0, 1)
            double     td65 = V.get(0, 1);
            V.unsafe_set(1, 0, td65);
                        
            V.unsafe_set(0, 2, (2.0 + t * (10.0 + t * (14.0 + t * (-10.0 + t * (-94.0 + t * (10.0 + (158.0 - 90.0 * t) * t)))))) / ((1.0 + t * (7.0 + t * (21.0 + t * (35.0 + t * (35.0 + t * (21.0 + t * (7.0 + t))))))) * Math.pow(u, 2)));
                        
            //  V(2, 0) = V(0, 2)
            double     td98 = V.get(0, 2);
            V.unsafe_set(2, 0, td98);
                        
            V.unsafe_set(0, 3, (1.0 + t * (3.0 + t * (-1.0 + t * (-11.0 + t * (-41.0 + t * (133.0 + t * (-119.0 + 35.0 * t))))))) / ((1.0 + t * (7.0 + t * (21.0 + t * (35.0 + t * (35.0 + t * (21.0 + t * (7.0 + t))))))) * Math.pow(u, 3)));
                        
            //  V(3, 0) = V(0, 3)
            double     td133 = V.get(0, 3);
            V.unsafe_set(3, 0, td133);
                        
            V.unsafe_set(1, 1, (14.722222222222225 + t * (38.611111111111114 + t * (7.5 + t * (-131.94444444444446 + t * (-94.72222222222223 + t * (112.5 + (214.72222222222223 - 161.38888888888889 * t) * t)))))) / ((1. + t * (7. + t * (21. + t * (35. + t * (35. + t * (21. + t * (7. + t))))))) * Math.pow(u, 2)));
                        
            V.unsafe_set(1, 2, (24.999999999999996 + t * (11.666666666666666 + t * (-94.99999999999999 + t * (-94.99999999999999 + t * (221.66666666666666 + t * (155. + t * (-364.99999999999994 + 141.66666666666666 * t))))))) / ((1. + t * (7. + t * (21. + t * (35. + t * (35. + t * (21. + t * (7. + t))))))) * Math.pow(u, 3)));
                        
            //  V(2, 1) = V(1, 2)
            double     td199 = V.get(1, 2);
            V.unsafe_set(2, 1, td199);
                        
            V.unsafe_set(1, 3, (15.666666666666666 + t * (-33.666666666666664 + t * (-10.999999999999993 + t * (11.666666666666686 + t * (188.33333333333331 + t * (-349. + (233.66666666666666 - 55.666666666666664 * t) * t)))))) / ((1. + t * (7. + t * (21. + t * (35. + t * (35. + t * (21. + t * (7. + t))))))) * Math.pow(u, 4)));
                        
            //  V(3, 1) = V(1, 3)
            double     td233 = V.get(1, 3);
            V.unsafe_set(3, 1, td233);
                        
            V.unsafe_set(2, 2, (46.0 + t * (-78.0 + t * (-174.0 + t * (430.0 + t * (-30.0 + t * (-546.0 + (478.0 - 126.0 * t) * t)))))) / ((1.0 + t * (7.0 + t * (21.0 + t * (35.0 + t * (35.0 + t * (21.0 + t * (7.0 + t))))))) * Math.pow(u, 4)));
                        
            V.unsafe_set(2, 3, (30.0 + t * (-130.0 + t * (150.0 + t * (150.0 + t * (-550.0 + t * (570.0 + t * (-270.0 + 50.0 * t))))))) / ((1.0 + t * (7.0 + t * (21.0 + t * (35.0 + t * (35.0 + t * (21.0 + t * (7.0 + t))))))) * Math.pow(u, 5)));
                        
            //  V(3, 2) = V(2, 3)
            double     td301 = V.get(2, 3);
            V.unsafe_set(3, 2, td301);
                        
            V.unsafe_set(3, 3, (20.0 + t * (-140.0 + t * (420.0 + t * (-700.0 + t * (700.0 + t * (-420.0 + (140.0 - 20.0 * t) * t)))))) / ((1.0 + t * (7.0 + t * (21.0 + t * (35.0 + t * (35.0 + t * (21.0 + t * (7.0 + t))))))) * Math.pow(u, 6)));
        } else {
                        
            s = 1.0 - t;
                        
            V.unsafe_set(0, 0, (s * (-372.0 + s * (1580.0 + s * (-2878.0 + s * (2872.0 + s * (-1652.0 + (518.0 - 69.0 * s) * s)))))) / (-128.0 + s * (448.0 + s * (-672.0 + s * (560.0 + s * (-280.0 + s * (84.0 + (-14.0 + s) * s)))))));
                        
            V.unsafe_set(0, 1, (Math.pow(s, 2) * (-464. + s * (1668. + s * (-2437.333333333333 + s * (1808.333333333333 + s * (-681. + 104.16666666666666 * s)))))) / ((-128. + s * (448. + s * (-672. + s * (560. + s * (-280. + s * (84. + (-14. + s) * s)))))) * u));
                        
            //  V(1, 0) = V(0, 1)
            double     td404 = V.get(0, 1);
            V.unsafe_set(1, 0, td404);
                        
            V.unsafe_set(0, 2, (Math.pow(s, 3) * (-276.0 + s * (824.0 + s * (-932.0 + (472.0 - 90.0 * s) * s)))) / ((-128.0 + s * (448.0 + s * (-672.0 + s * (560.0 + s * (-280.0 + s * (84.0 + (-14.0 + s) * s)))))) * Math.pow(u, 2)));
                        
            //  V(2, 0) = V(0, 2)
            double     td437 = V.get(0, 2);
            V.unsafe_set(2, 0, td437);
                        
            V.unsafe_set(0, 3, (Math.pow(s, 4) * (-64.0 + s * (154.0 + s * (-126.0 + 35.0 * s)))) / ((-128.0 + s * (448.0 + s * (-672.0 + s * (560.0 + s * (-280.0 + s * (84.0 + (-14.0 + s) * s)))))) * Math.pow(u, 3)));
                        
            //  V(3, 0) = V(0, 3)
            double     td468 = V.get(0, 3);
            V.unsafe_set(3, 0, td468);
                        
            V.unsafe_set(1, 1, (Math.pow(s, 3) * (-740. + s * (1960. + s * (-1988.3333333333335 + (914.9999999999999 - 161.38888888888889 * s) * s)))) / ((-128. + s * (448. + s * (-672. + s * (560. + s * (-280. + s * (84. + (-14. + s) * s)))))) * Math.pow(u, 2)));
                        
            V.unsafe_set(1, 2, (Math.pow(s, 4) * (-479.99999999999994 + s * (939.9999999999999 + s * (-626.6666666666666 + 141.66666666666666 * s)))) / ((-128. + s * (448. + s * (-672. + s * (560. + s * (-280. + s * (84. + (-14. + s) * s)))))) * Math.pow(u, 3)));
                        
            //  V(2, 1) = V(1, 2)
            double     td531 = V.get(1, 2);
            V.unsafe_set(2, 1, td531);
                        
            V.unsafe_set(1, 3, (Math.pow(s, 5) * (-116. + (156. - 55.666666666666664 * s) * s)) / ((-128. + s * (448. + s * (-672. + s * (560. + s * (-280. + s * (84. + (-14. + s) * s)))))) * Math.pow(u, 4)));
                        
            //  V(3, 1) = V(1, 3)
            double     td559 = V.get(1, 3);
            V.unsafe_set(3, 1, td559);
                        
            V.unsafe_set(2, 2, (Math.pow(s, 5) * (-324.0 + (404.0 - 126.0 * s) * s)) / ((-128.0 + s * (448.0 + s * (-672.0 + s * (560.0 + s * (-280.0 + s * (84.0 + (-14.0 + s) * s)))))) * Math.pow(u, 4)));
                        
            V.unsafe_set(2, 3, (Math.pow(s, 6) * (-80.0 + 50.0 * s)) / ((-128.0 + s * (448.0 + s * (-672.0 + s * (560.0 + s * (-280.0 + s * (84.0 + (-14.0 + s) * s)))))) * Math.pow(u, 5)));
                        
            //  V(3, 2) = V(2, 3)
            double     td612 = V.get(2, 3);
            V.unsafe_set(3, 2, td612);
                        
            V.unsafe_set(3, 3, (-20.0 * Math.pow(s, 7)) / ((-128.0 + s * (448.0 + s * (-672.0 + s * (560.0 + s * (-280.0 + s * (84.0 + (-14.0 + s) * s)))))) * Math.pow(u, 6)));
        }
        return V;
    }
    
} // class Fmp

