/***** /polynomialfiltering/components/Emp/CoreEmp5/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.components.emp;
 
import java.util.stream.IntStream;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import polynomialfiltering.main.AbstractFilter;
import polynomialfiltering.main.AbstractFilterWithCovariance;
import static polynomialfiltering.main.Utility.*;
import polynomialfiltering.components.ICore;

 

///// @class CoreEmp5
/// @brief Class for the 5th order expanding memory polynomial filter.
/// 
public class CoreEmp5 extends ICore {
    protected  int order;
    protected  double tau;
    
    public CoreEmp5() {}  // auto-generated null constructor


    ///// @brief Constructor
    /// 
    /// 
    ///  @param		tau	nominal time step
    /// 
    
    public CoreEmp5 (final double tau) {
                
        this.order = 5;
                
        this.tau = tau;
    }
    
    
    public int getSamplesToStart () {
        return this.order + 2;
    }
    

    ///// @brief Get the innovation scale vector
    /// 
    /// 
    ///  @param		t	external time
    ///  @param		dtau	internal step
    /// 
    ///  @return  vector (order+1) of (observation-predict) multipliers
    /// 
    
    public DMatrixRMaj getGamma (final double n, final double dtau) {
        double n2;
        double n3;
        double n4;
        double denom;
        DMatrixRMaj g = new DMatrixRMaj(6, 1);
                
        n2 = n * n;
                
        n3 = n2 * n;
                
        n4 = n2 * n2;
                
        denom = 1.0 / ((n + 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1));
        g = (new DMatrixRMaj(new double[] {6.0 * (2.0 * n + 1.0) * (3.0 * n4 + 6.0 * n3 + 77.0 * n2 + 74.0 * n + 120.0), 126.0 * (5.0 * n4 + 10.0 * n3 + 55.0 * n2 + 50.0 * n + 28.0), (2.0 * 1.0) * 420.0 * (2.0 * n + 1.0) * (4.0 * n2 + 4.0 * n + 15.0), (3.0 * 2.0 * 1.0) * 1260.0 * (6.0 * n2 + 6.0 * n + 7.0), (4.0 * 3.0 * 2.0 * 1.0) * 3780.0 * (2.0 * n + 1.0), (5.0 * 4.0 * 3.0 * 2.0 * 1.0) * 2772.0}));
                
        //  g = denom * g
        CommonOps_DDRM.scale( denom, g, g );
        return g;
    }
    
    
    public double getFirstVRF (final int n) {
        return this._getFirstVRF(n, this.tau);
    }
    
    
    public double getLastVRF (final int n) {
        return this._getLastVRF(n, this.tau);
    }
    
    
    public DMatrixRMaj getDiagonalVRF (final int n) {
        
        return  this._getDiagonalVRF(n, this.tau);
    }
    
    
    public DMatrixRMaj getVRF (final int n) {
        
        return  this._getVRF(n, this.tau);
    }
    
    
    protected double _getFirstVRF (final double n, final double tau) {
        return (6.0 * (6.0 * Math.pow(n, 5) + 45.0 * Math.pow(n, 4) + 280.0 * Math.pow(n, 3) + 855.0 * Math.pow(n, 2) + 1334.0 * n + 840.0)) / (n * ((Math.pow(n, 5) - 9.0 * Math.pow(n, 4) + 25.0 * Math.pow(n, 3)) - 15.0 * Math.pow(n, 2) - 26.0 * n + 24.0));
    }
    
    
    protected double _getLastVRF (final double n, final double tau) {
        return 10059033600.0 / (n * Math.pow(tau, 10.0) * (n - 4.0) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0) * (n + 5.0) * (n + 6.0));
    }
    
    
    protected DMatrixRMaj _getDiagonalVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(order + 1, order + 1);
                
        //  V = zeros(this.order + 1, this.order + 1)
        CommonOps_DDRM.fill( V, 0.0 );
                
        V.unsafe_set(0, 0, this._getFirstVRF(n, tau));
                
        V.unsafe_set(1, 1, (588.0 * (25.0 * Math.pow(n, 8) + 500.0 * Math.pow(n, 7) + 4450.0 * Math.pow(n, 6) + 23300.0 * Math.pow(n, 5) + 79585.0 * Math.pow(n, 4) + 181760.0 * Math.pow(n, 3) + 267180.0 * Math.pow(n, 2) + 226920.0 * n + 84528.0)) / (n * Math.pow(tau, 2) * (((Math.pow(n, 10.0) + 11.0 * Math.pow(n, 9)) - 330.0 * Math.pow(n, 7) - 627.0 * Math.pow(n, 6) + 3003.0 * Math.pow(n, 5) + 7370.0 * Math.pow(n, 4)) - 9020.0 * Math.pow(n, 3) - 24024.0 * Math.pow(n, 2) + 6336.0 * n + 17280.0)));
                
        V.unsafe_set(2, 2, (70560.0 * (32.0 * Math.pow(n, 6) + 432.0 * Math.pow(n, 5) + 2480.0 * Math.pow(n, 4) + 7800.0 * Math.pow(n, 3) + 14418.0 * Math.pow(n, 2) + 14963.0 * n + 6690.0)) / (n * Math.pow(tau, 4) * (((Math.pow(n, 10.0) + 11.0 * Math.pow(n, 9)) - 330.0 * Math.pow(n, 7) - 627.0 * Math.pow(n, 6) + 3003.0 * Math.pow(n, 5) + 7370.0 * Math.pow(n, 4)) - 9020.0 * Math.pow(n, 3) - 24024.0 * Math.pow(n, 2) + 6336.0 * n + 17280.0)));
                
        V.unsafe_set(3, 3, (2721600.0 * (48.0 * Math.pow(n, 4) + 402.0 * Math.pow(n, 3) + 1274.0 * Math.pow(n, 2) + 1828.0 * n + 1047.0)) / (n * Math.pow(tau, 6) * (((Math.pow(n, 10.0) + 11.0 * Math.pow(n, 9)) - 330.0 * Math.pow(n, 7) - 627.0 * Math.pow(n, 6) + 3003.0 * Math.pow(n, 5) + 7370.0 * Math.pow(n, 4)) - 9020.0 * Math.pow(n, 3) - 24024.0 * Math.pow(n, 2) + 6336.0 * n + 17280.0)));
                
        V.unsafe_set(4, 4, (25401600.0 * ((n - 4.0) * (n + 6.0) + 99.0 * Math.pow((n + 2.0), 2))) / (n * Math.pow(tau, 8) * (n - 4.0) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0) * (n + 5.0) * (n + 6.0)));
                
        V.unsafe_set(5, 5, this._getLastVRF(n, tau));
        return V;
    }
    
    
    protected DMatrixRMaj _getVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(order + 1, order + 1);
                
        V = this._getDiagonalVRF(n, tau);
                
        V.unsafe_set(0, 1, (126.0 * (5.0 * Math.pow(n, 4) + 30.0 * Math.pow(n, 3) + 115.0 * Math.pow(n, 2) + 210.0 * n + 148.0)) / (n * tau * ((Math.pow(n, 5) - 9.0 * Math.pow(n, 4) + 25.0 * Math.pow(n, 3)) - 15.0 * Math.pow(n, 2) - 26.0 * n + 24.0)));
                
        //  V(1, 0) = V(0, 1)
        double     td30 = V.get(0, 1);
        V.unsafe_set(1, 0, td30);
                
        V.unsafe_set(0, 2, (840.0 * (8.0 * Math.pow(n, 3) + 36.0 * Math.pow(n, 2) + 82.0 * n + 69.0)) / (n * Math.pow(tau, 2) * ((Math.pow(n, 5) - 9.0 * Math.pow(n, 4) + 25.0 * Math.pow(n, 3)) - 15.0 * Math.pow(n, 2) - 26.0 * n + 24.0)));
                
        //  V(2, 0) = V(0, 2)
        double     td57 = V.get(0, 2);
        V.unsafe_set(2, 0, td57);
                
        V.unsafe_set(0, 3, (7560.0 * (6.0 * Math.pow(n, 2) + 18.0 * n + 19.0)) / (n * Math.pow(tau, 3) * ((Math.pow(n, 5) - 9.0 * Math.pow(n, 4) + 25.0 * Math.pow(n, 3)) - 15.0 * Math.pow(n, 2) - 26.0 * n + 24.0)));
                
        //  V(3, 0) = V(0, 3)
        double     td81 = V.get(0, 3);
        V.unsafe_set(3, 0, td81);
                
        V.unsafe_set(0, 4, (90720.0 * (2.0 * n + 3.0)) / (n * Math.pow(tau, 4) * ((Math.pow(n, 5) - 9.0 * Math.pow(n, 4) + 25.0 * Math.pow(n, 3)) - 15.0 * Math.pow(n, 2) - 26.0 * n + 24.0)));
                
        //  V(4, 0) = V(0, 4)
        double     td102 = V.get(0, 4);
        V.unsafe_set(4, 0, td102);
                
        V.unsafe_set(0, 5, 332640.0 / (n * Math.pow(tau, 5) * ((Math.pow(n, 5) - 9.0 * Math.pow(n, 4) + 25.0 * Math.pow(n, 3)) - 15.0 * Math.pow(n, 2) - 26.0 * n + 24.0)));
                
        //  V(5, 0) = V(0, 5)
        double     td120 = V.get(0, 5);
        V.unsafe_set(5, 0, td120);
                
        V.unsafe_set(1, 2, (17640.0 * (10.0 * Math.pow(n, 6) + 150.0 * Math.pow(n, 5) + 965.0 * Math.pow(n, 4) + 3420.0 * Math.pow(n, 3) + 7179.0 * Math.pow(n, 2) + 8520.0 * n + 4356.0)) / (n * Math.pow(tau, 3) * (((Math.pow(n, 9) + 9.0 * Math.pow(n, 8)) - 18.0 * Math.pow(n, 7) - 294.0 * Math.pow(n, 6) - 39.0 * Math.pow(n, 5) + 3081.0 * Math.pow(n, 4) + 1208.0 * Math.pow(n, 3)) - 11436.0 * Math.pow(n, 2) - 1152.0 * n + 8640.0)));
                
        //  V(2, 1) = V(1, 2)
        double     td168 = V.get(1, 2);
        V.unsafe_set(2, 1, td168);
                
        V.unsafe_set(1, 3, (105840.0 * (12.0 * Math.pow(n, 6) + 177.0 * Math.pow(n, 5) + 1125.0 * Math.pow(n, 4) + 3870.0 * Math.pow(n, 3) + 7550.0 * Math.pow(n, 2) + 7954.0 * n + 3588.0)) / (n * Math.pow(tau, 4) * (((Math.pow(n, 10.0) + 11.0 * Math.pow(n, 9)) - 330.0 * Math.pow(n, 7) - 627.0 * Math.pow(n, 6) + 3003.0 * Math.pow(n, 5) + 7370.0 * Math.pow(n, 4)) - 9020.0 * Math.pow(n, 3) - 24024.0 * Math.pow(n, 2) + 6336.0 * n + 17280.0)));
                
        //  V(3, 1) = V(1, 3)
        double     td216 = V.get(1, 3);
        V.unsafe_set(3, 1, td216);
                
        V.unsafe_set(1, 4, (211680.0 * (25.0 * Math.pow(n, 4) + 270.0 * Math.pow(n, 3) + 1205.0 * Math.pow(n, 2) + 2400.0 * n + 1692.0)) / (n * Math.pow(tau, 5) * (((Math.pow(n, 9) + 9.0 * Math.pow(n, 8)) - 18.0 * Math.pow(n, 7) - 294.0 * Math.pow(n, 6) - 39.0 * Math.pow(n, 5) + 3081.0 * Math.pow(n, 4) + 1208.0 * Math.pow(n, 3)) - 11436.0 * Math.pow(n, 2) - 1152.0 * n + 8640.0)));
                
        //  V(4, 1) = V(1, 4)
        double     td258 = V.get(1, 4);
        V.unsafe_set(4, 1, td258);
                
        V.unsafe_set(1, 5, (665280.0 * (15.0 * Math.pow(n, 4) + 165.0 * Math.pow(n, 3) + 770.0 * Math.pow(n, 2) + 1630.0 * n + 1284.0)) / (n * Math.pow(tau, 6) * (((Math.pow(n, 10.0) + 11.0 * Math.pow(n, 9)) - 330.0 * Math.pow(n, 7) - 627.0 * Math.pow(n, 6) + 3003.0 * Math.pow(n, 5) + 7370.0 * Math.pow(n, 4)) - 9020.0 * Math.pow(n, 3) - 24024.0 * Math.pow(n, 2) + 6336.0 * n + 17280.0)));
                
        //  V(5, 1) = V(1, 5)
        double     td300 = V.get(1, 5);
        V.unsafe_set(5, 1, td300);
                
        V.unsafe_set(2, 3, (1058400.0 * (16.0 * Math.pow(n, 4) + 144.0 * Math.pow(n, 3) + 506.0 * Math.pow(n, 2) + 822.0 * n + 549.0)) / (n * Math.pow(tau, 5) * (((Math.pow(n, 9) + 9.0 * Math.pow(n, 8)) - 18.0 * Math.pow(n, 7) - 294.0 * Math.pow(n, 6) - 39.0 * Math.pow(n, 5) + 3081.0 * Math.pow(n, 4) + 1208.0 * Math.pow(n, 3)) - 11436.0 * Math.pow(n, 2) - 1152.0 * n + 8640.0)));
                
        //  V(3, 2) = V(2, 3)
        double     td342 = V.get(2, 3);
        V.unsafe_set(3, 2, td342);
                
        V.unsafe_set(2, 4, (604800.0 * (120.0 * Math.pow(n, 4) + 1068.0 * Math.pow(n, 3) + 3766.0 * Math.pow(n, 2) + 6047.0 * n + 3594.0)) / (n * Math.pow(tau, 6) * (((Math.pow(n, 10.0) + 11.0 * Math.pow(n, 9)) - 330.0 * Math.pow(n, 7) - 627.0 * Math.pow(n, 6) + 3003.0 * Math.pow(n, 5) + 7370.0 * Math.pow(n, 4)) - 9020.0 * Math.pow(n, 3) - 24024.0 * Math.pow(n, 2) + 6336.0 * n + 17280.0)));
                
        //  V(4, 2) = V(2, 4)
        double     td384 = V.get(2, 4);
        V.unsafe_set(4, 2, td384);
                
        V.unsafe_set(2, 5, (139708800.0 * (Math.pow(n, 2) + 5.0 * n + 9.0)) / (n * Math.pow(tau, 7) * (((Math.pow(n, 9) + 9.0 * Math.pow(n, 8)) - 18.0 * Math.pow(n, 7) - 294.0 * Math.pow(n, 6) - 39.0 * Math.pow(n, 5) + 3081.0 * Math.pow(n, 4) + 1208.0 * Math.pow(n, 3)) - 11436.0 * Math.pow(n, 2) - 1152.0 * n + 8640.0)));
                
        //  V(5, 2) = V(2, 5)
        double     td419 = V.get(2, 5);
        V.unsafe_set(5, 2, td419);
                
        V.unsafe_set(3, 4, (114307200.0 * (5.0 * Math.pow(n, 2) + 21.0 * n + 23.0)) / (n * Math.pow(tau, 7) * (((Math.pow(n, 9) + 9.0 * Math.pow(n, 8)) - 18.0 * Math.pow(n, 7) - 294.0 * Math.pow(n, 6) - 39.0 * Math.pow(n, 5) + 3081.0 * Math.pow(n, 4) + 1208.0 * Math.pow(n, 3)) - 11436.0 * Math.pow(n, 2) - 1152.0 * n + 8640.0)));
                
        //  V(4, 3) = V(3, 4)
        double     td455 = V.get(3, 4);
        V.unsafe_set(4, 3, td455);
                
        V.unsafe_set(3, 5, (279417600.0 * (4.0 * Math.pow(n, 2) + 17.0 * n + 21.0)) / (n * Math.pow(tau, 8) * (((Math.pow(n, 10.0) + 11.0 * Math.pow(n, 9)) - 330.0 * Math.pow(n, 7) - 627.0 * Math.pow(n, 6) + 3003.0 * Math.pow(n, 5) + 7370.0 * Math.pow(n, 4)) - 9020.0 * Math.pow(n, 3) - 24024.0 * Math.pow(n, 2) + 6336.0 * n + 17280.0)));
                
        //  V(5, 3) = V(3, 5)
        double     td491 = V.get(3, 5);
        V.unsafe_set(5, 3, td491);
                
        V.unsafe_set(4, 5, 5029516800.0 / (n * Math.pow(tau, 9) * (n - 4.0) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 3.0) * (n + 4.0) * (n + 5.0) * (n + 6.0)));
                
        //  V(5, 4) = V(4, 5)
        double     td513 = V.get(4, 5);
        V.unsafe_set(5, 4, td513);
        return V;
    }
    
} // class Emp

