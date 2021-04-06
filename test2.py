import time

import cv2
import numpy as np

# Video_File = "BasketballDrill_832x480_50.yuv"
Video_File = "/home/jassy/project/c/video/test_out.yuv"
height = 480
width = 832
fp = open(Video_File, 'rb')
filename = Video_File.split('/')[-1][:-4]  # for save
print(filename)
# fp_out = open(savepath+filename+"_out.yuv", 'wb')
fps = 50
Frame_Size = height * width * 3 // 2
h_h = height // 2
h_w = width // 2
fp.seek(0, 2)
ps = fp.tell()
Number_Frame = ps // Frame_Size
fp.seek(0, 0)
image = []
for i in range(Number_Frame):
    print("%d/ %d" % (i + 1, Number_Frame))
    Yt = np.zeros(shape=(height, width), dtype='uint8')
    Ut = np.zeros(shape=(h_h, h_w), dtype='uint8')
    Vt = np.zeros(shape=(h_h, h_w), dtype='uint8')

    for m in range(height):
        for n in range(width):
            Yt[m, n] = ord(fp.read(1))
    for m in range(h_h):
        for n in range(h_w):
            Ut[m, n] = ord(fp.read(1))
    for m in range(h_h):
        for n in range(h_w):
            Vt[m, n] = ord(fp.read(1))
    img = np.concatenate((Yt.reshape(-1), Ut.reshape(-1), Vt.reshape(-1)))
    img = img.reshape((height * 3 // 2, width)).astype('uint8')
    bgr_img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_I420)
    image.append(bgr_img)

for i in range(Number_Frame):
    cv2.imshow('cap video', image[i])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    time.sleep(1 / fps)


class Producer:
    def __init__(self, video_path, width, height):
        self.video_path = video_path
        self.width = width
        self.height = height
        self.fp = open(video_path, 'rb')
