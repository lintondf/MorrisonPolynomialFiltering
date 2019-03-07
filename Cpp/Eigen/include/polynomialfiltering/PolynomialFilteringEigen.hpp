#ifndef __POLYNOMIAL_FILTERING_HPP
#define __POLYNOMIAL_FILTERING_HPP

#include <iostream>
#include <exception>
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

	inline RealMatrix ones(Index N, Index M = 1) {
		return MatrixXd::Constant(N, M, 1.0);
	}

	inline RealMatrix solve(RealMatrix A, RealMatrix B) {
		return A.colPivHouseholderQr().solve(B);
	}

	inline RealMatrix inv(RealMatrix M) {
		return M.inverse();
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

	inline RealMatrix arrayDivide(RealMatrix a, RealMatrix b) {
		return a.array() / b.array();
	}

	inline long len(RealMatrix a) {
		return (long) (a.rows() * a.cols());
	}

	inline long len(RealVector a) {
		return (long) (a.size());
	}

	inline RealVector test() {
		return Map<RowVectorXd>(new double[3] { 1, 2, 3 }, 3);
	}


	class ValueError : public std::exception {
		std::string message; 
	public:
		ValueError(std::string message) {
			this->message = message;
		}

		virtual const char* what() const throw() {
			return message.c_str();
		}
	};
}


#endif // __POLYNOMIAL_