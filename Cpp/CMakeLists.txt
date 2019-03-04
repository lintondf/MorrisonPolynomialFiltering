cmake_minimum_required(VERSION 3.12)

project(FilteringCpp) 

include_directories(boost_1_69_0)
include_directories(include)
#include_directories(src)
set(SOURCES src/polynomialfiltering/Main.cpp src/polynomialfiltering/components/FixedMemoryPolynomialFilter.cpp)

link_directories(../boost_1_69_0/stage/lib)
add_executable(PolynomialFilteringCpp ${SOURCES})
