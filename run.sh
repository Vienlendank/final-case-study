#!/usr/bin/env bash
set -e
docker build -t qwen25-chat .
docker run --rm -p 8080:8080 qwen25-chat
