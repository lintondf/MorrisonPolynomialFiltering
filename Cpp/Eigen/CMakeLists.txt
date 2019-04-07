cmake_minimum_required(VERSION 3.10)

project(FilteringCpp) 
set(CMAKE_CXX_STANDARD 11)

find_package(GSL REQUIRED )
include_directories(include ${GSL_INCLUDE_DIRS}) 

add_subdirectory( test )


#include_directories(src) 
#set(SOURCES src/polynomialfiltering/Main.cpp src/polynomialfiltering/components/FixedMemoryPolynomialFilter.cpp)
#set(SOURCES src/polynomialfiltering/Main.cpp 
#	src/polynomialfiltering/components/FixedMemoryPolynomialFilter.cpp
set(SOURCES  src/polynomialfiltering/Main.cpp 
    src/polynomialfiltering/components/FixedMemoryPolynomialFilter.cpp
	src/EigenTest.cpp) 
#add_executable(PolynomialFilteringCpp ${SOURCES})
add_executable(EigenTest ${SOURCES})
target_link_libraries( EigenTest GSL::gsl ) # /Users/NOOK/GITHUB/MorrisonPolynomialFiltering/Cpp/GSL/lib/gsl/gsl.lib ) 