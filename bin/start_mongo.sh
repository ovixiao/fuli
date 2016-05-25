#!/usr/bin/env bash

MONGO_ROOT=/Users/xiao/mongodb
mkdir -p ${MONGO_ROOT}
#mkdir -p ${MONGO_ROOT}/database

mongod --dbpath=${MONGO_ROOT}/ --logpath=${MONGO_ROOT}/mongodb.log --logappend --fork --smallfiles
