#!/bin/bash

DIR=$1

raspivid -b 2000000 -o - -t 0 -w 1920 -h 1080 -fps 30 -g 30 -pf baseline -lev 4.1 | \
 ffmpeg -nostdin -re -i - -c:v copy -f hls -hls_time 2 -hls_list_size 3 -hls_flags delete_segments+split_by_time+program_date_time -hls_segment_filename "${DIR}/chunk_%03d.ts" "${DIR}/stream.m3u8"
