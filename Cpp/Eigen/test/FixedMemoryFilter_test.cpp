// FixedMemoryFilter_test.cpp

#include <iostream>
#include <vector>

#include <Windows.h>

#include <netcdf.h>
#include <Eigen/Dense>

#include <winconfig.h>
#include <cpptest.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/FixedMemoryPolynomialFilter.hpp>

using namespace Eigen;
using namespace PolynomialFiltering;


//typedef Matrix<double, Dynamic, Dynamic> RealMatrix;

#define BUFSIZE MAX_PATH
#define FILE_NAME "C:\\Users\\NOOK\\GITHUB\\ReynekeMorrisonFiltering\\testdata\\FixedMemoryFiltering.nc"

#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

class TestData {
public:
	TestData(std::string filePath) {
		int retval, numgrps;
		retval = nc_open(FILE_NAME, NC_NOWRITE, &ncid);
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

	~TestData() {
		nc_close(ncid);
	}

	const std::vector<std::string> getGroupNames() {
		return groupNames;
	}

	std::vector<std::string> getMatchingGroups(std::string testName) {
		std::vector<std::string> matches;
		for (int i = 0; i < groupNames.size(); i++) {
			if (groupNames.at(i).substr(0, testName.size()) == testName) {
				matches.push_back(groupNames.at(i));
			}
		}
		return matches;
	}

	RealMatrix getGroupVariable(std::string groupName, std::string variableName) {
		for (int i = 0; i < groupNames.size(); i++) {
			if (groupNames.at(i) == groupName) {
				int gid = groupIds.at(i);
				int vid;
				nc_inq_varid(gid, variableName.c_str(), &vid);

				//int  rh_id;
				nc_type rh_type;
				int rh_ndims;
				int  rh_dimids[NC_MAX_VAR_DIMS];
				int rh_natts;
				nc_inq_var(gid, vid, 0, &rh_type, &rh_ndims, rh_dimids, &rh_natts);
				size_t count[2];
				for (int j = 0; j < rh_ndims; j++) {
					size_t dval;
					char dname[NC_MAX_NAME];
					nc_inq_dim(gid, rh_dimids[j], dname, &dval);
					//std::cout << "              " << j << " " << dname << " " << dval << std::endl;
					count[j] = dval;
				}
				size_t start[2] = { 0, 0 };
				size_t numel = count[0] * count[1];
				double* data = new double[numel];
				nc_get_vara_double(gid, vid, start, count, data);
				Map<RealMatrix>  m(data, count[1], count[0]);
				return m.transpose();
			}
		}
		return RealMatrix::Zero(0,0);
	}

protected:
	int   ncid;  // root netCDF dataset id
	std::vector<std::string>  groupNames;
	std::vector<int>          groupIds;
};

class FixedMemoryFilterTestSuite : public Test::Suite
{
public:
	FixedMemoryFilterTestSuite() {
		TEST_ADD(FixedMemoryFilterTestSuite::first_test)
	}

protected:
	virtual void setup();
	virtual void tear_down() {} // remove resources...

	virtual RealMatrix execute(RealMatrix setup, RealMatrix data);

	void executeMatching(const std::string pattern);

private:
	TestData* testData;

