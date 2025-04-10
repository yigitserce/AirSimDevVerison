cmake_minimum_required(VERSION 3.5.0)
project(CppLib)

set(CMAKE_CXX_STANDARD 11)

find_package(PkgConfig REQUIRED)
pkg_check_modules(GSTREAMER REQUIRED gstreamer-1.0 gstreamer-app-1.0)

LIST(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../cmake-modules") 
INCLUDE("${CMAKE_CURRENT_LIST_DIR}/../cmake-modules/CommonSetup.cmake")

CommonSetup()

IncludeEigen()

SetupConsoleBuild()

find_package(OpenCV 4.10 REQUIRED)

include_directories(
    ${AIRSIM_ROOT}/CppLib
    ${OpenCV_INCLUDE_DIRS}
    ${RPC_LIB_INCLUDES}
    ${GSTREAMER_INCLUDE_DIRS}
    ${AIRSIM_ROOT}/AirLib/include
    ${AIRSIM_ROOT}/MavLinkCom/include
    ${AIRSIM_ROOT}/MavLinkCom/common_utils
)

AddExecutableSource()

CommonTargetLink()
target_link_libraries(${PROJECT_NAME} AirLib)
target_link_libraries(${PROJECT_NAME} ${RPC_LIB})
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
target_link_libraries(${PROJECT_NAME} ${GSTREAMER_LIBRARIES})
