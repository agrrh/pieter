#!/bin/bash

find ./jobs/* -type d 2>/dev/null | xargs -n1 rm -rf
