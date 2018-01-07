#!/bin/bash

JOB_NAME=$1
SCENARIO_PATH=$2
STATE_PATH=$3

CWD=$(pwd)
TMP_DIR=$(mktemp -d)

cd ${TMP_DIR}

# Start actually

touch ${CWD}/${STATE_PATH}

timeout --preserve-status 600 ${CWD}/${SCENARIO_PATH}
RC=$?

echo "${RC};$(date +%s)" > ${CWD}/${STATE_PATH}

rm -rf ${TMP_DIR}
