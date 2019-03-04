//EigenTest.cpp

//#include <iostream>
//#include <Eigen/Dense>
#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/FixedMemoryPolynomialFilter.hpp>
//using namespace Eigen;
//using namespace std;

using namespace PolynomialFiltering;

int main() {
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

	return 0;
}