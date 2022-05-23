#!/bin/bash

while true
do
  cd .monitor
  ./main.py
  cd ..
  sleep 300
done