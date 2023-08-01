#!/bin/bash

# Available parameters
DEVICE=$1
NAME=$2
WIDTH=$3
HEIGHT=$4
ROTATION=$5
AWB=$6
DIR=$7

# Find the needed programs
RASPIVID=$(which raspivid)
FFMPEG=$(which ffmpeg)

# Defaults
if [[ "${NAME}" == "" ]]; then
  NAME="RPI Live"
fi

if [[ "${WIDTH}" == "" ]]; then
  WIDTH="1920"
fi

if [[ "${HEIGHT}" == "" ]]; then
  HEIGHT="1080"
fi

if [[ "${ROTATION}" == "" ]]; then
  ROTATION="0"
fi

if [[ "${AWB}" == "" ]]; then
  AWB="auto"
fi

if [[ "${DIR}" == "" ]]; then
  DIR="/dev/shm/test"
fi

if [[ ! -d "${DIR}" ]]; then
  mkdir -p "${DIR}"
fi

ROTATION_ACTION=""
if [[ "${ROTATION}" == "h" ]]; then
  ROTATION_ACTION="--hflip"
  ROTATION=""
elif [[ "${ROTATION}" == "v" ]]; then
  ROTATION_ACTION="--vflip"
  ROTATION=""
else
  ROTATION_ACTION="--rotation"
fi

# Start streaming
"${RASPIVID}" --output - --bitrate 2000000 --timeout 0 --width "${WIDTH}" --height "${HEIGHT}" "${ROTATION_ACTION}" "${ROTATION}" --awb "${AWB}" --framerate 30 --intra 30 --profile high --level 4.2 -ae 16,0xff,0x808000 -a 8 -a " ${NAME} @ %d/%m/%Y %X " -a 1024 | \
 "${FFMPEG}" -hide_banner -nostdin -re -i - -c:v copy -f hls -hls_time 2 -hls_list_size 3 -hls_flags delete_segments+split_by_time -hls_segment_filename "${DIR}/chunk_%03d.ts" "${DIR}/stream.m3u8"