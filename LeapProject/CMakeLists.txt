cmake_minimum_required(VERSION 3.16)
project(LeapProject)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)

# Include Leap SDK headers
include_directories(${CMAKE_SOURCE_DIR}/include)

# Add the source files
add_executable(LeapProject src/main.cpp)

# Link LeapC library
target_link_libraries(LeapProject ${CMAKE_SOURCE_DIR}/lib/LeapC.lib)
