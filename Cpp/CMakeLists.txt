project(FilteringCpp) 

include_directories(boost_1_69_0)
include_directories(src)
link_directories(../boost_1_69_0/stage/lib)
add_executable(FilteringCpp src/Filtering.cpp)
