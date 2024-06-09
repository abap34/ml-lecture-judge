#!/bin/bash
cd backend
docker build -f Dockerfile.executor -t executor .
cd ..
docker-compose build

