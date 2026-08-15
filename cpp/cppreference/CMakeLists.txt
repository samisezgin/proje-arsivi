cmake_minimum_required(VERSION 3.0.0)
project(study VERSION 0.1.0)


add_executable(study main.cpp)
target_include_directories(study PUBLIC "./")
set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
#set(CMAKE_CXX_STANDARD 17)
include(CPack)
