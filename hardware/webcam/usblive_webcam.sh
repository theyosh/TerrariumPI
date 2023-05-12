#!/bin/bash

# Available parameters
NAME=$1
WIDTH=$2
HEIGHT=$3
ROTATION=$4
AWB=$5
DIR=$6

# Find the needed programs
FFMPEG=$(which ffmpeg)

# Defaults
if [[ "${NAME}" == "" ]]; then
  NAME="USB Live"
fi

if [[ "${WIDTH}" == "" ]]; then
  WIDTH="1280"
fi

if [[ "${HEIGHT}" == "" ]]; then
  HEIGHT="720"
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
  ROTATION_ACTION="hflip,"
elif [[ "${ROTATION}" == "v" ]]; then
  ROTATION_ACTION="vflip,"
elif [[ "${ROTATION}" == "0" ]]; then
  ROTATION_ACTION=""
elif [[ "${ROTATION}" == "90" ]]; then
  ROTATION_ACTION="transpose=1,"
elif [[ "${ROTATION}" == "180" ]]; then
  ROTATION_ACTION="transpose=2,transpose=2,"
elif [[ "${ROTATION}" == "270" ]]; then
  ROTATION_ACTION="transpose=2,"
fi

# Start streaming
"${FFMPEG}" -hide_banner -y -nostdin -f v4l2 -flags +global_header -pix_fmt yuv420p -framerate 30 -video_size "${WIDTH}x${HEIGHT}" -re -i /dev/video0 \
 -c:v h264_omx -profile:v 66 -flags:v +global_header -flags +cgop -g 6 -b:v 2000K -vf "${ROTATION_ACTION}format=yuv420p,drawtext=fontfile=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf:box=1:boxcolor=black:text='${NAME} %{localtime\:%a %d %b %Y @ %H\\\\\:%M\\\\\:%S}':fontsize=14:fontcolor=white@1:x=3:y=3" -f hls -hls_time 2 -hls_list_size 3 -hls_flags delete_segments+split_by_time -hls_segment_filename "${DIR}/chunk_%03d.ts" "${DIR}/stream.m3u8"
