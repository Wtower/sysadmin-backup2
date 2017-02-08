#!/usr/bin/env bash
coverage run --branch --source='.' test.py
coverage report -m | tee coverage.log
coverage html
