//testMain.cpp

#define DOCTEST_CONFIG_IMPLEMENT
#include <doctest.h>
#include <TestData.hpp>
#include <cmath>
#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
#include <polynomialfiltering/Main.hpp>

using namespace Eigen;
using namespace polynomialfiltering;

std::string TestData::testDataPath() {
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        std::string path = std::string(cwd);
        std::string testDir("Cpp/Eigen" );
        std::size_t where = path.find(testDir);
        if (where > 0) {
            path = path.replace(where, path.size()-where, "testdata");
            path = path.append( path.substr(where-1,1)); // append directory separator
            return path;
        }
    }
    return "";
}

TestData::TestData(std::string fileName) {
    std::string filePath = testDataPath();
    filePath += fileName;
    int retval, numgrps;
    retval = nc_open(filePath.c_str(), NC_NOWRITE, &ncid);
    //std::cout << "TestData: nc_open " << filePath << " -> " << retval << std::endl;
    if (retval == 0) {
        nc_inq_grps(ncid, &numgrps, NULL);
        int* grp_ncids = new int[numgrps];
        nc_inq_grps(ncid, &numgrps, grp_ncids);
        for (int g = 0; g < numgrps; g++) {
            char name[NC_MAX_NAME];
            nc_inq_grpname(grp_ncids[g], name);
            groupNames.push_back(name);
            groupIds.push_back(grp_ncids[g]);
        }
    }
}


TestData::~TestData() {
    nc_close(ncid);
}

const std::vector<std::string> TestData::getGroupNames() {
    return groupNames;
}

std::vector<std::string> TestData::getMatchingGroups(std::string testName) {
    std::vector<std::string> matches;
    for (int i = 0; i < groupNames.size(); i++) {
        if (groupNames.at(i).substr(0, testName.size()) == testName) {
            matches.push_back(groupNames.at(i));
        }
    }
    return matches;
}

Group TestData::getGroup( const std::string groupName ) {
    for (int i = 0; i < groupNames.size(); i++) {
        if (groupNames.at(i) == groupName) {
            int gid = groupIds.at(i);
            return gid;
        }
    }
    return -1;
}

RealMatrix TestData::getGroupVariable(std::string groupName, std::string variableName) {
    for (int i = 0; i < groupNames.size(); i++) {
        if (groupNames.at(i) == groupName) {
            int gid = groupIds.at(i);
            return getArray( gid, variableName);
        }
    }
    return RealMatrix::Zero(0, 0);
}

RealMatrix TestData::getArray( Group gid, std::string variableName ) {
    int vid;
    int status = nc_inq_varid(gid, variableName.c_str(), &vid);
    if (status != NC_NOERR) {
        throw ValueError("Missing test variable:" + variableName);
    }
    
    //int  rh_id;
    nc_type rh_type;
    int rh_ndims;
    int  rh_dimids[NC_MAX_VAR_DIMS];
    int rh_natts;
    nc_inq_var(gid, vid, 0, &rh_type, &rh_ndims, rh_dimids, &rh_natts);
    size_t count[2];
    count[0] = count[1] = 1;
    for (int j = 0; j < rh_ndims; j++) {
        size_t dval;
        char dname[NC_MAX_NAME];
        nc_inq_dim(gid, rh_dimids[j], dname, &dval);
        //std::cout << "              " << j << " " << dname << " " << dval << std::endl;
        count[j] = dval;
    }
    size_t start[2] = { 0, 0 };
    size_t numel = count[0] * count[1];
    //printf("%s: %d dims %zu * %zu = %zu\n", variableName.c_str(), rh_ndims, count[0], count[1], numel);
    double* data = new double[numel];
    nc_get_vara_double(gid, vid, start, count, data);
    Map<RealMatrix>  m(data, count[1], count[0]);
    RealMatrix out = m.transpose();
    delete[] data;
    return out;
}

double TestData::getScalar( Group gid, std::string variableName ) {
    RealMatrix m = getArray( gid, variableName );
    return m(0, 0);
}

int TestData::getInteger( Group gid, std::string variableName ) {
    return (int) getScalar(gid, variableName);
}

static double ulp(double t) {
    double ulpOne = 2.220446049250313e-16;
    int exp;
    double mantissa = frexp(t, &exp);
    exp--; // unbias exponent to match Java Math.getExponent
    return ulpOne * ::pow(2.0, (double) exp);
}

static double maxLog2Error = 0.0;
static std::string prefix = "";
static double threshold = 0.0; //1.5 * 1.0E-7;

void assert_almost_equal(double A, double B) {
    double max = std::max( fabs(A), fabs(B) );
    double u = ulp(max);
    double maxError = fabs(A-B);
    double threshold = 1.0*u;
    double log2Error = log2(maxError/u);
    if (log2Error > maxLog2Error) {
        maxLog2Error = log2Error;
    }
    prefix = "";
}


