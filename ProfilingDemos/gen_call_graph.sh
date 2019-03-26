#!/bin/bash

if [ $# != 1 ]
 then
  echo "Please supply name of pstats file to graph"
  exit 1
fi

gprof2dot -f pstats $1 |dot -Tpng -o $1".png"

