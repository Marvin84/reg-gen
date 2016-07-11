#!/bin/bash

if [[ $# < 2 ]]; then
  echo "This script downloads files specified in an experimental matrix to a given directory and updates the matrix with the local paths."
  echo "A backup of the original matrix is created."
  echo ""
  echo "USAGE: $0 [EM.txt] [TARGET PATH]"
  exit 0
fi

TARGETPATH=`echo $2 | sed 's/\\//\\\\\\//g'`

grep -E "http:|https:|ftp:" $1 | sed "s/^.*\(\(https\?\|ftp\):\/\/[^ \t]*\/\([^\/ \t]*\)\).*$/wget \1 -nc --output-document=$TARGETPATH\3/" | bash
grep -E "(http:|https:|ftp:).*\.gz" $1 | sed "s/^.*\(\(https\?\|ftp\):\/\/[^ \t]*\/\([^\/ \t]*\)\).*$/gunzip $TARGETPATH\3/" | bash

cp $1 $1.bck
sed -i "s/\(\(https\?\|ftp\):\/\/[^ \t]*\/\([^\/ \t]*\)\)\.gz/$TARGETPATH\3/" $1
sed -i "s/\(\(https\?\|ftp\):\/\/[^ \t]*\/\([^\/ \t]*\)\)/$TARGETPATH\3/" $1