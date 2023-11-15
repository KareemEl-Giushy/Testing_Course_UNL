#!/bin/bash
if grep "redo" $1; then
    echo "0"                 # Success.
    exit 0;
fi
echo "1"                     # Failure.
exit 1;
