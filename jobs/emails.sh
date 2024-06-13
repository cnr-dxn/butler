#!/bin/bash

EMAIL_SCRIPT="/home/cnrdxn/butler/insertingEmails/main.py"
ARGS="commit"

source /home/cnrdxn/.bashrc
/usr/bin/python3 $EMAIL_SCRIPT $ARGS
