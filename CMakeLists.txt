cmake_minimum_required(VERSION 4.0)
project(LuaBridge C)

set(CMAKE_C_STANDARD 11)

# Find Python development components
find_package(Python COMPONENTS Development REQUIRED)

# Create Python extension module (MODULE for .pyd/.so)
add_library(LuaBridge MODULE
        src/LuaBridge/main.c
)

# Include Python headers
target_include_directories(LuaBridge PRIVATE ${Python_INCLUDE_DIRS})

# Link against Python library
target_link_libraries(LuaBridge PRIVATE ${Python_LIBRARIES})

# On Windows, avoid adding "lib" prefix to .pyd
if(WIN32)
    set_target_properties(LuaBridge PROPERTIES PREFIX "")
endif()

message(STATUS "Python include dir: ${Python_INCLUDE_DIRS}")
