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

void t1(const Matrix3d m) {
	std::cout << m << std::endl;
}

void t2(const Vector3d v) {
	std::cout << "V " << v << std::endl;
}

int main() {
	Matrix<double, 4, 4> mx;
	Matrix3d m = Matrix3d::Constant(2.0);
	t1(m);
	MatrixXd m1 = MatrixXd::Ones(3, 3);
	t1(m1);
	VectorXd v = VectorXd::Zero(3);
	t2(v);
	t2(m.col(1));
	t2(m1.col(2));
	t2(m.row(0));
	MatrixXd m2 = MatrixXd::Ones(10, 5);
	t2(m2.row(6).head(3));
	//(6, 2, 4.0);
	/*
	int N = 3;
	PMatrix m = MatrixXd::Identity(N, N);
	t1(m);
	PVector v = RealVector::Constant(N, 1, 1.0);
	t1(v);
	t2(PVector(m.block(0, 0, 1, N).transpose()));

	PVector vv(VectorXd::Constant(1.0));
	std::cout << m * v << std::endl;
	return 1;
	*/
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