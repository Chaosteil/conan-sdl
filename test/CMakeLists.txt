project(sdl_test)
cmake_minimum_required(VERSION 2.8)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_executable(test test.c)
include_directories(${CONAN_INCLUDE_DIRS})
target_link_libraries(test ${CONAN_LIBS})
