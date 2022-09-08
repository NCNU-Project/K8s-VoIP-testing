#!/bin/bash

if [ -f /data/rtpengine/*.env ];then
    for f in /data/rtpengine/*.env;do
        source $f
    done
fi

python3 main.py

