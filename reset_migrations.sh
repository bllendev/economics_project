#!/bin/bash

# Assume the current directory is the Django project root
BASE_DIR=$(pwd)

# Use find to locate .py files in 'migrations' directories excluding '__init__.py'
find "$BASE_DIR" -path "*/migrations/*.py" -not -name "__init__.py" -type f -exec rm {} +

echo "Migration files have been removed, keeping __init__.py files."
