#!/bin/sh

# ** info: setting the target host
export K6_TARGET_HOST=http://localhost:10048

# ** info: running the load tests
k6 run test/load_test/k6_scripts/rest/user/search-by-email.js

# ** info: unsetting the target host
unset K6_TARGET_HOST
