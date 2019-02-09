#!/bin/bash

for i in $(seq 1 30); do 
	proxychains curl --silent $1 &
done
