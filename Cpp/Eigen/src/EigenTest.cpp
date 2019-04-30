//EigenTest.cpp

#include <iostream>
#include <Eigen/Dense>
#include <chrono>
#include<math.h>
#include <gsl/gsl_cdf.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
//#include <polynomialfiltering/Main.hpp>
//#include <polynomialfiltering/components/FixedMemoryPolynomialFilter.hpp>
using namespace Eigen;
//using namespace std;
using namespace polynomialfiltering;

class Timer
{
public:
	Timer() : beg_(clock_::now()) {}
	void reset() { beg_ = clock_::now(); }
	double elapsed() const {
		return std::chrono::duration_cast<second_>
			(clock_::now() - beg_).count();
	}

private:
	typedef std::chrono::high_resolution_clock clock_;
	typedef std::chrono::duration<double, std::ratio<1> > second_;
	std::chrono::time_point<clock_> beg_;
};

typedef VectorXd RealVector;
typedef MatrixXd RealMatrix;


void t1(const Matrix3d m) {
	std::cout << m << std::endl;
}

void t2(const Vector3d v) {
	std::cout << "V " << v << std::endl;
}

int main() {
	double x = 0.05;
	double nu = 2;
	double chicdf = 0;
	double chi = 0;
	Timer tmr;
	RealMatrix3 three;
	RealMatrix3 sum;
	for (int k = 0; k < 5; k++) {
		for (int i = 0; i < 100000000; i++) {
			three << x, 1 * x, 2 * x, 4 * x, 5 * x, 6 * x, 7 * x, 8 * x, 9 * x;  // 3.71 s, 3.39, 0.006427, 100xO2 0.6278

			sum += three;
			x += 1e-6;
			//chi += gsl_cdf_chisq_Pinv(1 - x, nu);
			//chicdf += gsl_cdf_chisq_P(3.0, nu);
		}
		double t = tmr.elapsed();
		std::cout << sum << std::endl;
		std::cout << "A " << t << std::endl;
		tmr.reset();
		sum = 0 * sum;
	}
	for (int k = 0; k < 5; k++) {
		for (int i = 0; i < 100000000; i++) {
			//three << x, 1 * x, 2 * x, 4 * x, 5 * x, 6 * x, 7 * x, 8 * x, 9 * x;  // 3.71 s, 3.39, 0.006427, 100xO2 0.6278
			three = (RealMatrix3() << x, 1 * x, 2 * x, 4 * x, 5 * x, 6 * x, 7 * x, 8 * x, 9 * x).finished(); //5.52 s, 5.99, 0.006234, 0.65595

			sum += three;
			x += 1e-6;
			//chi += gsl_cdf_chisq_Pinv(1 - x, nu);
			//chicdf += gsl_cdf_chisq_P(3.0, nu);
		}
		double t = tmr.elapsed();
		std::cout << sum << std::endl;
		std::cout << "B " << t << std::endl;
		tmr.reset();
		sum = 0 * sum;
	}
	for (int k = 0; k < 5; k++) {
		for (int i = 0; i < 100000000; i++) {
			//three << x, 1 * x, 2 * x, 4 * x, 5 * x, 6 * x, 7 * x, 8 * x, 9 * x;  // 3.71 s, 3.39, 0.006427, 100xO2 0.6278
			//three = (RealMatrix3() << x, 1 * x, 2 * x, 4 * x, 5 * x, 6 * x, 7 * x, 8 * x, 9 * x).finished(); //5.52 s, 5.99, 0.006234, 0.65595
			three(0, 0) = x;
			three(0, 1) = 1 * x;
			three(0, 2) = 2 * x;
			three(1, 0) = 4 * x;
			three(1, 1) = 5 * x;
			three(1, 2) = 6 * x;
			three(2, 0) = 7 * x;
			three(2, 1) = 8 * x;
			three(2, 2) = 9 * x; // 5.61, 5.3, 0.0062, 0.6796
			sum += three;
			x += 1e-6;
			//chi += gsl_cdf_chisq_Pinv(1 - x, nu);
			//chicdf += gsl_cdf_chisq_P(3.0, nu);
		}
		double t = tmr.elapsed();
		std::cout << sum << std::endl;
		std::cout << "C " << t << std::endl;
		tmr.reset();
		sum = 0 * sum;
	}
	/*
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
	*/
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