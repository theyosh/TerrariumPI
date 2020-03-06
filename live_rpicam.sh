#!/bin/bash

NAME=$1
WIDTH=$2
HEIGHT=$3
ROTATION=$4
AWB=$5
DIR=$6

# Test defaults
if [[ "${NAME}" == "" ]];
then
  NAME="RPI Live"
fi

if [[ "${WIDTH}" == "" ]];
then
  WIDTH="1920"
fi

if [[ "${HEIGHT}" == "" ]];
then
  HEIGHT="1080"
fi

if [[ "${ROTATION}" == "" ]];
then
  ROTATION="0"
fi

if [[ "${AWB}" == "" ]];
then
  AWB="auto"
fi

if [[ "${DIR}" == "" ]];
then
  DIR="/dev/shm/test"
fi

if [[ ! -d "${DIR}" ]];
then
  mkdir -p "${DIR}"
fi


if [[ "${ROTATION}" == "h" ]];
then
  ROTATION="-hf"
elif [[ "${ROTATION}" == "v" ]];
then
  ROTATION="-vf"
else
  ROTATION="-rot ${ROTATION}"
fi

`which raspivid` -o - -b 2000000 -t 0 -w ${WIDTH} -h ${HEIGHT} ${ROTATION} -awb ${AWB} --drc low -fps 30 -g 30 -pf main -lev 4.1 -ae 16,0xff,0x808000 -a 8 -a " ${NAME} @ %d/%m/%Y %X " -a 1024 | \
 `which ffmpeg` -hide_banner -nostdin -re -i - -c:v copy -f hls -hls_time 2 -hls_list_size 3 -hls_flags delete_segments+split_by_time -hls_segment_filename "${DIR}/chunk_%03d.ts" "${DIR}/stream.m3u8"
