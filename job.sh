#!/bin/bash

TIMER=$(date +%s)

JOB_NAME=$1
SCENARIO_PATH=$2

CWD=$(pwd)
TMP_DIR=$(mktemp -d)

cd ${TMP_DIR}

timeout --preserve-status 600 ${CWD}/${SCENARIO_PATH}
RC=$?

DURATION=$[$(date +%s)-${TIMER}]

echo "${DURATION};${RC}" > ${CWD}/logs/${JOB_NAME}.result

rm -rf ${TMP_DIR}
