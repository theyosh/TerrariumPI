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
FFMPEG=$(which ffmpeg)

# Defaults
if [[ "${DEVICE}" == "" ]]; then
  DEVICE="rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"
fi

if [[ "${NAME}" == "" ]]; then
  NAME="RTSP Live"
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
  ROTATION_ACTION="vflip,hflip"
elif [[ "${ROTATION}" == "270" ]]; then
  ROTATION_ACTION="transpose=2,"
fi

# Start streaming
"${FFMPEG}" -hide_banner -y -nostdin -stimeout 10000000 -re -i "${DEVICE}" \
 -c:v h264_omx -profile:v 66 -flags:v +global_header -flags +cgop -g 6 -b:v 2000K -vf "${ROTATION_ACTION}format=yuv420p,drawtext=fontfile=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf:box=1:boxcolor=black:text='${NAME} %{localtime\:%a %d %b %Y @ %H\\\\\:%M\\\\\:%S}':fontsize=14:fontcolor=white@1:x=3:y=3" -f hls -hls_time 2 -hls_list_size 3 -hls_flags delete_segments+split_by_time -hls_segment_filename "${DIR}/chunk_%03d.ts" "${DIR}/stream.m3u8"
