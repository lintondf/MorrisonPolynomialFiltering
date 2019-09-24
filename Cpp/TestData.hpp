#pragma once
#ifndef __FILTERING_TESTDATA_HPP
#define __FILTERING_TESTDATA_HPP

#include <iostream>
#include <stdlib.h>
#include <vector>
#include <unistd.h>
#include <string>

#include <cmath>

#include <netcdf.h>
#include <Eigen/Dense>

#include <doctest.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

using namespace Eigen;
using namespace polynomialfiltering;


void assert_almost_equal(const RealMatrix A, const RealMatrix B);

void assert_almost_equal(const RealMatrix A, double B);

void assert_almost_equal(double B, const RealMatrix A);

void assert_almost_equal(double A, double B);

void assert_array_less(const RealMatrix A, const RealMatrix B);

void assert_array_less(double A, double B);

void assert_not_empty(std::vector< std::string >& list);

void assert_clear();

double assert_report( const std::string id );

void assertEqual(double limitBits, double actualBits);

void assertGreaterEqual(double limitBits, double actualBits);

void assertTrue( bool tf );

void assertFalse( bool tf );

typedef int Group;

class TestData {
public:

	static std::shared_ptr <TestData> make(std::string filename) {
		return std::shared_ptr<TestData>(new TestData(filename));
	}
    
    static std::string testDataPath();


    TestData(std::string fileName);

	void close() {} // meet python interface; closed in destructor

    ~TestData();
    
    const std::vector<std::string> getGroupNames();

    std::vector<std::string> getMatchingGroups(std::string testName);
    
    Group getGroup( const std::string groupName );

    RealMatrix getGroupVariable(std::string groupName, std::string variableName);
    
    RealMatrix getArray( Group gid, std::string variableName );
    
    double getScalar( Group gid, std::string variableName );
    
    int getInteger( Group gid, std::string variableName );
    
    
protected:
	int   ncid;  // root netCDF dataset id
	std::vector<std::string>  groupNames;
	std::vector<int>          groupIds;
};



#endif // __FILTERING_TESTDATA_HPP
