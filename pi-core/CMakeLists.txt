cmake_minimum_required(VERSION 3.10)
project(ai_glasses_pi_core)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(src/services/camera_service)
add_subdirectory(src/services/vision_object_danger)
