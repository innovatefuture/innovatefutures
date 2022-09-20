#!/bin/bash

templates_dir=templates

compile_ts() {
  # echo "compiling from ${1} to ${2}" # compile from last dir in memory  since we are about to overwrite it
  tsc --strict --target es2017 --outDir $1/ts_output/js $(find $2 -type f -name '*.ts')
}

allfiles=$(find $templates_dir -type f -name '*.ts')

#declaring empty before loop and bool to catch repeating
last_dir=""
previous_match=0
for path in $allfiles; do
  dir_name=${path%/*} # keep before the last slash so we pass files from the same dir
  if [[ "$dir_name" == "$last_dir" ]]; then
    #echo "same dir"
    previous_match=1
  else
    if [[ "$last_dir" != "" ]]; then                           # to take out the first iteration
      if [[ $previous_match == 1 ]]; then                      # previous match match
        echo "current ${dir_name} and last ${last_dir}" # compile from current and the one from the previous iteration
        compile_ts $templates_dir $dir_name
        compile_ts $templates_dir $last_dir # compile from last dir in memory since we are about to overwrite it
        previous_match=0
      else
        echo "current ${dir_name}"
        compile_ts $templates_dir $dir_name # compile from last dir in memory since we are about to overwrite it
      fi
    fi
  fi
  last_dir=$dir_name
done

docker-compose exec app python3 manage.py collectstatic --noinput
