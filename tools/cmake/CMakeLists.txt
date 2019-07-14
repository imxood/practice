cmake_minimum_required(VERSION 3.13.1)

include(CMakeParseArguments)

include(test_cmake.cmake)


##############

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


##############

function(test_source_add)

	message(STATUS "ARGC: ${ARGC}")
	message(STATUS "ARGN: ${ARGN}")
	message(STATUS "ARGV: ${ARGV}")

	file(GLOB_RECURSE FILES ${ARGN})
	message(STATUS "FILES = ${FILES}")

endfunction()

function(test_source_add_if condition)

	message(STATUS "ARGC: ${ARGC}")
	message(STATUS "ARGV: ${ARGV}")
	message(STATUS "ARGN: ${ARGN}")

	if(${${condition}})
		test_source_add(${ARGN})
	endif()

endfunction()

set(CONFIG_TEST ON)

test_source_add(tool.py)

test_source_add_if(CONFIG_TEST tool.py CMakeLists.txt)



##############

find_program(DTC dtc)

message(STATUS "DTC: ${DTC}")

if(${DTC} STREQUAL DTC-NOTFOUND)
	message(FATAL_ERROR "Unable to find dtc")
endif()

set(MIN_DTC_VERSION 1.4.6)
execute_process(
	COMMAND
	${DTC} --version
	OUTPUT_VARIABLE dtc_version_output
)

message(STATUS "dtc_version_output: ${dtc_version_output}")

string(REGEX MATCH "Version: DTC ([0-9]+\.[0-9]+.[0-9]+).*" out_var ${dtc_version_output})

if(${CMAKE_MATCH_1} VERSION_LESS ${MIN_DTC_VERSION})
	assert(0 "The detected dtc version is unsupported.                                 \n\
		The version was found to be ${CMAKE_MATCH_1}                                   \n\
		But the minimum supported version is ${MIN_DTC_VERSION}                        \n\
		See https://docs.zephyrproject.org/latest/getting_started/                     \n\
		for how to use the SDK's dtc alongside a custom toolchain."
	)
endif()



##############

macro(macro_test hello world)
	# 所有的参数
	MESSAGE(STATUS ARGV=${ARGV})
	# 非显式声明的所有参数
	MESSAGE(STATUS ARGN=${ARGN})

	MESSAGE(STATUS ARGV0=${ARGV0})
	MESSAGE(STATUS ARGV1=${ARGV1})
	MESSAGE(STATUS ARGV2=${ARGV2})
	MESSAGE(STATUS ARGV3=${ARGV3})
endmacro()

# 调用宏时传入4个参数
macro_test(TOM JERRY SUSAN BERN)




# add_custom_target 添加定制目标, 给目标添加属性, 显示属性, 执行目标

add_custom_target(test_target)

set_property(
	TARGET test_target
    APPEND PROPERTY COMPILE_DEFINITIONS
	"abc:${CMAKE_CURRENT_SOURCE_DIR}/testfile"
)

file(GENERATE
    OUTPUT "includes.txt"
    CONTENT "$<TARGET_PROPERTY:test_target,COMPILE_DEFINITIONS>\n"
)

function(print_property_attributes type name propName)
	if ("${type}" STREQUAL "CACHE")
		set(propTypeArgs)
		list(APPEND propTypeArgs CACHE)
		list(APPEND propTypeArgs "${name}")
			# list used because "set(propTypeArgs CACHE "${name}")" is an error...
		if ("${propName}" STREQUAL "")
			set(propName VALUE)
		endif()
	elseif ("${type}" STREQUAL "VARIABLE")
		set(propTypeArgs VARIABLE)
		set(propName "${name}") # force propName to variable name for VARIABLE
	else()
		message("type '${type}' not implemented yet...")
		return()
	endif()

	message("propName='${propName}'") # the name of the property

	get_property(propIsSet ${propTypeArgs} PROPERTY "${propName}" SET)
	message("propIsSet='${propIsSet}'")

	if (propIsSet)
		get_property(propValue ${propTypeArgs} PROPERTY "${propName}")
		message("propValue='${propValue}'")

		get_property(propIsDefined ${propTypeArgs} PROPERTY "${propName}" DEFINED)
		message("propIsDefined='${propIsDefined}'")

		get_property(propBriefDocs ${propTypeArgs} PROPERTY "${propName}" BRIEF_DOCS)
		message("propBriefDocs='${propBriefDocs}'")

		get_property(propFullDocs ${propTypeArgs} PROPERTY "${propName}" FULL_DOCS)
		message("propFullDocs='${propFullDocs}'")

		if ("${type}" STREQUAL "CACHE")
			if ("${propName}" STREQUAL "VALUE")
				print_property_attributes(CACHE "${name}" ADVANCED)
				print_property_attributes(CACHE "${name}" HELPSTRING)
				print_property_attributes(CACHE "${name}" MODIFIED)
				print_property_attributes(CACHE "${name}" STRINGS)
				print_property_attributes(CACHE "${name}" TYPE)
			endif()
		endif()
	endif()
endfunction()


function(print_variable_property_values varname)
	set(name "${varname}")
	set(value "${${varname}}")

	message("name='${name}'")
	message("value='${value}'")
	# SET, 是否是被set_property; DEFINE, 是否是被define_property
	get_property(varPropIsSet VARIABLE PROPERTY "${name}" SET)

	if (varPropIsSet)
		message("type='VARIABLE'")
		print_property_attributes(VARIABLE "${name}" "")
	else()
		message("variable '${name}' is not set")
	endif()

	get_property(cachePropIsSet CACHE "${name}" PROPERTY VALUE SET)

	if (cachePropIsSet)
		message("type='CACHE'")
		print_property_attributes(CACHE "${name}" "")
	else()
		message("cache entry '${name}' is not set")
	endif()

endfunction()


message("cmake version ${CMAKE_VERSION}")

set(plain_variable "plain variable value")
set(cache_entry "cache entry value" CACHE STRING "cache doc string")

print_variable_property_values(plain_variable)
print_variable_property_values(cache_entry)






# 定制运行目标(就像make中的目标一样)
# add_custom_target, 每次都会运行命令
# add_custom_command, 有两种形式,
# 	1. OUTPUT, 产生文件
# 	2. TARGET, 目标定制(就是hook功能, 执行前,执行后等触发)
# 它会根据目标是否有变化,才考虑是否运行命令, 如果没有依赖它的命令它就不会执行
#
# make Test1.txt, 执行命令生成Test1.txt, 第二次执行不会执行, "ninja: no work to do."
# make Test2
set(TEST_FILE "Test1.txt")
add_custom_command(OUTPUT ${TEST_FILE}
	COMMAND echo "Generating Test1.txt file..."
	COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_LIST_FILE} ${TEST_FILE}
	COMMENT  "This is a Test1"
)

# Test2每一次都会运行
add_custom_target(Test2
	ALL DEPENDS ${TEST_FILE}
	COMMAND echo "Run Test2..."
	COMMENT  "This is a Test2"
)

# 这个command会在Test2执行前执行,,,,, PRE_BUILD只对VS有效!
add_custom_command(TARGET Test2
	PRE_BUILD
	COMMAND echo "executing a fake command"
	COMMENT "This command will be executed before building target Test2"
)

add_custom_target(Test3
	COMMAND echo "hello, I am Test3"
	COMMENT "This is Test3"
)

add_custom_command(OUTPUT Test4.txt
	COMMAND touch Test4.txt
	COMMENT "This is Test4"
)
