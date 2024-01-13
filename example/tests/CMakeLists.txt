if(BUILD_TESTS)
target_sources(unit_tests
  PRIVATE ${CMAKE_CURRENT_LIST_DIR}/test_foo.cpp
  PRIVATE ${CMAKE_CURRENT_LIST_DIR}/tests_main.cpp
)

endif()

