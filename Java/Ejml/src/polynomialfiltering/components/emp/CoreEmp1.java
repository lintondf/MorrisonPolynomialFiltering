/***** /polynomialfiltering/components/Emp/CoreEmp1/
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

 

///// @class CoreEmp1
/// @brief Class for the 1st order expanding memory polynomial filter.
/// 
public class CoreEmp1 extends ICore {
    protected  int order;
    protected  double tau;
    
    public CoreEmp1() {}  // auto-generated null constructor


    ///// @brief Constructor
    /// 
    /// 
    ///  @param		tau	nominal time step
    /// 
    
    public CoreEmp1 (final double tau) {
                
        this.order = 1;
                
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
        double denom;
        DMatrixRMaj g = new DMatrixRMaj(2, 1);
                
        denom = 1.0 / ((n + 2) * (n + 1));
        g = (new DMatrixRMaj(new double[] {2.0 * (2.0 * n + 1.0), 6.0}));
                
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
        return (2.0 * (2.0 * n + 3.0)) / (n * (n + 1.0));
    }
    
    
    protected double _getLastVRF (final double n, final double tau) {
        return 12.0 / (n * Math.pow(tau, 2) * (n + 1.0) * (n + 2.0));
    }
    
    
    protected DMatrixRMaj _getDiagonalVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(2, 2);
                
        //  V = zeros(this.order + 1, this.order + 1)
        CommonOps_DDRM.fill( V, 0.0 );
                
        V.unsafe_set(0, 0, this._getFirstVRF(n, tau));
                
        V.unsafe_set(1, 1, this._getLastVRF(n, tau));
        return V;
    }
    
    
    protected DMatrixRMaj _getVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(2, 2);
                
        V = this._getDiagonalVRF(n, tau);
                
        V.unsafe_set(0, 1, 6.0 / (n * tau * (n + 1.0)));
                
        //  V(1, 0) = V(0, 1)
        double     td6 = V.get(0, 1);
        V.unsafe_set(1, 0, td6);
        return V;
    }
    
} // class Emp

