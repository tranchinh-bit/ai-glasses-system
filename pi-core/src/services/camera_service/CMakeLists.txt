cmake_minimum_required(VERSION 3.10)

project(camera_service)

add_executable(camera_service main.cpp)

# Link libcamera nếu cần, tuỳ môi trường:
# find_package(PkgConfig REQUIRED)
# pkg_check_modules(LIBCAMERA REQUIRED libcamera)
# target_include_directories(camera_service PRIVATE ${LIBCAMERA_INCLUDE_DIRS})
# target_link_libraries(camera_service PRIVATE ${LIBCAMERA_LIBRARIES})
