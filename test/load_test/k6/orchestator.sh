#!/bin/sh

print_title() {
	TIT='\033[1;33m'
	NCL='\033[0m'
	title=$1

	set -e

	echo -e
	echo -e "${TIT}${title}${NCL}"
	echo -e
}

print_space() {
	set -e

	echo -e
	echo -e
	echo -e
}

# ** info: getting the path of the current script
scripts_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# ** info: setting the target host
export K6_TARGET_HOST=http://localhost:10048

# ** info: running the load tests
print_title "Executing Load Tests"
k6 run $scripts_path/rest/collect-request/create.js
print_space
k6 run $scripts_path/rest/user/search-by-email.js
print_space

# ** info: unsetting the target host
unset K6_TARGET_HOST
