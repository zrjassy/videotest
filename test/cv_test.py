import av_test
import sys

video_name = '../video/test.mp4'
container = av_test.open(video_name)
print(container.streams)
