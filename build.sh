#!/bin/bash
docker-compose build
cd backend
docker build -f Dockerfile.executor -t executor_image .
cd ..

