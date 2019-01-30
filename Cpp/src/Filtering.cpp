#include <iostream>

#include <boost/bind/bind.hpp>
#include "boost/math/special_functions/pow.hpp"
#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/lu.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <boost/math/special_functions/factorials.hpp>
#include "boost/tuple/tuple.hpp"
#include <boost/accumulators/accumulators.hpp>
#include "boost/accumulators/statistics/stats.hpp"
#include "boost/accumulators/statistics/mean.hpp"
#include "boost/accumulators/statistics/variance.hpp"
#include "boost/accumulators/statistics/moment.hpp"

/*
yes, you can solve linear equations with boost's ublas library. Here is one short way using LU-factorize and back-substituting to get the inverse:

using namespace boost::ublas;

Ainv = identity_matrix<float>(A.size1());
permutation_matrix<size_t> pm(A.size1());
lu_factorize(A,pm)
lu_substitute(A, pm, Ainv);
So to solve a linear system Ax=y, you would solve the equation trans(A)Ax=trans(A)y by taking the inverse of (trans(A)A)^-1 to get x: x = (trans(A)A)^-1Ay.

shareimprove this answer
answered Aug 19 '09 at 3:51

Inverse
3,45722032
10
If all you need is a solution for Ax=y, just use permutation_matrix<size_t> pm(A.size1()); lu_factorize(A, pm); lu_substitute(A, pm, y); and y is replaced with the solution. – Joey Jul 10 '14 at 17:24
*/

using namespace boost::accumulators;

using namespace boost::numeric::ublas;
using namespace boost::tuples;

matrix<double> stateTransitionMatrix(const std::size_t N, double dt) {
	matrix<double> B = identity_matrix<double>(N);
	for (std::size_t i = 0; i < N; i++) {
		for (std::size_t j = i + 1; j < N; j++) {
			unsigned ji = (unsigned) (j - i);
			double fji = boost::math::factorial<double>(ji);
			B(i, j) = pow(dt, ji) / fji;
		}
	}
	return B;
}

class EditorDefault;
class FilterBase;

enum FilterStates {
	IDLE,         // Filter is awaiting the first observation
	INITIALIZING, // Filter has processed one or more observations, but state estimate is not reliable
	RUNNING,      // Filter state estimate is reliable
	COASTING,     // Filter has not received a recent observation, but the predicted state should be usable
	RESETING,     // Filter coast interval has been exceed and it will reinitialize on the next observation
};

class FilterBase {
public:
	FilterBase(unsigned n0 = 1) :
		state(IDLE) {
		this->n0 = n0;
		this->editor = new EditorDefault(this);
	}

	void restart(double t0, vector<double> Z0) {
		this->t0 = t0;
		this->t = t0;
		this->Z = Z0;
	}

	double getGoodnessOfFit() {
		get<1>(this->editor->getResidualStatitics());
	}

	double getBiasOfFit() {
		get<0>(this->editor->getResidualStatitics());
	}

	virtual double getTime() = 0;

	virtual vector<double> getState(double t) = 0;

	virtual bool add(double t, double y) = 0;


	unsigned getN0() {
		return n0;
	}

	FilterStates getState() {
		return state;
	}

	void setEditor(EditorDefault* editor) {
		this->editor = editor;
	}

	void setState(FilterStates state) {
		this->state = state;
	}

protected:
	double t0;
	double t;
	double Z;
	unsigned n0;
	FilterStates state;
	EditorDefault* editor;

};
class EditorDefault {
public:
	EditorDefault(FilterBase* filter, std::size_t editingWindow = 25) :
		filter(filter) {
		this->n = 0;
		this->E = vector<double>(editingWindow);
	}

	void reset() {
		this->n = 0;
		this->E *= 0.0;
	}

	void updateResiduals(double e) {
		if (this->E.size() > 0) {
			this->E(this->n % this->E.size()) = e;
		}
		this->n++;
	}

	tuple<double, double> getResidualStatitics(void) {
		accumulator_set<double, stats<tag::variance> > acc;
		for_each(E.begin(), E.end(), boost::bind<void>(boost::ref(acc), _1) );
		return tuple<double, double>(mean(acc), variance(acc));
	}

	bool isGoodObservation(double t, double y, double e) {
		if (this->n >= this->filter->getN0()) {
			this->filter->setState(RUNNING);
		} else {
			this->filter->setState(INITIALIZING);
		}
	}

protected:
	FilterBase*     filter;
	unsigned        n;
	vector<double>  E;
};
int main() {
	using namespace boost::numeric::ublas;

	matrix<double> TntTn(3,3);
	TntTn(0, 0) = 11.0; TntTn(0, 1) = -5.5; TntTn(0, 2) = 3.85;
	TntTn(1, 0) = -5.5; TntTn(1, 1) = 3.85; TntTn(1, 2) = -3.025;
	TntTn(2, 0) = 3.85; TntTn(2, 1) = -3.025; TntTn(2, 2) = 2.5333;
	vector<double> TntYn(3);
	TntYn(0) = 45.99012356;
	TntYn(1) = -9.88611426;
	TntYn(2) = 0.36213461;

	std::cout << TntTn << std::endl;
	std::cout << TntYn << std::endl;

	permutation_matrix<std::size_t> pm(TntTn.size1());
	lu_factorize(TntTn, pm); 
	lu_substitute(TntTn, pm, TntYn);
	std::cout << TntYn << std::endl;

	std::cout << stateTransitionMatrix(8, 0.1) << std::endl;
	return 0;
}