void assert_clear() {
    maxLog2Error = 0.0;
}

double assert_report( const std::string from ) {
    double result = maxLog2Error;
    printf("%-72s: %10.2f bits\n", from.c_str(), maxLog2Error);
    maxLog2Error = 0.0;
    return result;
}

void assertEqual(double limitBits, double actualBits) {
    CHECK(limitBits == actualBits);
}

void assertGreaterEqual(double limitBits, double actualBits) {
    CHECK(limitBits >= actualBits);
}

void assertTrue( bool tf ) {
    CHECK( tf );
}

void assertFalse( bool tf ) {
    CHECK( !tf );
}

void assert_almost_equal(const RealMatrix A, const RealMatrix B) {
    CHECK(A.rows() == B.rows());
    CHECK(A.cols() == B.cols());
    RealMatrix d = A - B;
    d = d.cwiseAbs();
    double elementMax = d.maxCoeff();
    char tag[32];
    if (elementMax > threshold) {
        for (int i = 0; i < A.rows(); i++) {
            for (int j = 0; j < B.cols(); j++) {
                sprintf(tag, "(%d,%d)", i,j);
                prefix = tag;
                assert_almost_equal(A(i,j), B(i,j));
            }
        }
    }
}

void assert_almost_equal(const RealMatrix A, const RealVector B) {
    CHECK(A.rows() == B.rows());
    CHECK(A.cols() == B.cols());
    RealMatrix d = A - B;
    d = d.cwiseAbs();
    double elementMax = d.maxCoeff();
    char tag[32];
    if (elementMax > threshold) {
        for (int i = 0; i < A.rows(); i++) {
            sprintf(tag, "(%d)", i);
            prefix = tag;
            assert_almost_equal(A(i,0), B(i,0));
        }
    }
}

void assert_almost_equal(const RealMatrix A, double B) {
	CHECK(A.rows() == 1);
	CHECK(A.cols() == 1);
	assert_almost_equal(A(0, 0), B);
}

void assert_almost_equal(double B, const RealMatrix A) {
	CHECK(A.rows() == 1);
	CHECK(A.cols() == 1);
	assert_almost_equal(A(0, 0), B);
}

void assert_array_less(const RealMatrix A, const RealMatrix B) {
	CHECK( (A.array() < B.array()).all() );
}

void assert_array_less(double A, double B) {
	CHECK(A < B);
}

void assert_not_empty(std::vector< std::string >& list) {
	CHECK(list.size() > 0);
}

