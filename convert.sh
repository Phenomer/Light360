#!/bin/sh

VIDEO_NAME=sample01
SOURCE_VIDEO=movie.mp4
EXPORT_DIR=videos/${VIDEO_NAME}

mkdir -p ${EXPORT_DIR}
rye run python3 light360.py -i "${SOURCE_VIDEO}" -o "${EXPORT_DIR}/light.json"
ffmpeg -i "${SOURCE_VIDEO}" -c:v copy -c:a aac -ac 2 \
    -f hls \
    -hls_time 1 \
    -hls_list_size 0 \
    -hls_flags +split_by_time \
    -hls_segment_type fmp4 \
    -hls_fmp4_init_filename "init.mp4" \
    -hls_segment_filename "${EXPORT_DIR}/segment_%04d.m4s" \
    ${EXPORT_DIR}/video.m3u8
