#!/usr/bin/env bash

print_title() {
	TIT='\033[1;33m'
	NCL='\033[0m'
	title=$1

	set -e

	echo -e
	echo -e "${TIT}${title}${NCL}"
	echo -e
}

# ** info: fetching changed files list
staged_files=($(git diff --name-only --cached))
changed_files_count=${#staged_files[@]}
cero_element=${staged_files[0]}

# ** info: printing changed files list
if ([ $changed_files_count != 0 ] && [ "$cero_element" != "" ]); then
	print_title "Changed Files Count On This Commit"
	printf 'files in stage area: %i' $changed_files_count
	echo -e
	print_title "Changed Files List On This Commit"
	for staged_file in "${staged_files[@]}"; do
		echo $staged_file
	done
else
	print_title "There Are Not Changed Files On This Commit"
fi

# ** info: executing tests
print_title "Executing Unit Tests"
pytest --quiet

# ** info: cleaning cache
print_title "Cleaning Cache"
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

# ** info: formatting files
print_title "Formatting Files"
black ./src
printf "\n"
black ./test/unit_test
printf "\n"
prettier ./test/load_test/k6/**/*.js --write
printf "\n"
prettier "./**/*.{yaml,json,md,graphql,sh,env}|Dockerfile" --write

# ** info: exporting dependencies if needed
if [[ " ${staged_files[@]} " =~ " poetry.lock " ]]; then
	print_title "Exporting Dependencies"
	poetry export --without-hashes --only dev --format=requirements.txt > ./req/dev.txt
	poetry export --without-hashes --format=requirements.txt > ./req/app.txt
	git add ./req/app.txt
	git add ./req/dev.txt
fi

# ** info: updating staged files
if ([ $changed_files_count != 0 ] && [ "$cero_element" != "" ]); then
	for staged_file in "${staged_files[@]}"; do
		if test -f "$staged_file"; then
			git add $staged_file
		fi
	done
fi

# ** info: linting files
print_title "Linting Files"
flake8 ./test/unit_test --verbose
printf "\n"
flake8 ./src --verbose

# ** info: validating typos
print_title "Validating Typos"
mypy --explicit-package-bases ./test/unit_test
printf "\n"
mypy --explicit-package-bases ./src

# ** info: linting files
print_title "Commit Sucessfully"

# ** info: cleaning cache
print_title "Cleaning Cache"
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
