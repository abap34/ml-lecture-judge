#!/bin/bash
cd backend
docker build -f Dockerfile.executor -t executor .
cd ..
docker-compose build redis celery-worker flower sqlite-web backend
docker-compose up redis celery-worker flower sqlite-web backend