//testMain.cpp

#define DOCTEST_CONFIG_IMPLEMENT
#include <doctest.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

using namespace Eigen;
using namespace polynomialfiltering;


void assert_almost_equal(RealMatrix& A, RealMatrix& B) {
	CHECK(A.isApprox(B));
}

void assert_almost_equal(RealVector& A, RealVector& B) {
	CHECK(A.isApprox(B));
}

void assert_almost_equal(RealMatrix& A, double B) {
	CHECK(A.rows() == 1);
	CHECK(A.cols() == 1);
	CHECK(fabs(A(0, 0) - B) < 1e-12);
}

void assert_almost_equal(double B, RealMatrix& A) {
	CHECK(A.rows() == 1);
	CHECK(A.cols() == 1);
	CHECK(fabs(A(0, 0) - B) < 1e-12);
}

void assert_almost_equal(double A, double B) {
	CHECK(fabs(A - B) < 1e-12);
}

void assert_not_empty(std::vector< std::string >& list) {
	CHECK(list.size() > 0);
}

int main(int argc, char** argv) {
	doctest::Context  context;
	char* args[] = { "", "-d", "--reporters=xml", NULL };
	context.applyCommandLine(2, args);
	int i = context.run(); // output);
	return i;
}