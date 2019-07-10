cmake_minimum_required(VERSION 3.13.1)

include(CMakeParseArguments)

include(test_cmake.cmake)



set(CMAKE_C_COMPILER "/home/mx/work/ose_fw_lastest/ose-dev-code-base/modules/ose_val_baremetal/BullseyeCoverage/bin/arm-zephyr-eabi-gcc")
set(TOOLCHAIN_C_FLAGS "-mthumb;-mcpu=cortex-m7;-mfpu=fpv5-sp-d16;-mfloat-abi=hard")

execute_process(
	COMMAND ${CMAKE_C_COMPILER} ${TOOLCHAIN_C_FLAGS} --print-libgcc-file-name
	OUTPUT_VARIABLE LIBGCC_FILE_NAME
	OUTPUT_STRIP_TRAILING_WHITESPACE
)

# function(tst_arguments)

# 	CMAKE_PARSE_ARGUMENTS(TEST "" "NAME;COMMAND;BASELINE" "ARGSLIST" ${ARGN})

# 	message("TEST_DEFAULT_ARGS is ${TEST_DEFAULT_ARGS} from ${ARGN}")
# 	message("TEST_NAME is ${TEST_NAME}")
# 	message("TEST_COMMAND is ${TEST_COMMAND}")
# 	message("TEST_ARGSLIST is ${TEST_ARGSLIST}")
# 	message("TEST_BASELINE is ${TEST_BASELINE}")

# endfunction()

# tst_arguments()

# TEST_ARGUMENT(
# 	NAME
# 		testiso
# 	COMMAND
# 		"RunMe"
# 	ARGSLIST
# 		${SRC}
# 	BASELINE
# 		"$ENV{HOME}"
# )


# function(check_module result name)
# 	set(options)
# 	set(oneValueArgs PATH EXPECTED_ARCH EXPECTED_VERSION VERSION_COMPARE)
# 	set(multiValueArgs)
# 	cmake_parse_arguments(check_module
# 							"${options}"
# 							"${oneValueArgs}"
# 							"${multiValueArgs}"
# 							${ARGN})

# 	set(res "false")
# 	set(module_path ${check_module_PATH})
# 	message(STATUS "check_module_PATH: '${check_module_PATH}'")

# endfunction()

# check_module()


function(test_source_add src_list)

	message("ARGC: ${ARGC}")
	message("ARGC: ${ARGV}")
	
	file(GLOB_RECURSE FILES ${ARGV})
	message("FILES = ${FILES}")

endfunction()


function(test_source_add_if condition src_list)

	message("ARGC: ${ARGC}")
	message("ARGC: ${ARGV}")

	list(SUBLIST ARGV 1 -1 FILES)
	message("FILES = ${FILES}")

	if(${${condition}})
		test_source_add(${FILES})
	endif()

endfunction()


set(CONFIG_TEST ON)

test_source_add(build.sh)

test_source_add_if(CONFIG_TEST build.sh CMakeLists.txt)

