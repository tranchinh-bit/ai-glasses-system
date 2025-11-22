cmake_minimum_required(VERSION 3.10)

project(vision_object_danger)

add_library(vision_object_danger STATIC
    detector.cpp
    tracker.cpp
    danger_analyzer.cpp
)

target_include_directories(vision_object_danger PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
