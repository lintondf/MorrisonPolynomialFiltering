cmake_minimum_required(VERSION 3.10)
set(CMAKE_OSX_DEPLOYMENT_TARGET "10.9" CACHE STRING "Minimum OS X deployment version")
project(FilteringCpp) 
set(CMAKE_CXX_STANDARD 11)

find_package(GSL REQUIRED )
include_directories(.. include ${GSL_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS}) 


add_subdirectory( test )


set(SOURCES src/EigenTest.cpp) 
add_executable(EigenTest ${SOURCES})
target_link_libraries( EigenTest GSL::gsl  ${Boost_LIBRARIES}) # /Users/NOOK/GITHUB/MorrisonPolynomialFiltering/Cpp/GSL/lib/gsl/gsl.lib ) 
