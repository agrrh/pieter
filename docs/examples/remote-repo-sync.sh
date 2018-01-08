#!/bin/bash

# Parameters

PIETER_JOB_SSH_HOST=example.org
PIETER_JOB_SSH_PORT=22
PIETER_JOB_SSH_USER=myuser
PIETER_JOB_SSH_KEY=private/keys/id_rsa

PIETER_JOB_REPO_SOURCE=git@github.com:torvalds/linux.git
PIETER_JOB_REPO_PATH=/opt
PIETER_JOB_REPO_REMOTE=origin
PIETER_JOB_REPO_BRANCH=master
PIETER_JOB_REPO_NAME=''

# Actual work

ssh \
  -o BatchMode \
  -o ForwardAgent=yes \
  -o StrictHostKeyChecking=no \
  -o IdentityFile=${PIETER_JOB_SSH_KEY} \
  -o User=${PIETER_JOB_SSH_USER} \
  -o Port=${PIETER_JOB_SSH_PORT} \
  ${PIETER_JOB_SSH_HOST} << HERE
 mkdir -p ${PIETER_JOB_REPO_PATH}/${PIETER_JOB_REPO_NAME}
 cd ${PIETER_JOB_REPO_PATH}
 git clone ${PIETER_JOB_REPO_SOURCE} -b ${PIETER_JOB_REPO_BRANCH} ${PIETER_JOB_REPO_NAME}
 cd ${PIETER_JOB_REPO_NAME}
 git pull ${PIETER_JOB_REPO_REMOTE} ${PIETER_JOB_REPO_BRANCH}
HERE
