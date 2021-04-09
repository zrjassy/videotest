import os
import subprocess
import PIL

import av
import av.datasets


h264_path = 'night-sky.h264'
if not os.path.exists(h264_path):
    subprocess.check_call([
        'ffmpeg',
        '-i', './video/test.mp4',
        '-vcodec', 'copy',
        '-an',
        '-bsf:v', 'h264_mp4toannexb',
        h264_path,
    ])

fh = open(h264_path, 'rb')

codec = av.CodecContext.create('h264', 'r')

while True:
    chunk = fh.read(1 << 16)
    packets = codec.parse(chunk)
    print("Parsed {} packets from {} bytes:".format(len(packets), len(chunk)))
    for packet in packets:
        # print('   ', packet)
        frames = codec.decode(packet)
        for frame in frames:
            # print('       ', frame)
            image = frame.to_image()
            image.show()

    # We wait until the end to bail so that the last empty `buf` flushes
    # the parser.
    if not chunk:
        break