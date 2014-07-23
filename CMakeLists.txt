project(py-mixnv)

## Setup
cmake_minimum_required(VERSION 2.8)
set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}"
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

include(PythonMacros)
include(CMakeCMacros)

cmake_c_add_flags(CMAKE_C_FLAGS -Wall -Wextra -std=gnu99)
# -std=c++0x is deprecated but gcc < 4.7 do not recognise c++11 ....
cmake_c_add_flags(CMAKE_CXX_FLAGS -Wall -Wextra
  -Wno-deprecated-register -std=c++0x)
cmake_c_add_flags(CMAKE_SHARED_LINKER_FLAGS -Wl,--as-needed -Wl,--no-undefined)
cmake_c_add_flags(CMAKE_MODULE_LINKER_FLAGS -Wl,--as-needed -Wl,--no-undefined)

add_subdirectory(mixnv)
