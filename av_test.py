import av

video_name = './video/test.mp4'
container = av.open(video_name)
stream = next(s for s in container.streams if s.type == 'video')
print(stream.pix_fmt)
# for frame in container.decode(video=0):
#     print(stream.pix_fmt)

print(stream)
print("container:", container)
print("container.streams:", container.streams)
print("container.format:", container.format)
