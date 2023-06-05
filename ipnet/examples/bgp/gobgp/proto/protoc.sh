#!/bin/bash


python3 -m grpc_tools.protoc -I./gobgp/api/ --python_out=. --grpc_python_out=. attribute.proto gobgp.proto capability.proto
