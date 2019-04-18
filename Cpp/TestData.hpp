#pragma once
#ifndef __FILTERING_TESTDATA_HPP
#define __FILTERING_TESTDATA_HPP

#include <iostream>
#include <vector>

#include <cmath>

#include <netcdf.h>
#include <Eigen/Dense>

#include <doctest.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

using namespace Eigen;
using namespace polynomialfiltering;

void assert_almost_equal(RealMatrix& A, RealMatrix& B);

void assert_almost_equal(RealMatrix& A, double B);

void assert_almost_equal(double B, RealMatrix& A);

void assert_almost_equal(double A, double B);

void assert_not_empty(std::vector< std::string >& list);


class TestData {
public:

	static std::shared_ptr <TestData> make(std::string filename) {
		return std::shared_ptr<TestData>(new TestData(filename));
	}


	TestData(std::string fileName) {
		std::string filePath = "C:\\Users\\NOOK\\GITHUB\\ReynekeMorrisonFiltering\\testdata\\";
		filePath += fileName;
		int retval, numgrps;
		retval = nc_open(filePath.c_str(), NC_NOWRITE, &ncid);
		std::cout << "TestData: " << filePath << " = " << retval << std::endl;
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

	void close() {} // meet python interface; closed in destructor

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
		return RealMatrix::Zero(0, 0);
	}

protected:
	int   ncid;  // root netCDF dataset id
	std::vector<std::string>  groupNames;
	std::vector<int>          groupIds;
};



#endif // __FILTERING_TESTDATA_HPP