
cmake_minimum_required(VERSION 3.10)

project(FilteringTests)    
set(CMAKE_CXX_STANDARD 11)

find_path (NETCDF_INCLUDES_C netcdf.h HINTS NETCDF_DIR NETCDF_DIR)
message(" inc =  ${NETCDF_INCLUDES_C}  ")
find_library (NETCDF_LIBRARIES_C  NAMES netcdf)
message(" lib =  ${NETCDF_LIBRARIES_C}  ") 

#set(CPPTEST_INCLUDES ../../cpptest )
#set(CPPTEST_LIBRARY ${CMAKE_CURRENT_SOURCE_DIR}/../../cpptest/cpptest.lib ) 

include_directories(eigen 
       ../..
       ${NETCDF_INCLUDES_C} )
#	   ${CPPTEST_INCLUDES} )
#  link_directories(${NETCDF_LIBRARIES_C})

enable_testing()

FILE(GLOB MAIN_SRC ../src/polynomialfiltering/*.cpp)
FILE(GLOB COMPONENTS_SRC ../src/polynomialfiltering/components/*.cpp)

FILE(GLOB TEST_SRC ../test/*_test.cpp)


set(SOURCES  ${MAIN_SRC}
	${COMPONENTS_SRC}
	${TEST_SRC}
	testMain.cpp)
add_executable(FilteringEigenTest ${SOURCES})
target_link_libraries( FilteringEigenTest ${NETCDF_LIBRARIES_C} ) 
