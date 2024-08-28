#!/bin/sh

## This script updates the ~/.ssh/known_hosts with keys for the IP address specified as argument.

ssh-keygen -R $1
ssh-keyscan -t rsa $1 >> ~/.ssh/known_hosts
