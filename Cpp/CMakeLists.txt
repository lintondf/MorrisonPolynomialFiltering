cmake_minimum_required(VERSION 3.12)

project(FilteringCpp) 

include_directories(boost_1_69_0)
include_directories(include)
#include_directories(src)
set(SOURCES src/polynomialfiltering/Main.cpp)
#"C:\Users\NOOK\GITHUB\ReynekeMorrisonFiltering\Cpp\src\PolynomialFiltering\Main.cpp"
#'C:/Users/NOOK/GITHUB/ReynekeMorrisonFiltering/Cpp/src/PolynomialFiltering/Main.cpp', needed by 'CMakeFiles/MainCpp.dir/src/PolynomialFiltering/Main.cpp.obj', missing and no known rule to make it	C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE\CMakeLists.txt	C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE\ninja	1	

link_directories(../boost_1_69_0/stage/lib)
add_executable(MainCpp ${SOURCES})