TEST_CASE("testTesting") {
		TestData *testData = new TestData("test.nc");
		Group group = testData->getGroup("Test" );
		if (group == -1) {
			std::cerr << ("Test group not found") << std::endl;
			return;
		}
		int i = testData->getInteger(group, "i" );
		if (i != 1) {
			std::cerr << ("i != 1: ") << std::endl;
			std::cerr << i << std::endl;
			return;
		}
		double x = testData->getScalar(group, "x");
		if (x != 3.14) {
			std::cerr << ("x != 3.14: ") << std::endl;
			std::cerr << x << std::endl;
			return;
		}
		RealMatrix v = testData->getArray(group, "v");
		if (v.rows() != 3 || v.cols() != 1) {
			std::cerr << ("v wrong shape; should be 3,1") << std::endl;
			std::cerr << v << std::endl;
			return;
		}
		if (v(0, 0) != 1.0 || v(1, 0) != 2.0 || v(2, 0) != 3.0) {
			std::cerr << ("v content wrong; should be [1;2;3]") << std::endl;
			std::cerr << v << std::endl;
			return;
		}
		RealMatrix m = testData->getArray(group, "m" );
		if (m.rows() != 2 || m.cols() != 2) {
			std::cerr << ("m wrong shape; should be 2, 2") << std::endl;
			std::cerr << v << std::endl;
			return;
		}
		if (m(0, 0) != 4.0 || m(0, 1) != 5.0 || 
			m(1, 0) != 6.0 || m(1, 1) != 7.0) {
			std::cerr << ("m content wrong; should be [[4,5],[6,7]]") << std::endl;
			std::cerr << m << std::endl;
			return;
		}
#ifdef SKIP
		assertTrue(true);
		try {
			assertTrue(false);
			std::cerr << "assertTrue failed to fail" <<  std::endl;
			return;
		} catch (const std::exception& ae) {}
		assertFalse(false);
		try {
			assertFalse(true);
			std::cerr << "assertFalse failed to fail" <<  std::endl;
			return;
		} catch (const std::exception& ae) {}
		assertGreaterEqual(3.0, 2.0);
		assertGreaterEqual(3.0, 3.0);
		try {
			assertGreaterEqual(2.0, 3.0);
			std::cerr << "assertGreaterEqual failed to fail" <<  std::endl;
			return;
		} catch (const std::exception& ae) {}
		assertEqual(1, 1);
		try {
			assertEqual(2,1);
			std::cerr << "assertEqual int failed to fail" <<  std::endl;
			return;
		} catch (const std::exception& ae) {}
		assertEqual(1.0, 1.0);
		try {
			assertEqual(2.0,1.0);
			std::cerr << "assertEqual double failed to fail" <<  std::endl;
			return;
		} catch (const std::exception& ae) {}
		assertEqual(FilterStatus::COASTING, FilterStatus::COASTING);
		try {
			assertEqual(FilterStatus::COASTING, FilterStatus::IDLE);
			std::cerr << "assertEqual FilterStatus failed to fail" <<  std::endl;
			return;
		} catch (const std::exception& ae) {}
#endif		
		RealMatrix A(3,3);
		RealMatrix B(3,3);
		A.fill(1.0);
		B.fill(2.0);
		assert_array_less(A, B);
		// try {
		// 	assert_array_less(B, A);
		// 	std::cerr << "assert_array_less failed to fail" <<  std::endl;
		// 	return;
		// } catch (const std::exception& ae) {}
		
		A.resize(1, 1);
		A.fill(1.0);
		assert_clear();
		assert_almost_equal(1.0, A);
		assert_report("Expect 0.0");
		assert_almost_equal(2.0, A);
		assert_report("Expect 51");
		// try {
		// 	assert_almost_equal(1.0, B);			
		// 	std::cerr << "assert_almost_equal failed to fail" <<  std::endl;
		// 	return;
		// } catch (const std::exception& ae) {}
		
		// try {
		// 	B.resize(A.rows()+1, A.cols());
		// 	assert_almost_equal(A, B);
		// 	std::cerr << "assert_almost_equal failed to fail" <<  std::endl;
		// 	return;
		// } catch (const std::exception& ae) {}
		// try {
		// 	B.resize(A.rows(), A.cols()+1);
		// 	assert_almost_equal(A, B);
		// 	std::cerr << "assert_almost_equal failed to fail" <<  std::endl;
		// 	return;
		// } catch (const std::exception& ae) {}
		
		std::vector<std::string> ls;
        ls.push_back("a");
        ls.push_back("b");
		assert_not_empty( ls );
		ls.clear();
		// try {
		// 	assert_not_empty( ls );
		// 	std::cerr << "assert_not_empty failed to fail" <<  std::endl;
		// 	return;
		// } catch (const std::exception& ae) {}
		
		double a = 1.0;
		assert_clear();
		double b = assert_report("Should be 0.0" );
		double c = nextafter(a, a+1);
		assert_almost_equal( a, c );
		b = assert_report("Expect 0.0");
		c = nextafter(c, a+1);
		assert_almost_equal( a, c );
		b = assert_report("Expect 1.0");
		c = nextafter(c, a+1);
		double expecting[] = {5.49, 8.81, 12.13, 15.46, 18.78, 22.10, 25.42, 28.75, 32.07, 35.39, 38.71, 42.03, 45.36, 48.68, 51.00, 52.32};
		for (int j = -14; j <= 1; j++) {
			double p = ::pow(10.0, j);
			assert_clear();
			assert_almost_equal( a, a+p );
			if (fabs(maxLog2Error - expecting[14+j]) > 0.01) {
				std::cerr << "assert_almost_equal double incorrect" <<  std::endl;
                std::cerr << maxLog2Error << " " << expecting[14+j] << std::endl;
				return;				
			}
//			System.out.println(j + " " + maxLog2Error + " " + expecting[14+j]);
//			b = assert_report(String.format("Expect %5.1f", expecting[14+j]));
		}

		assert_clear();
		A.resize(3, 3);
		B.resize(3, 3);
		A.fill(1.0);
		for (int j = -14; j <= 1; j++) {
			double p = ::pow(10.0, j);
			assert_clear();
			B.fill(a+p);
			assert_almost_equal( A, B );
			if (fabs(maxLog2Error - expecting[14+j]) > 0.01) {
				std::cerr << "assert_almost_equal matrix incorrect" <<  std::endl;
				return;				
			}
//			b = assert_report(String.format("Expect %5.1f", expecting[14+j]));
		}
		std::cout << "Test of testing OK" <<  std::endl;
}

int main(int argc, char** argv) {
    doctest::Context  context;
    const char* args[] = { "", "-d", "--reporters=xml", NULL };
    context.applyCommandLine(2, args);
    int i = context.run(); // output);
    return i;
}
