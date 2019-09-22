/***** /polynomialfiltering/components/Emp/CoreEmp2/
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

 

///// @class CoreEmp2
/// @brief Class for the 2nd order expanding memory polynomial filter.
/// 
public class CoreEmp2 extends ICore {
    protected  int order;
    protected  double tau;
    
    public CoreEmp2() {}  // auto-generated null constructor


    ///// @brief Constructor
    /// 
    /// 
    ///  @param		tau	nominal time step
    /// 
    
    public CoreEmp2 (final double tau) {
                
        this.order = 2;
                
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
        double denom;
        DMatrixRMaj g = new DMatrixRMaj(3, 1);
                
        n2 = n * n;
                
        denom = 1.0 / ((n + 3) * (n + 2) * (n + 1));
        g = (new DMatrixRMaj(new double[] {3.0 * (3.0 * n2 + 3.0 * n + 2.0), 18.0 * (2.0 * n + 1.0), (2.0 * 1.0) * 30.0}));
                
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
        return (3.0 * (3.0 * Math.pow(n, 2) + 9.0 * n + 8.0)) / (n * (Math.pow(n, 2) - 1.0));
    }
    
    
    protected double _getLastVRF (final double n, final double tau) {
        return 720.0 / (n * Math.pow(tau, 4) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0));
    }
    
    
    protected DMatrixRMaj _getDiagonalVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(order + 1, order + 1);
                
        //  V = zeros(this.order + 1, this.order + 1)
        CommonOps_DDRM.fill( V, 0.0 );
                
        V.unsafe_set(0, 0, this._getFirstVRF(n, tau));
                
        V.unsafe_set(1, 1, (12.0 * ((n - 1.0) * (n + 3.0) + 15.0 * Math.pow((n + 2.0), 2))) / (n * Math.pow(tau, 2) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0)));
                
        V.unsafe_set(2, 2, this._getLastVRF(n, tau));
        return V;
    }
    
    
    protected DMatrixRMaj _getVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(order + 1, order + 1);
                
        V = this._getDiagonalVRF(n, tau);
                
        V.unsafe_set(0, 1, (18.0 * (2.0 * n + 3.0)) / (n * tau * (Math.pow(n, 2) - 1.0)));
                
        //  V(1, 0) = V(0, 1)
        double     td10 = V.get(0, 1);
        V.unsafe_set(1, 0, td10);
                
        V.unsafe_set(0, 2, 60.0 / (n * Math.pow(tau, 2) * (Math.pow(n, 2) - 1.0)));
                
        //  V(2, 0) = V(0, 2)
        double     td17 = V.get(0, 2);
        V.unsafe_set(2, 0, td17);
                
        V.unsafe_set(1, 2, 360.0 / (n * Math.pow(tau, 3) * (n - 1.0) * (n + 1.0) * (n + 3.0)));
                
        //  V(2, 1) = V(1, 2)
        double     td27 = V.get(1, 2);
        V.unsafe_set(2, 1, td27);
        return V;
    }
    
} // class Emp

