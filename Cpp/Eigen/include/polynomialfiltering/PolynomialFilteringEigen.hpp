#ifndef __POLYNOMIAL_FILTERING_HPP
#define __POLYNOMIAL_FILTERING_HPP

#include <iostream>
#include <Eigen/Dense>

using namespace Eigen;

namespace PolynomialFiltering {
	typedef VectorXd RealVector;
	typedef MatrixXd RealMatrix;

	// wrapper to match Python eye syntax for square matrices
	inline RealMatrix copy(RealMatrix m) {
		return m;
	}

	inline RealMatrix identity(Index N) {
		return MatrixXd::Identity(N, N);
	}

	inline RealMatrix ones(Index N, Index M) {
		return MatrixXd::Constant(N, M, 1.0);
	}

	inline RealMatrix solve(RealMatrix A, RealMatrix B) {
		return A.colPivHouseholderQr().solve(B);
	}

	inline RealMatrix transpose(RealMatrix M) {
		return M.transpose();
	}

	inline RealMatrix operator+(RealMatrix m, double x) {
		return m.array() + x;
	}

	inline RealMatrix operator-(RealMatrix m, double x) {
		return m.array() - x;
	}

	inline RealMatrix arrayTimes(RealMatrix a, RealMatrix b) {
		return a.array() * b.array();
	}

}


#endif // __POLYNOMIAL_