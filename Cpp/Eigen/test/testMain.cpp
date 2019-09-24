//testMain.cpp

#define DOCTEST_CONFIG_IMPLEMENT
#include <doctest.h>
#include <TestData.hpp>
#include <cmath>
#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

using namespace Eigen;
using namespace polynomialfiltering;

std::string TestData::testDataPath() {
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        std::string path = std::string(cwd);
        std::string testDir("Cpp/Eigen/test");
        std::size_t where = path.find(testDir);
        if (where > 0) {
            path = path.replace(where, testDir.size(), "testdata");
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
    return ulpOne * pow(2.0, (double) exp);
}

static double maxLog2Error = 0.0;
static std::string prefix = "";
static double threshold = 1.5 * 1.0E-7;

void assert_almost_equal(double A, double B) {
    double max = std::max( fabs(A), fabs(B) );
    double u = ulp(max);
    double maxError = fabs(A-B);
    double threshold = 1.0*u;
    if (maxError > threshold) {
        double log2Error = log2(maxError/u);
        if (log2Error > maxLog2Error) {
            maxLog2Error = log2Error;
        }
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

int main(int argc, char** argv) {
    doctest::Context  context;
    const char* args[] = { "", "-d", "--reporters=xml", NULL };
    context.applyCommandLine(2, args);
    int i = context.run(); // output);
    return i;
}
