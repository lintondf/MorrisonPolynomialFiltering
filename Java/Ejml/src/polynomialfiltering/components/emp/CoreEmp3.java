/***** /polynomialfiltering/components/Emp/CoreEmp3/
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

 

///// @class CoreEmp3
/// @brief Class for the 3rd order expanding memory polynomial filter.
/// 
public class CoreEmp3 extends ICore {
    protected  int order;
    protected  double tau;
    
    public CoreEmp3() {}  // auto-generated null constructor


    ///// @brief Constructor
    /// 
    /// 
    ///  @param		tau	nominal time step
    /// 
    
    public CoreEmp3 (final double tau) {
                
        this.order = 3;
                
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
        double denom;
        DMatrixRMaj g = new DMatrixRMaj(4, 1);
                
        n2 = n * n;
                
        n3 = n2 * n;
                
        denom = 1.0 / ((n + 4) * (n + 3) * (n + 2) * (n + 1));
        g = (new DMatrixRMaj(new double[] {8.0 * (2.0 * n3 + 3.0 * n2 + 7.0 * n + 3.0), 20.0 * (6.0 * n2 + 6.0 * n + 5.0), (2.0 * 1.0) * 120.0 * (2.0 * n + 1.0), (3.0 * 2.0 * 1.0) * 140.0}));
                
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
        return (8.0 * (2.0 * Math.pow(n, 3) + 9.0 * Math.pow(n, 2) + 19.0 * n + 15.0)) / (n * (Math.pow(n, 3) - 2.0 * Math.pow(n, 2) - n + 2.0));
    }
    
    
    protected double _getLastVRF (final double n, final double tau) {
        return 100800.0 / (n * Math.pow(tau, 6) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0));
    }
    
    
    protected DMatrixRMaj _getDiagonalVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(order + 1, order + 1);
                
        //  V = zeros(this.order + 1, this.order + 1)
        CommonOps_DDRM.fill( V, 0.0 );
                
        V.unsafe_set(0, 0, this._getFirstVRF(n, tau));
                
        V.unsafe_set(1, 1, (200.0 * (6.0 * Math.pow(n, 4) + 51.0 * Math.pow(n, 3) + 159.0 * Math.pow(n, 2) + 219.0 * n + 116.0)) / (n * Math.pow(tau, 2) * ((Math.pow(n, 6) + 7.0 * Math.pow(n, 5) + 7.0 * Math.pow(n, 4)) - 35.0 * Math.pow(n, 3) - 56.0 * Math.pow(n, 2) + 28.0 * n + 48.0)));
                
        V.unsafe_set(2, 2, (720.0 * ((n - 2.0) * (n + 4.0) + 35.0 * Math.pow((n + 2.0), 2))) / (n * Math.pow(tau, 4) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0)));
                
        V.unsafe_set(3, 3, this._getLastVRF(n, tau));
        return V;
    }
    
    
    protected DMatrixRMaj _getVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(order + 1, order + 1);
                
        V = this._getDiagonalVRF(n, tau);
                
        V.unsafe_set(0, 1, (20.0 * (6.0 * Math.pow(n, 2) + 18.0 * n + 17.0)) / (n * tau * (Math.pow(n, 3) - 2.0 * Math.pow(n, 2) - n + 2.0)));
                
        //  V(1, 0) = V(0, 1)
        double     td17 = V.get(0, 1);
        V.unsafe_set(1, 0, td17);
                
        V.unsafe_set(0, 2, (240.0 * (2.0 * n + 3.0)) / (n * Math.pow(tau, 2) * (Math.pow(n, 3) - 2.0 * Math.pow(n, 2) - n + 2.0)));
                
        //  V(2, 0) = V(0, 2)
        double     td31 = V.get(0, 2);
        V.unsafe_set(2, 0, td31);
                
        V.unsafe_set(0, 3, 840.0 / (n * Math.pow(tau, 3) * (Math.pow(n, 3) - 2.0 * Math.pow(n, 2) - n + 2.0)));
                
        //  V(3, 0) = V(0, 3)
        double     td42 = V.get(0, 3);
        V.unsafe_set(3, 0, td42);
                
        V.unsafe_set(1, 2, (600.0 * (9.0 * Math.pow(n, 2) + 39.0 * n + 40.0)) / (n * Math.pow(tau, 3) * ((Math.pow(n, 5) + 5.0 * Math.pow(n, 4)) - 3.0 * Math.pow(n, 3) - 29.0 * Math.pow(n, 2) + 2.0 * n + 24.0)));
                
        //  V(2, 1) = V(1, 2)
        double     td66 = V.get(1, 2);
        V.unsafe_set(2, 1, td66);
                
        V.unsafe_set(1, 3, (1680.0 * (6.0 * Math.pow(n, 2) + 27.0 * n + 32.0)) / (n * Math.pow(tau, 4) * ((Math.pow(n, 6) + 7.0 * Math.pow(n, 5) + 7.0 * Math.pow(n, 4)) - 35.0 * Math.pow(n, 3) - 56.0 * Math.pow(n, 2) + 28.0 * n + 48.0)));
                
        //  V(3, 1) = V(1, 3)
        double     td93 = V.get(1, 3);
        V.unsafe_set(3, 1, td93);
                
        V.unsafe_set(2, 3, 50400.0 / (n * Math.pow(tau, 5) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 3.0) * (n + 4.0)));
                
        //  V(3, 2) = V(2, 3)
        double     td107 = V.get(2, 3);
        V.unsafe_set(3, 2, td107);
        return V;
    }
    
} // class Emp

