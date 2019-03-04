#ifndef FILTERING_HPP
#define FILTERING_HPP

#include <boost/tuple/tuple.hpp>
#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/matrix.hpp>

typedef boost::numeric::ublas::vector<double> RealVector;
typedef boost::numeric::ublas::matrix<double> RealMatrix;

class EditorDefault;

enum FilterStates {
	IDLE,         // Filter is awaiting the first observation
	INITIALIZING, // Filter has processed one or more observations, but state estimate is not reliable
	RUNNING,      // Filter state estimate is reliable
	COASTING,     // Filter has not received a recent observation, but the predicted state should be usable
	RESETING,     // Filter coast interval has been exceed and it will reinitialize on the next observation
};



class FilterBase {
public:
	FilterBase(unsigned n0 = 1);

	void restart(double t0, RealVector Z0);

	double getGoodnessOfFit(void);

	double getBiasOfFit(void);

	unsigned getN0(void);

	FilterStates getState(void);

	void setEditor(EditorDefault* editor);

	void setState(FilterStates state);

	virtual double getTime(void) = 0;

	virtual RealVector getState(double t) = 0;

	virtual bool add(double t, double y) = 0;

protected:
	double t0;
	double t;
	RealVector Z;
	unsigned n0;
	FilterStates state;
	EditorDefault* editor;

};

class EditorDefault {
public:
	EditorDefault(FilterBase* filter, std::size_t editingWindow = 25);

	void reset(void);

	void updateResiduals(double e);

	boost::tuples::tuple<double, double> getResidualStatitics(void);

	bool isGoodObservation(double t, double y, double e);

protected:
	FilterBase*     filter;
	unsigned        n;
	RealVector  E;
};

FilterBase::FilterBase(unsigned n0) :
	state(IDLE) {
	this->n0 = n0;
	this->editor = new EditorDefault(this);
}

void FilterBase::restart(double t0, RealVector Z0) {
	this->t0 = t0;
	this->t = t0;
	this->Z = Z0;
}

double FilterBase::getGoodnessOfFit(void) {
	return boost::tuples::get<1>(this->editor->getResidualStatitics());
}

double FilterBase::getBiasOfFit(void) {
	return boost::tuples::get<0>(this->editor->getResidualStatitics());
}

unsigned FilterBase::getN0(void) {
	return n0;
}

FilterStates FilterBase::getState(void) {
	return state;
}

void FilterBase::setEditor(EditorDefault* editor) {
	this->editor = editor;
}

void FilterBase::setState(FilterStates state) {
	this->state = state;
}


EditorDefault::EditorDefault(FilterBase* filter, std::size_t editingWindow) :
	filter(filter) {
	this->n = 0;
	this->E = RealVector(editingWindow);
}

void EditorDefault::reset() {
	this->n = 0;
	this->E *= 0.0;
}

void EditorDefault::updateResiduals(double e) {
	if (this->E.size() > 0) {
		this->E(this->n % this->E.size()) = e;
	}
	this->n++;
}

boost::tuples::tuple<double, double> EditorDefault::getResidualStatitics(void) {
	//accumulator_set<double, stats<tag::variance> > acc;
	//for_each(E.begin(), E.end(), boost::bind<void>(boost::ref(acc), _1) );
	return boost::tuples::tuple<double, double>(0.0, 0.0); // mean(acc), variance(acc));
}

bool EditorDefault::isGoodObservation(double t, double y, double e) {
	if (this->n >= this->filter->getN0()) {
		this->filter->setState(RUNNING);
	}
	else {
		this->filter->setState(INITIALIZING);
	}
	return false;
}

#endif