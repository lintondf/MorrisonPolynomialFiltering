
cmake_minimum_required(VERSION 3.10)
set(CMAKE_OSX_DEPLOYMENT_TARGET "10.9" CACHE STRING "Minimum OS X deployment version")
project(FilteringTests)    
set(CMAKE_CXX_STANDARD 11)

find_path (NETCDF_INCLUDES_C netcdf.h HINTS NETCDF_DIR NETCDF_DIR)
message(" inc =  ${NETCDF_INCLUDES_C}  ")
find_library (NETCDF_LIBRARIES_C  NAMES netcdf)
message(" lib =  ${NETCDF_LIBRARIES_C}  ") 

#set(Boost_USE_STATIC_LIBS OFF)
#set(Boost_USE_MULTITHREADED ON)
#set(Boost_USE_STATIC_RUNTIME OFF)
#set(Boost_MATH_NO_LIB ON)
#FIND_PACKAGE(Boost REQUIRED COMPONENTS system math math_c99)
#message("BOOST " Boost::math ${BOOST_INCLUDE_DIRS} ${BOOST_LIBRARIES})
include_directories(.. include ${GSL_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

#set(CPPTEST_INCLUDES ../../cpptest )
#set(CPPTEST_LIBRARY ${CMAKE_CURRENT_SOURCE_DIR}/../../cpptest/cpptest.lib ) 

include_directories(eigen 
       ../..
       ${NETCDF_INCLUDES_C}  ${GSL_INCLUDE_DIRS} ${BOOST_INCLUDE_DIRS} )
#	   ${CPPTEST_INCLUDES} )
#  link_directories(${NETCDF_LIBRARIES_C})

enable_testing()

FILE(GLOB_RECURSE MAIN_SRC ../src/polynomialfiltering/*.cpp)
# FILE(GLOB_RECURSE COMPONENTS_SRC ../src/polynomialfiltering/components/*.cpp  ../src/polynomialfiltering/components/filters/*.cpp)

FILE(GLOB_RECURSE TEST_SRC ../test/*_test.cpp)

if(MSVC)
  set(CMAKE_EXE_LINKER_FLAGS
      "${CMAKE_EXE_LINKER_FLAGS}  /NODEFAULTLIB:LIBCMT")
endif()

set(SOURCES  ${MAIN_SRC}
	${TEST_SRC}
	testMain.cpp)
add_executable(FilteringEigenTest ${SOURCES})
target_link_libraries( FilteringEigenTest ${NETCDF_LIBRARIES_C}  ${BOOST_LIBRARIES} boost_math_tr1 boost_math_c99) 
