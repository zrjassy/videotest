# 将彩色视频转为灰度视频
import imageio

reader = imageio.get_reader('x.mp4')
fps = reader.get_meta_data()['fps']

writer = imageio.get_writer('x.mp4', fps=fps)

for im in reader:
    writer.append_data(im[:, :, 1])
writer.close()
