#!/bin/sh

# ** info: getting the path of the current script
scripts_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# ** info: setting the target host
export K6_TARGET_HOST=http://localhost:10048

# ** info: running the load tests
k6 run $scripts_path/rest/user/search-by-email.js

# ** info: unsetting the target host
unset K6_TARGET_HOST
