#include <fstream>

// include headers that implement a archive in simple text format
#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>

#include <boost/tuple/tuple.hpp>
#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/matrix.hpp>

typedef boost::numeric::ublas::vector<double> RealVector;
typedef boost::numeric::ublas::matrix<double> RealMatrix;

int main() {
	// create and open a character archive for output
	std::ofstream ofs("filename");

	// create class instance
	const RealVector g(3);
	g(0) = 10; g(1) = 20; g(2) = 30;

	// save data to archive
	{
		boost::archive::text_oarchive oa(ofs);
		// write class instance to archive
		oa << g;
		// archive and stream closed when destructors are called
	}

/*	// ... some time later restore the class instance to its orginal state
	gps_position newg;
	{
		// create and open an archive for input
		std::ifstream ifs("filename");
		boost::archive::text_iarchive ia(ifs);
		// read class state from archive
		ia >> newg;
		// archive and stream closed when destructors are called
	}
*/
	return 0;
}
