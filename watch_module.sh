#!/bin/bash
# SCRIPT=${1:-extract_data.py}
watchmedo shell-command --patterns="*.py" --recursive --command="python extract_data.py"