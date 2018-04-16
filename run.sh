#!/bin/bash
# Master script.

cd "$(dirname "$0")"
source ~/.virtualenvs/memtracker/bin/activate
cd ~/memtracker
python main.py
