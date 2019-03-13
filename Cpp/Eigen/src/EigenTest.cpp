//EigenTest.cpp

#include <iostream>
#include <Eigen/Dense>
//#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
//#include <polynomialfiltering/Main.hpp>
//#include <polynomialfiltering/components/FixedMemoryPolynomialFilter.hpp>
using namespace Eigen;
//using namespace std;

typedef VectorXd RealVector;
typedef MatrixXd RealMatrix;


class PVector : public VectorXd {
public:
	PVector() : VectorXd() {
	}

	PVector(VectorXd v) : VectorXd(v) {

	}

	explicit operator VectorXd() const {
		(VectorXd)this;
	}
 };

class PMatrix : public MatrixXd {
public:
	PMatrix() : MatrixXd() {
	}

	PMatrix(MatrixXd v) : MatrixXd(v) {

	}
};

void t1(const PVector& m) {
	std::cout << "Vector " << m << std::endl;
}

void t1(const PMatrix& m) {
	std::cout << "Matrix " << m << std::endl;
}

void t2(const PVector& m) {
	std::cout << "Vector param " << m << std::endl;
}

int main() {
	int N = 3;
	PMatrix m = MatrixXd::Identity(N, N);
	t1(m);
	PVector v = RealVector::Constant(N, 1, 1.0);
	t1(v);
	t2(PVector(m.block(0, 0, 1, N).transpose()));

	PVector vv(VectorXd::Constant(1.0));
	std::cout << m * v << std::endl;
	return 1;

	/*
	RealMatrix  m;
	m = ArrayXXd::Zero(3, 5); // 
	std::cout << m << std::endl;
	m = MatrixXd::Identity(3, 5);
	std::cout << m << std::endl;


	//m = AbstractFilter::stateTransitionMatrix(5, 0.1);
	//std::cout << m << std::endl;

	Components::FixedMemoryFilter filter(3, 11);
	for (double t = 0.0; t < 1.2; t += 0.1) {
		filter.add(t, 100.0*t);
	}
	std::cout << filter.getTime() << " " << filter.getState(filter.getTime()) << std::endl;
	
	//Matrix3d m = Matrix3d::Random();
	//m = (m + Matrix3d::Constant(1.2)) * 50;
	//cout << "m =" << endl << m << endl;
	//Vector3d v(1, 2, 3);

	//cout << "m * v =" << endl << m * v << endl;
	*/
	return 0;
}