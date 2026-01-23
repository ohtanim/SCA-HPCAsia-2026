cmake_minimum_required(VERSION 3.11)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_COMPILER mpicxx)

project("qiskit-cpp" LANGUAGES CXX C)

set(TARGET qiskit-cpp-test)

if ("${CMAKE_BUILD_TYPE}" STREQUAL "Debug")
  set(LIB_PATH debug)
else()
  set(LIB_PATH release)
endif()

set(QISKIT_CPP_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/)

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)
find_package(MPI REQUIRED)

include(FetchContent)

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.12.0/json.tar.xz DOWNLOAD_EXTRACT_TIMESTAMP true)
FetchContent_MakeAvailable(json)

if(NOT DEFINED QISKIT_ROOT)
    message(FATAL_ERROR "QISKIT_ROOT is not set. This variable is required for the project to build.")
endif()
if(NOT DEFINED QRMI_ROOT)
    message(FATAL_ERROR "QRMI_ROOT is not set. This variable is required for the project to build.")
endif()

function(add_application APP_NAME CPP_FILE)
  # source files for the client app
  set(SRC_FILE ${CMAKE_CURRENT_SOURCE_DIR}/${CPP_FILE})

  add_executable(${APP_NAME} ${SRC_FILE})
  set_target_properties(${APP_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/")

  message("   Qiskit Root = ${QISKIT_ROOT}")
  message("   QRMI Root = ${QRMI_ROOT}")
  # add libraries
  target_link_libraries(${APP_NAME}
    PRIVATE
          "-L${QISKIT_ROOT}/dist/c/lib -L${QRMI_ROOT}/target/release -Wl,-rpath ${QISKIT_ROOT}/dist/c/lib -Wl,-rpath ${QRMI_ROOT}/target/release" qiskit qrmi nlohmann_json::nlohmann_json
      )
  target_compile_options(${APP_NAME} PRIVATE "-DQRMI_ROOT=${QRMI_ROOT}")

  # path to headerfile
  target_include_directories(${APP_NAME}
    PRIVATE
      ${QISKIT_ROOT}/dist/c/include
      ${QRMI_ROOT}
      ${SAMPLES_PATH}
      ${CMAKE_CURRENT_SOURCE_DIR}/../src
      nlohmann_json::nlohmann_json
  )

  install (TARGETS ${APP_NAME} DESTINATION .)
endfunction()

function(add_application_test TEST_NAME APP_NAME CPP_FILE)
  add_application(${APP_NAME} ${CPP_FILE})
  add_test(NAME ${TEST_NAME} COMMAND ${APP_NAME})
endfunction()

if(QRMI_ROOT OR QISKIT_IBM_RUNTIME_C_ROOT)
  add_application(sampler_test sampler_test.cpp)
endif()
