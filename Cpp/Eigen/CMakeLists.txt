cmake_minimum_required(VERSION 3.10)

project(FilteringCpp) 
set(CMAKE_CXX_STANDARD 11)

include_directories(include) 

add_subdirectory( test )

#include_directories(boost_1_69_0)
#link_directories(../boost_1_69_0/stage/lib)  

# include_directories(eigen) 

#include_directories(src) 
#set(SOURCES src/polynomialfiltering/Main.cpp src/polynomialfiltering/components/FixedMemoryPolynomialFilter.cpp)
#set(SOURCES src/polynomialfiltering/Main.cpp 
#	src/polynomialfiltering/components/FixedMemoryPolynomialFilter.cpp
set(SOURCES  src/polynomialfiltering/Main.cpp 
    src/polynomialfiltering/components/FixedMemoryPolynomialFilter.cpp
	src/EigenTest.cpp) 
#add_executable(PolynomialFilteringCpp ${SOURCES})
add_executable(EigenTest ${SOURCES})
