#!/bin/bash

# set echo color
red='\e[91m'
green='\e[92m'
yellow='\e[93m'
cyan='\e[96m'
none='\e[0m'

function usage {
    print "${cyan}"
	print "Usage: $(basename $0) [OPTIONS]"
	print "\t-h | --help, Show help"
    print "\t--clean, Clean up"
	print "\t-t TargetName| --target TargetName, build target"
	print "${none}"
}

function print {
	echo -e "$@"
}

function log_info {
	echo -e "${green}$@${none}"
}

function log_warn {
	echo -e "${yellow}$@${none}"
}

function log_error {
	echo -e "${red}$@${none}"
}


function get_opts {

	while getopts "dht:-:" option; do
		case "${option}" in
			-)
				case "${OPTARG}" in
					help)
						print "--help, I'm help"
						;;
					clean)
						print "--clean, I'm clean"
						log_info "clean up success!"
						;;
					target)
						val="${!OPTIND}"; OPTIND=$(( $OPTIND + 1 ))
						print "--target=$val, I'm target"
						;;
					loglevel=*)
						val=${OPTARG#*=}
						opt=${OPTARG%=$val}
						echo "Parsing option: '--${opt}', value: '${val}'" >&2
						;;
					*)
						if [ "$OPTERR" = 1 ] && [ "${optspec:0:1}" != ":" ]; then
							echo "Unknown option --${OPTARG}" >&2
						fi
						;;
				esac;;
			t)
				log_info "-t $OPTARG"
				;;
			h)
				usage
				;;
			*)
				if [ "$OPTERR" != 1 ] || [ "${optspec:0:1}" = ":" ]; then
					echo "Non-option argument: '-${OPTARG}'" >&2
				fi
				;;
		esac
	done

	echo "OPTIND: $OPTIND"

	if [ "$OPTIND" = "1" ]; then
		log_error "Parameters are necessary"
		exit -1
	fi
}

get_opts $@
