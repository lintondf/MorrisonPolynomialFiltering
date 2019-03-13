#ifndef __POLYNOMIAL_FILTERING_HPP
#define __POLYNOMIAL_FILTERING_HPP

#include <iostream>
#include <exception>
#include <tuple>

namespace PolynomialFiltering {
	class PolynomialFilteringException : public std::exception {
	protected:
		std::string message;
	public:
		PolynomialFilteringException() :
			message("Polynomial Filtering Exception: ") {}


		virtual const char* what() const throw() {
			return message.c_str();
		}
	};

	class ValueError : public PolynomialFilteringException {
	public:
		ValueError(std::string message) {
			this->message += message;
		}

	};

	class EigenException : public PolynomialFilteringException {
	public:
		EigenException(std::string where) {
			this->message += "Fatai Eigen Exception; " + where;
		}
	};

}

#define eigen_assert(X) do { if(!(X)) throw ::PolynomialFiltering::EigenException(#X); } while(false);

#include <Eigen/Dense>

using namespace Eigen;
namespace PolynomialFiltering {

	typedef VectorXd RealVector;
	typedef MatrixXd RealMatrix;

	// wrapper to match Python eye syntax for square matrices
	inline RealMatrix copy(const RealMatrix& m) {
		return m;
	}

	inline RealMatrix identity(Index N) {
		return MatrixXd::Identity(N, N);
	}

	inline RealMatrix ones(Index N, Index M = 1) {
		return MatrixXd::Constant(N, M, 1.0);
	}

	inline RealVector diag(const RealMatrix& m) {
		return m.diagonal();
	}

	inline RealMatrix diag(const RealVector& v) {
		return v.asDiagonal();
	}

	inline RealMatrix sqrt(const RealMatrix& m) {
		return m.array().sqrt();
	}

	inline RealVector sqrt(const RealVector& v) {
		return v.array().sqrt();
	}

	inline RealMatrix zeros(Index N, Index M = 1) {
		return MatrixXd::Constant(N, M, 0.0);
	}

	inline RealMatrix solve(const RealMatrix& A, const RealMatrix& B) {
		return A.ldlt().solve(B); //  A.colPivHouseholderQr().solve(B);
	}

	inline RealMatrix inv(const RealMatrix& M) {
		return M.inverse();
	}

	inline RealMatrix transpose(const RealMatrix& M) {
		return M.transpose();
	}

	inline RealMatrix operator+(const RealMatrix& m, double x) {
		return m.array() + x;
	}

	inline RealMatrix operator-(const RealMatrix& m, double x) {
		return m.array() - x;
	}

	inline RealMatrix arrayTimes(const RealMatrix& a, const RealMatrix& b) {
		return a.array() * b.array();
	}

	inline RealMatrix arrayDivide(const RealMatrix& a, const RealMatrix& b) {
		return a.array() / b.array();
	}

	inline long len(const RealMatrix& a) {
		return (long) (a.rows() * a.cols());
	}

	inline long len(const RealVector& a) {
		return (long) (a.size());
	}

	inline RealVector test() {
		return Map<RowVectorXd>(new double[3] { 1, 2, 3 }, 3);
	}

}


#endif // __POLYNOMIAL_