INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_ISEE3 isee3)

FIND_PATH(
    ISEE3_INCLUDE_DIRS
    NAMES isee3/api.h
    HINTS $ENV{ISEE3_DIR}/include
        ${PC_ISEE3_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    ISEE3_LIBRARIES
    NAMES gnuradio-isee3
    HINTS $ENV{ISEE3_DIR}/lib
        ${PC_ISEE3_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ISEE3 DEFAULT_MSG ISEE3_LIBRARIES ISEE3_INCLUDE_DIRS)
MARK_AS_ADVANCED(ISEE3_LIBRARIES ISEE3_INCLUDE_DIRS)

