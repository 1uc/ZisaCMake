cmake_minimum_required(VERSION 3.18)
project(Example)

option(BUILD_TESTS OFF "Should tests be built?")

add_library(utils SHARED)

add_executable(foo ${CMAKE_CURRENT_SOURCE_DIR}/src/foo_main.cpp)
target_link_libraries(foo PUBLIC utils)

add_subdirectory(src)

if(BUILD_TESTS)
  add_executable(unit_tests)
  target_link_libraries(unit_tests PUBLIC utils)
endif()

add_subdirectory(tests)
