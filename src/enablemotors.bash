#!/bin/bash
read -p 'Total bots: ' tb
for (( c=1; c<=tb; c++ )); 
        do
            rosservice call /robot$c/enable_motors true
        done