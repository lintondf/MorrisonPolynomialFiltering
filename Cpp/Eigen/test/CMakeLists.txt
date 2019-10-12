
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
#FIND_PACKAGE(Boost REQUIRED COMPONENTS system math math_c99 serialization)
#message("BOOST " Boost::math ${BOOST_INCLUDE_DIRS} ${BOOST_LIBRARIES})

set(SQLITECPP_INCLUDE ../../SQLiteCpp/include)
set(SQLITECPP_BUILD ${CMAKE_CURRENT_SOURCE_DIR}/../../SQLiteCpp/build/)
set(SQLITECPP_LIBRARY ${SQLITECPP_BUILD}libSQLiteCpp.a ${SQLITECPP_BUILD}sqlite3/libsqlite3.a)
#set(SQLITECPP_LIBRARY SQLiteCpp)

include_directories(.. include ${SQLITECPP_INCLUDE} ${GSL_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

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
# Link SQLiteCpp_example1 with SQLiteCpp and sqlite3 (and also pthread and dl for linux)
#if(UNIX AND NOT APPLE)
#   # Linux
#   set(SQLITECPP_LIBRARIES sqlite3 pthread dl)
#else(UNIX AND APPLE)
   # Mac OS
   set(SQLITECPP_LIBRARIES ${SQLITECPP_LIBRARY} pthread)
#else()
#   # Windows
#   set(SQLITECPP_LIBRARIES sqlite3)
#endif()
target_link_libraries( FilteringEigenTest ${SQLITECPP_LIBRARIES} ${NETCDF_LIBRARIES_C}  ${BOOST_LIBRARIES}) # boost_math_tr1 boost_math_c99) 
