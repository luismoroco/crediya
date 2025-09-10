#!/bin/bash

ansible-playbook infrastructure/playbook/configure_environment.yml -e "environment=docker"
