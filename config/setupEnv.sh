#!/bin/bash

# ----------------
# Build environment variables for ADO PipeLines
# ----------------

# Oracle

export LD_LIBRARY_PATH=/home/vsts/work/1/s/test-\runner/dbclients/unix/instantclient_19_8
printenv 
chmod +rwx $LD_LIBRARY_PATH
for entry in "$LD_LIBRARY_PATH"/*
do
  echo "$entry"
  echo "changing permission"
  chmod +rwx "$entry"
done