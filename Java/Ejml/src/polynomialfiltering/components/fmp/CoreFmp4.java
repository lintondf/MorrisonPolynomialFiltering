/***** /polynomialfiltering/components/Fmp/CoreFmp4/
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

 
public class CoreFmp4 extends AbstractCoreFmp {
    
    public CoreFmp4() {}  // auto-generated null constructor

    
    public CoreFmp4 (final double tau, final double theta) {
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
        double t5;
        double mt2;
        double mt3;
        double mt4;
        double mt5;
                
        t2 = t * t;
                
        t3 = t2 * t;
                
        t5 = t2 * t3;
                
        mt2 = (1 - t) * (1 - t);
                
        mt3 = (1 - t) * mt2;
                
        mt4 = mt2 * mt2;
                
        mt5 = mt2 * mt3;
        return (new DMatrixRMaj(new double[] {1. - t5, 5.0 / 12.0 * mt2 * (5. + 7. * t + 7. * t2 + 5. * t3), (2. * 1.) * 5.0 / 24.0 * mt3 * (7. + 10. * t + 7. * t2), (3. * 2. * 1.) * 5.0 / 12.0 * mt4 * (1. + t), (4. * 3. * 2. * 1.) * 1.0 / 24.0 * mt5}));
    }
    
    
    protected DMatrixRMaj _getVRF (final double u, final double t) {
        DMatrixRMaj V = new DMatrixRMaj(5, 5);
        double s;
                
        //  V = zeros(4 + 1, 4 + 1)
        CommonOps_DDRM.fill( V, 0.0 );
        if (t < 0.5) {
                        
            V.unsafe_set(0, 0, (-251.0 * Math.pow(t, 9) - 159.0 * Math.pow(t, 8) - 36.0 * Math.pow(t, 7) + 66.0 * Math.pow(t, 6) + 124.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0) / (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0));
                        
            V.unsafe_set(0, 1, (5.0 / 12.0 * (1100.0 * Math.pow(t, 9) - 182.0 * Math.pow(t, 8) - 816.0 * Math.pow(t, 7) - 707.0 * Math.pow(t, 6) - 170.0 * Math.pow(t, 5) + 285.0 * Math.pow(t, 4) + 292.0 * Math.pow(t, 3) + 151.0 * Math.pow(t, 2) + 42.0 * t + 5.0)) / (u * (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0)));
                        
            //  V(1, 0) = V(0, 1)
            double     td112 = V.get(0, 1);
            V.unsafe_set(1, 0, td112);
                        
            V.unsafe_set(0, 2, (1.0 / 12.0 * ((-6510.0 * Math.pow(t, 9) + 8190.0 * Math.pow(t, 8) + 4620.0 * Math.pow(t, 7)) - 2955.0 * Math.pow(t, 6) - 4850.0 * Math.pow(t, 5) - 425.0 * Math.pow(t, 4) + 880.0 * Math.pow(t, 3) + 755.0 * Math.pow(t, 2) + 260.0 * t + 35.0)) / (Math.pow(u, 2) * (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0)));
                        
            //  V(2, 0) = V(0, 2)
            double     td170 = V.get(0, 2);
            V.unsafe_set(2, 0, td170);
                        
            V.unsafe_set(0, 3, (5.0 / 2.0 * ((154.0 * Math.pow(t, 9) - 406.0 * Math.pow(t, 8) + 204.0 * Math.pow(t, 7) + 209.0 * Math.pow(t, 6)) - 136.0 * Math.pow(t, 5) - 39.0 * Math.pow(t, 4) - 4.0 * Math.pow(t, 3) + 11.0 * Math.pow(t, 2) + 6.0 * t + 1.0)) / (Math.pow(u, 3) * (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0)));
                        
            //  V(3, 0) = V(0, 3)
            double     td227 = V.get(0, 3);
            V.unsafe_set(3, 0, td227);
                        
            V.unsafe_set(0, 4, (-(Math.pow((t - 1.0), 5)) * (70.0 * Math.pow(t, 4) + 35.0 * Math.pow(t, 3) * (t + 1.0) + 15.0 * Math.pow(t, 2) * Math.pow((t + 1.0), 2) + 5.0 * t * Math.pow((t + 1.0), 3) + Math.pow((t + 1.0), 4))) / (Math.pow(u, 4) * Math.pow((t + 1.0), 9)));
                        
            //  V(4, 0) = V(0, 4)
            double     td258 = V.get(0, 4);
            V.unsafe_set(4, 0, td258);
                        
            V.unsafe_set(1, 1, (1.0 / 72.0 * ((-60995.0 * Math.pow(t, 9) + 55045.0 * Math.pow(t, 8) + 56220.0 * Math.pow(t, 7) + 4940.0 * Math.pow(t, 6)) - 37730.0 * Math.pow(t, 5) - 38370.0 * Math.pow(t, 4) - 1540.0 * Math.pow(t, 3) + 11980.0 * Math.pow(t, 2) + 8205.0 * t + 2245.0)) / (Math.pow(u, 2) * (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0)));
                        
            V.unsafe_set(1, 2, (25.0 / 72.0 * ((2913.0 * Math.pow(t, 9) - 5710.0 * Math.pow(t, 8) - 304.0 * Math.pow(t, 7) + 3608.0 * Math.pow(t, 6) + 2114.0 * Math.pow(t, 5)) - 1516.0 * Math.pow(t, 4) - 1528.0 * Math.pow(t, 3) - 184.0 * Math.pow(t, 2) + 389.0 * t + 218.0)) / (Math.pow(u, 3) * (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0)));
                        
            //  V(2, 1) = V(1, 2)
            double     td372 = V.get(1, 2);
            V.unsafe_set(2, 1, td372);
                        
            V.unsafe_set(1, 3, (-1.0 / 12.0 * (((8668.0 * Math.pow(t, 9) - 28763.0 * Math.pow(t, 8) + 24708.0 * Math.pow(t, 7) + 9452.0 * Math.pow(t, 6)) - 16892.0 * Math.pow(t, 5) - 858.0 * Math.pow(t, 4) + 1148.0 * Math.pow(t, 3) + 3292.0 * Math.pow(t, 2) + 288.0 * t) - 1043.0)) / (Math.pow(u, 4) * (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0)));
                        
            //  V(3, 1) = V(1, 3)
            double     td430 = V.get(1, 3);
            V.unsafe_set(3, 1, td430);
                        
            V.unsafe_set(1, 4, (5.0 / 6.0 * ((((285.0 * Math.pow(t, 9) - 1426.0 * Math.pow(t, 8) + 2732.0 * Math.pow(t, 7)) - 2356.0 * Math.pow(t, 6) + 710.0 * Math.pow(t, 5) + 80.0 * Math.pow(t, 4)) - 4.0 * Math.pow(t, 3) + 68.0 * Math.pow(t, 2)) - 139.0 * t + 50.0)) / (Math.pow(u, 5) * (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0)));
                        
            //  V(4, 1) = V(1, 4)
            double     td487 = V.get(1, 4);
            V.unsafe_set(4, 1, td487);
                        
            V.unsafe_set(2, 2, (-1.0 / 72.0 * (((87647.0 * Math.pow(t, 9) - 262227.0 * Math.pow(t, 8) + 155652.0 * Math.pow(t, 7) + 158508.0 * Math.pow(t, 6)) - 70518.0 * Math.pow(t, 5) - 160482.0 * Math.pow(t, 4) + 51492.0 * Math.pow(t, 3) + 54348.0 * Math.pow(t, 2)) - 273.0 * t - 14147.0)) / (Math.pow(u, 4) * (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0)));
                        
            V.unsafe_set(2, 3, (175.0 / 3.0 * (((15.0 * Math.pow(t, 9) - 65.0 * Math.pow(t, 8) + 91.0 * Math.pow(t, 7)) - 17.0 * Math.pow(t, 6) - 59.0 * Math.pow(t, 5) + 25.0 * Math.pow(t, 4) + 25.0 * Math.pow(t, 3)) - 11.0 * Math.pow(t, 2) - 8.0 * t + 4.0)) / (Math.pow(u, 5) * (Math.pow(t, 9) + 9.0 * Math.pow(t, 8) + 36.0 * Math.pow(t, 7) + 84.0 * Math.pow(t, 6) + 126.0 * Math.pow(t, 5) + 126.0 * Math.pow(t, 4) + 84.0 * Math.pow(t, 3) + 36.0 * Math.pow(t, 2) + 9.0 * t + 1.0)));
                        
            //  V(3, 2) = V(2, 3)
            double     td601 = V.get(2, 3);
            V.unsafe_set(3, 2, td601);
                        
            V.unsafe_set(2, 4, (-(Math.pow((t - 1.0), 7)) * (420.0 * Math.pow(t, 2) - 280.0 * t * (t - 1.0) + 385.0 / 6.0 * Math.pow((t - 1.0), 2) + 15.0 * Math.pow((t + 1.0), 2) + 35.0 * (t + 1.0) * (2.0 * t + 1.0))) / (Math.pow(u, 6) * Math.pow((t + 1.0), 9)));
                        
            //  V(4, 2) = V(2, 4)
            double     td632 = V.get(2, 4);
            V.unsafe_set(4, 2, td632);
                        
            V.unsafe_set(3, 3, (5.0 / 2.0 * Math.pow((t - 1.0), 6) * ((t + 1.0) * (8.0 * (-t + 1.0) * (t + 1.0) - 7.0 * (t - 1.0) * (5.0 * t + 3.0)) + 7.0 * (5.0 * t + 3.0) * ((-t + 1.0) * (t + 1.0) - (t - 1.0) * (5.0 * t + 3.0)))) / (Math.pow(u, 6) * Math.pow((t + 1.0), 9)));
                        
            V.unsafe_set(3, 4, (35.0 * Math.pow((t - 1.0), 7) * (-(-t + 1.0) * (t + 1.0) + (t - 1.0) * (5.0 * t + 3.0))) / (Math.pow(u, 7) * Math.pow((t + 1.0), 9)));
                        
            //  V(4, 3) = V(3, 4)
            double     td689 = V.get(3, 4);
            V.unsafe_set(4, 3, td689);
                        
            V.unsafe_set(4, 4, (70.0 * Math.pow((-t + 1.0), 9)) / (Math.pow(u, 8) * Math.pow((t + 1.0), 9)));
        } else {
                        
            s = 1 - t;
                        
            V.unsafe_set(0, 0, (s * (-1930.0 + s * (10970.0 + s * (-28100.0 + s * (42280.0 + s * (-40766.0 + s * (25722.0 + s * (-10344.0 + (2418.0 - 251.0 * s) * s)))))))) / (-512.0 + s * (2304.0 + s * (-4608.0 + s * (5376.0 + s * (-4032.0 + s * (2016.0 + s * (-672.0 + s * (144.0 + (-18.0 + s) * s)))))))));
                        
            V.unsafe_set(0, 1, (Math.pow(s, 2) * (-3249.9999999999995 + s * (16349.999999999998 + s * (-35887.5 + s * (44524.99999999999 + s * (-33702.08333333333 + s * (15553.33333333333 + s * (-4049.166666666666 + 458.3333333333333 * s)))))))) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * u));
                        
            //  V(1, 0) = V(0, 1)
            double     td788 = V.get(0, 1);
            V.unsafe_set(1, 0, td788);
                        
            V.unsafe_set(0, 2, (Math.pow(s, 3) * (-2909.9999999999995 + s * (12854.999999999998 + s * (-23931.66666666666 + s * (24011.249999999996 + s * (-13684.999999999998 + (4200. - 542.5 * s) * s)))))) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 2)));
                        
            //  V(2, 0) = V(0, 2)
            double     td831 = V.get(0, 2);
            V.unsafe_set(2, 0, td831);
                        
            V.unsafe_set(0, 3, (Math.pow(s, 4) * (-1350. + s * (5175. + s * (-8012.5 + s * (6249.999999999999 + s * (-2450. + 385. * s)))))) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 3)));
                        
            //  V(3, 0) = V(0, 3)
            double     td872 = V.get(0, 3);
            V.unsafe_set(3, 0, td872);
                        
            V.unsafe_set(0, 4, (Math.pow(s, 5) * (-256.0 + s * (837.0 + s * (-1044.0 + (588.0 - 126.0 * s) * s)))) / ((-512.0 + s * (2304.0 + s * (-4608.0 + s * (5376.0 + s * (-4032.0 + s * (2016.0 + s * (-672.0 + s * (144.0 + (-18.0 + s) * s)))))))) * Math.pow(u, 4)));
                        
            //  V(4, 0) = V(0, 4)
            double     td910 = V.get(0, 4);
            V.unsafe_set(4, 0, td910);
                        
            V.unsafe_set(1, 1, (Math.pow(s, 3) * (-7040.000000000001 + s * (28020. + s * (-47643.333333333336 + s * (44220. + s * (-23600.55555555556 + (6859.861111111111 - 847.1527777777778 * s) * s)))))) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 2)));
                        
            V.unsafe_set(1, 2, (Math.pow(s, 4) * (-6900. + s * (22450. + s * (-29962.5 + s * (20445.833333333332 + s * (-7120.48611111111 + 1011.4583333333333 * s)))))) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 3)));
                        
            //  V(2, 1) = V(1, 2)
            double     td993 = V.get(1, 2);
            V.unsafe_set(2, 1, td993);
                        
            V.unsafe_set(1, 3, (Math.pow(s, 5) * (-3344. + s * (8763. + s * (-8887.666666666666 + (4104.083333333333 - 722.3333333333333 * s) * s)))) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 4)));
                        
            //  V(3, 1) = V(1, 3)
            double     td1031 = V.get(1, 3);
            V.unsafe_set(3, 1, td1031);
                        
            V.unsafe_set(1, 4, (Math.pow(s, 6) * (-649.9999999999999 + s * (1319.9999999999998 + s * (-949.1666666666666 + 237.49999999999997 * s)))) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 5)));
                        
            //  V(4, 1) = V(1, 4)
            double     td1067 = V.get(1, 4);
            V.unsafe_set(4, 1, td1067);
                        
            V.unsafe_set(2, 2, (Math.pow(s, 5) * (-7055.999999999999 + s * (17611.999999999996 + s * (-16848.999999999996 + (7313.833333333332 - 1217.3194444444443 * s) * s)))) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 4)));
                        
            V.unsafe_set(2, 3, (Math.pow(s, 6) * (-3499.9999999999995 + s * (6474.999999999999 + s * (-4083.333333333333 + 874.9999999999999 * s)))) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 5)));
                        
            //  V(3, 2) = V(2, 3)
            double     td1140 = V.get(2, 3);
            V.unsafe_set(3, 2, td1140);
                        
            V.unsafe_set(2, 4, (Math.pow(s, 7) * (-689.9999999999999 + (865. - 289.16666666666663 * s) * s)) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 6)));
                        
            //  V(4, 2) = V(2, 4)
            double     td1173 = V.get(2, 4);
            V.unsafe_set(4, 2, td1173);
                        
            V.unsafe_set(3, 3, (Math.pow(s, 7) * (-1760. + (2110. - 632.5 * s) * s)) / ((-512. + s * (2304. + s * (-4608. + s * (5376. + s * (-4032. + s * (2016. + s * (-672. + s * (144. + (-18. + s) * s)))))))) * Math.pow(u, 6)));
                        
            V.unsafe_set(3, 4, (Math.pow(s, 8) * (-350.0 + 210.0 * s)) / ((-512.0 + s * (2304.0 + s * (-4608.0 + s * (5376.0 + s * (-4032.0 + s * (2016.0 + s * (-672.0 + s * (144.0 + (-18.0 + s) * s)))))))) * Math.pow(u, 7)));
                        
            //  V(4, 3) = V(3, 4)
            double     td1236 = V.get(3, 4);
            V.unsafe_set(4, 3, td1236);
                        
            V.unsafe_set(4, 4, (70.0 * Math.pow((-t + 1.0), 9)) / (Math.pow(u, 8) * Math.pow((t + 1.0), 9)));
        }
        return V;
    }
    
} // class Fmp