	void first_test();
};

void FixedMemoryFilterTestSuite::setup() {
	testData = new TestData(FILE_NAME);
}

RealMatrix FixedMemoryFilterTestSuite::execute(RealMatrix setup, RealMatrix data) {
	int order = (int)setup(0);
	int window = (int)setup(1);
	int M = (int)setup(2);
	int iCheck = (int)setup(3);

	RealMatrix times = data.col(0);
	RealMatrix observations = data.col(1);

	Components::FixedMemoryFilter fixed(order, window);
	for (int i = 0; i < M; i++) {
		fixed.add(times(i), observations(i));
	}
	return fixed.getState(times(iCheck));
}

void FixedMemoryFilterTestSuite::executeMatching(const std::string pattern ) {
	std::vector<std::string> matches = testData->getMatchingGroups(pattern);
	for (int i = 0; i < matches.size(); i++) {
		RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
		RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
		RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

		RealMatrix actual = execute(setup, data);

		TEST_ASSERT(expected.isApprox(expected));
	}
}

void FixedMemoryFilterTestSuite::first_test() {
	executeMatching("testPerfect");
}

RealMatrix executePerfect(RealMatrix setup, RealMatrix data) {
	int order = (int)setup(0);
	int window = (int)setup(1);
	int M = (int)setup(2);
	int iCheck = (int)setup(3);
	
	RealMatrix times = data.col(0);
	RealMatrix observations = data.col(1);

	Components::FixedMemoryFilter fixed(order, window);
	for (int i = 0; i < M; i++) {
		fixed.add( times(i), observations(i) );
	}
	return fixed.getState(times(iCheck));
}

void testPerfect(TestData& testData) {
	std::vector<std::string> matches = testData.getMatchingGroups("testPerfect");
	for (int i = 0; i < matches.size(); i++) {
		RealMatrix setup = testData.getGroupVariable(matches.at(i), "setup");
		RealMatrix data = testData.getGroupVariable(matches.at(i), "data");
		RealMatrix expected = testData.getGroupVariable(matches.at(i), "expected");

		RealMatrix actual = executePerfect(setup, data);

		if (!expected.isApprox(expected)) {
			std::cout << i << ": " << (actual - expected) << std::endl;
		} else {
			std::cout << i << " PASSED" << std::endl;
		}
	}
}

int main() {
	Test::TextOutput output(Test::TextOutput::Verbose);
	FixedMemoryFilterTestSuite ts;
	return ts.run(output) ? EXIT_SUCCESS : EXIT_FAILURE;
	//TestData testData(FILE_NAME);
	//testPerfect(testData);

	//const std::vector<std::string> groups = testData.getGroupNames();
	//for (int i = 0; i < groups.size(); i++) {
	//	std::cout << groups.at(i) << std::endl;
	//}
	//std::vector<std::string> matches = testData.getMatchingGroups("testPerfect_2");
	//for (int i = 0; i < matches.size(); i++) {
	//	std::cout << matches.at(i) << std::endl;
	//	std::cout << testData.getGroupVariable(matches.at(i), "setup") << std::endl;
	//}

	return 0;

	//TCHAR Buffer[BUFSIZE];
	//DWORD dwRet;
	//dwRet = GetCurrentDirectory(BUFSIZE, Buffer);
	//std::cout << Buffer << std::endl;
	int ncid, retval, numgrps;

	/* Open the file. NC_NOWRITE tells netCDF we want read-only access
	 * to the file.*/
	if ((retval = nc_open(FILE_NAME, NC_NOWRITE, &ncid)))
		ERR(retval);
	std::cout << retval << " " << ncid << std::endl;

	if ((retval = nc_inq_grps(ncid, &numgrps, NULL)))
		ERR(retval);
	int* grp_ncids = new int[numgrps];
	nc_inq_grps(ncid, &numgrps, grp_ncids );

	for (int g = 0; g < numgrps; g++) {
		char name[NC_MAX_NAME];
		nc_inq_grpname(grp_ncids[g], name);
		int nvars;
		nc_inq_nvars(grp_ncids[g], &nvars);
		int* varids = new int[nvars];
		nc_inq_varids(grp_ncids[g], &nvars, varids);
		std::cout << g << " " << name << " " << nvars << std::endl;
		for (int i = 0; i < nvars; i++) {
			//int  rh_id;
			nc_type rh_type;
			int rh_ndims;
			int  rh_dimids[NC_MAX_VAR_DIMS];
			int rh_natts;
			nc_inq_var(grp_ncids[g], varids[i], 0, &rh_type, &rh_ndims, rh_dimids,	&rh_natts);
			char vname[NC_MAX_NAME];
			nc_inq_varname(grp_ncids[g], varids[i], vname);
			std::cout << "     " << i << " " << vname << " " <<  rh_type << " " << rh_ndims << std::endl;

			size_t count[2];
			for (int j = 0; j < rh_ndims; j++) {
				size_t dval;
				char dname[NC_MAX_NAME];
				nc_inq_dim(grp_ncids[g], rh_dimids[j], dname, &dval);
				//std::cout << "              " << j << " " << dname << " " << dval << std::endl;
				count[j] = dval;
			}
			size_t start[2] = { 0, 0 };
			size_t numel = count[0] * count[1];
			double* data = new double[numel];
			nc_get_vara_double(grp_ncids[g], varids[i], start, count, data);
			std::cout << "              ";
			for (int k = 0; k < numel; k++) {
				std::cout << data[k] << ", ";
			}
			std::cout << std::endl;
//			Map<Matrix<double, Dynamic, Dynamic>, 0, InnerStride<>>  m(data, count[0], count[1], InnerStride<>(count[1]));
//			Map<Matrix<double, Dynamic, Dynamic>>  m(data, count[1], count[0]);
			Map<RealMatrix>  m(data, count[1], count[0]);
			std::cout << m.transpose() << std::endl;
		}
	}
}