#!/usr/bin/env bash

MONGO_ROOT=/User/xiao
mkdir -p ${MONGO_ROOT}
mkdir -p ${MONGO_ROOT}/database

mongod --dbpath=${MONGO_ROOT}/database/ --logpath=${MONGO_ROOT}/mongodb.log --logappend --fork
