import ffmpeg

video = (
    ffmpeg.input("video.mp4")
    .output("video/output.m3u8", format="hls", hls_time=10, hls_list_size=0)
    .run()
)
