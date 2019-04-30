/***** /components/Fmp_test/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ TEST
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <netcdf.h>

#include <doctest.h>

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <TestData.hpp>
#include <polynomialfiltering/components/RecursivePolynomialFilter.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/ICore.hpp>
#include <polynomialfiltering/components/Emp.hpp>
#include <polynomialfiltering/components/Fmp.hpp>




#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        namespace Fmp_test {
            
            using namespace Eigen;
            
            void testName () {
                std::shared_ptr<polynomialfiltering::components::ICore> core90;
                std::shared_ptr<polynomialfiltering::components::ICore> core95;
                std::shared_ptr<polynomialfiltering::components::ICore> core95half;
                std::shared_ptr<polynomialfiltering::components::ICore> core95double;
                core90 = makeFmpCore(3, 1.0, 0.90);
                core95 = makeFmpCore(3, 1.0, 0.95);
                core95half = makeFmpCore(3, 2.0, 0.95);
                core95double = makeFmpCore(3, 0.5, 0.95);
                assert_almost_equal(core90->getVRF(1), core90->getVRF(10));
                assert_array_less(core95->getVRF(1), core90->getVRF(1));
                assert_almost_equal(ones(3 + 1, 3 + 1), arrayTimes((arrayDivide(core95double->getVRF(1), core95->getVRF(1))), (arrayDivide(core95half->getVRF(1), core95->getVRF(1)))));
                assert_almost_equal(core90->getGamma(10.0, 5.0), core90->getGamma(11.0, 5.0));
                assert_almost_equal(core90->getGamma(10.0, 5.0), core90->getGamma(10.0, 6.0));
                assert_almost_equal(core95->getGamma(10.0, 5.0), core95half->getGamma(10.0, 5.0));
                assert_almost_equal(core95->getGamma(10.0, 5.0), core95double->getGamma(10.0, 5.0));
            }

        }; // namespace Fmp_test
    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)

TEST_CASE("Fmp_test") {
    SUBCASE("testName") {
        components::Fmp_test::testName();
    }
}

