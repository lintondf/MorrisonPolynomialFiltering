/***** /polynomialfiltering/components/FixedMemoryPolynomialFilter/FixedMemoryFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.components.fixedmemorypolynomialfilter;
 
import java.util.stream.IntStream;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import polynomialfiltering.main.AbstractFilter;
import polynomialfiltering.main.AbstractFilterWithCovariance;
import static polynomialfiltering.main.Utility.*;
import polynomialfiltering.main.Utility.ValueError;
import org.ejml.interfaces.linsol.LinearSolverDense;
import org.ejml.dense.row.factory.LinearSolverFactory_DDRM;

 

///// @class FixedMemoryFilter
/// @brief Equally-weighted, fixed memory size, irregularly spaced data filter
/// 
/// Same units between state and observations
/// 
public class FixedMemoryFilter extends AbstractFilter {
    protected  int order; ///<  order of fitted polynomial
    protected  int L; ///<  number of samples in memory window
    protected  int n; ///<  total number of observations processed
    protected  int n0; ///<  number of observations required for valid result
    protected  double t0; ///<  start time of filter
    protected  double t; ///<  current time of filter
    protected  double tau; ///<  nominal step time of filter
    protected  DMatrixRMaj Z = new DMatrixRMaj(); ///<  UNNORMALIZED (external units) state vector
    protected  DMatrixRMaj tRing = new DMatrixRMaj(); ///<  ring buffer holding times of observations
    protected  DMatrixRMaj yRing = new DMatrixRMaj(); ///<  ring buffer holding values of observations
    
    public FixedMemoryFilter() {}  // auto-generated null constructor

    
    public FixedMemoryFilter(final int order) {
        this(order, 51);
    }
    
    public FixedMemoryFilter (final int order, final int memorySize) {
        super(order);
        if (order < 0 || order > 5) {
            throw new ValueError("Polynomial orders < 1 or > 5 are not supported");
        }
                
        this.order = order;
                
        this.L = memorySize;
                
        this.n = 0;
                
        this.n0 = memorySize;
                
        this.t0 = 0.0;
                
        this.t = 0.0;
                
        this.tau = 0.0;
                
        //  this.Z = zeros(this.order + 1)
        this.Z.reshape(this.order + 1, 1);
        CommonOps_DDRM.fill( this.Z, 0.0 );
                
        //  this.tRing = zeros(memorySize)
        this.tRing.reshape(memorySize, 1);
        CommonOps_DDRM.fill( this.tRing, 0.0 );
                
        //  this.yRing = zeros(memorySize)
        this.yRing.reshape(memorySize, 1);
        CommonOps_DDRM.fill( this.yRing, 0.0 );
        this.status = FilterStatus.IDLE;
    }
    
    
    public int getN () {
        return this.n;
    }
    
    
    public double getTau () {
        return this.tau;
    }
    
    
    public double getTime () {
        return this.t;
    }
    
    
    public DMatrixRMaj transitionState (final double t) {
        DMatrixRMaj dt = new DMatrixRMaj(L, 1); ///<  array of delta times
        DMatrixRMaj Tn = new DMatrixRMaj(L, order+1);
        DMatrixRMaj Tnt = new DMatrixRMaj(order+1, L); ///<  transpose of Tn
        DMatrixRMaj TntTn = new DMatrixRMaj(order+1, order+1);
        DMatrixRMaj TntYn = new DMatrixRMaj(order+1, 1);
                
        //  dt = this.tRing - t
        CommonOps_DDRM.subtract( this.tRing, t, dt );
                
        Tn = this._getTn(dt);
                
        //  Tnt = transpose(Tn)
        CommonOps_DDRM.transpose( Tn, Tnt );
                
        //  TntTn = Tnt * Tn
        CommonOps_DDRM.mult( Tnt, Tn, TntTn );
                
        //  TntYn = Tnt * this.yRing
        CommonOps_DDRM.mult( Tnt, this.yRing, TntYn );
                
        //  this.Z = solve(TntTn, TntYn)
        this.Z.reshape( TntTn.numRows, TntYn.numCols );
        LinearSolverDense<DMatrixRMaj> solver = LinearSolverFactory_DDRM.leastSquares(TntTn.numRows, TntTn.numCols);
        boolean ok = solver.setA(TntTn);
        solver.solve(TntYn, this.Z);
        
        return  new DMatrixRMaj(this.Z);
    }
    
    
    public DMatrixRMaj getState () {
        
        //  asssignment.dummy = return ( this.transitionState(this.t))
        DMatrixRMaj tm3 = this.transitionState(this.t);
        return tm3;
    }
    
    
    public void add(final double t, final double y) {
        add(t, y, "");
    }
    
    public void add (final double t, final double y, final String observationId) {
        int idx;
                
        this.t = t;
        idx = this.n % this.L;
                
        this.tRing.unsafe_set(0, idx, t);
                
        this.yRing.unsafe_set(0, idx, y);
        this.n += 1;
        if (this.n > this.L) {
            this.status = FilterStatus.RUNNING;
        } else {
            this.status = FilterStatus.INITIALIZING;
        }
    }
    
    
    public DMatrixRMaj getVRF () {
        DMatrixRMaj V = new DMatrixRMaj();
        if (this.n < this.L) {
                        
            //  V = zeros(this.order + 1, this.order + 1)
            V.reshape(this.order + 1, this.order + 1);
            CommonOps_DDRM.fill( V, 0.0 );
        } else {
                        
            V = this._transitionVrf(this.t);
        }
        return V;
    }
    
    
    public double getFirstVRF () {
        DMatrixRMaj V = new DMatrixRMaj();
                
        V = this.getVRF();
        
        return  V.get(0, 0);
    }
    
    
    public double getLastVRF () {
        DMatrixRMaj V = new DMatrixRMaj();
                
        V = this.getVRF();
        
        return  V.get(this.order, this.order);
    }
    
    
    protected DMatrixRMaj _transitionVrf (final double t) {
        DMatrixRMaj dt = new DMatrixRMaj();
        DMatrixRMaj Tn = new DMatrixRMaj();
        DMatrixRMaj V = new DMatrixRMaj();
                
        //  dt = this.tRing - t
        dt.reshape( this.tRing.numRows, this.tRing.numCols );
        CommonOps_DDRM.subtract( this.tRing, t, dt );
                
        Tn = this._getTn(dt);
                
        //  V = inv(transpose(Tn) * Tn)
        DMatrixRMaj tm3 = new DMatrixRMaj(Tn.getNumCols(), Tn.getNumRows());
        CommonOps_DDRM.transpose( Tn, tm3 );
        DMatrixRMaj tm4 = new DMatrixRMaj( tm3.numRows, Tn.numCols );
        CommonOps_DDRM.mult( tm3, Tn, tm4 );
        V.reshape( tm4.numRows, tm4.numCols );
        boolean ok = CommonOps_DDRM.invert(tm4, V);
        //TODO check ok;
        return V;
    }
    
    
    protected DMatrixRMaj _getTn (final DMatrixRMaj dt) {
        DMatrixRMaj Tn = new DMatrixRMaj();
        DMatrixRMaj C = new DMatrixRMaj();
        double fact;
                
        //  Tn = zeros(dt.getNumElements(), this.order + 1)
        Tn.reshape(dt.getNumElements(), this.order + 1);
        CommonOps_DDRM.fill( Tn, 0.0 );
                
        //  Tn( : , 0 : (1-1)) = ones(dt.getNumElements(), 1)
        DMatrixRMaj tm6 = new DMatrixRMaj( dt.getNumElements(), 1 );
        CommonOps_DDRM.fill( tm6, 1 );
        CommonOps_DDRM.insert( tm6, Tn, 0, 0 );
                
        CommonOps_DDRM.scale( 1.0, dt, C );
                
        fact = 1.0;
        for (int i = 1; i < this.order + 1; i++) {
            fact /= i;
                        
            //  Tn( : , i) = C * fact
            DMatrixRMaj tm11 = new DMatrixRMaj( C.numRows, C.numCols );
            CommonOps_DDRM.scale( fact, C, tm11 );
            CommonOps_DDRM.insert( tm11, Tn, 0, i );
                        
            //  C = C .* dt
            C.reshape( C.numRows, C.numCols );
            CommonOps_DDRM.elementMult( C, dt, C );
        }
        return Tn;
    }
    
} // class FixedMemoryPolynomialFilter

