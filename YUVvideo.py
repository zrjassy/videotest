import sys
import time
import cv2
import os
import numpy as np


def str2int(string):
    # 去除'.png'
    return int(string[0:-4])


def readYUV(file, height, width, start_frame):
    """
    :param file: 待处理 YUV 视频的名字
    :param height: YUV 视频中图像的高
    :param width: YUV 视频中图像的宽
    :param start_frame: 起始帧
    :return: None
    """
    H = height
    W = width
    uv_H = H // 2
    uv_W = W // 2

    fp = open(file, 'rb')
    fp.seek(0, 2)  # 设置文件指针到文件流的尾部 + 偏移 0
    fp_end = fp.tell()  # 获取文件尾指针位置

    frame_size = height * width * 3 // 2  # 一帧图像所含的像素个数
    num_frame = fp_end // frame_size  # 计算 YUV 文件包含图像数
    print("This yuv file has {} frame images!".format(num_frame))
    fp.seek(frame_size * start_frame, 0)  # 设置文件指针到文件流的起始位置 + 偏移 frame_size * startframe

    Y = np.zeros((num_frame, H, W), np.uint8)
    U = np.zeros((num_frame, uv_H, uv_W), np.uint8)
    V = np.zeros((num_frame, uv_H, uv_W), np.uint8)

    # 从YUV文件中获取每一帧图像上每一个像素的YUV值
    for i in range(num_frame):
        for m in range(H):
            for n in range(W):
                Y[i, m, n] = ord(fp.read(1))
        for m in range(uv_H):
            for n in range(uv_W):
                U[i, m, n] = ord(fp.read(1))
        for m in range(uv_H):
            for n in range(uv_W):
                V[i, m, n] = ord(fp.read(1))
        print('读取第{}帧图像'.format(i + 1))
        # rgb = yuv2rgb(Y[i, :, :], U[i, :, :], V[i, :, :])
        # print('保存第{}帧图像'.format(i + 1))
        # cv2.imwrite('yuv2bgr/{}.png'.format(i + 1), rgb)
    # 将YUV转换成RGB并生成图像保存
    image = []
    # 将YUV转换成RGB并播放
    for i in range(num_frame):
        # 通过yuv2rgb函数将YUV数据转换成RGB数据
        rgb = yuv2rgb(Y[i, :, :], U[i, :, :], V[i, :, :])
        image.append(rgb)
    for i in range(num_frame):
        # 显示
        cv2.imshow('test', image[i])
        # 当按下 Q 键时退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        # 保持 1/fps 秒
        time.sleep(1 / 50)


def yuv2rgb(y, u, v):
    """
    :param y: y分量
    :param u: u分量
    :param v: v分量
    :return: rgb格式数据
    """
    rows, cols = y.shape[:2]
    img = np.concatenate((y.reshape(-1), u.reshape(-1), v.reshape(-1)))
    img = img.reshape((rows * 3 // 2, cols)).astype('uint8')
    # 选择转换格式 COLOR_YUV2BGR_I420
    bgr_img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_I420)
    return bgr_img
    # # 创建r,g,b分量
    # r = np.zeros((rows, cols), np.uint8)
    # g = np.zeros((rows, cols), np.uint8)
    # b = np.zeros((rows, cols), np.uint8)
    #
    # for i in range(rows):
    #     for j in range(int(cols)):
    #         Y = y[i, j]
    #         U = u[i // 2, j // 2] - 128
    #         V = v[i // 2, j // 2] - 128
    #         R_dif = V + ((V * 103) >> 8)
    #         G_dif = ((U * 88) >> 8) + ((V * 183) >> 8)
    #         B_dif = U + ((U * 198) >> 8)
    #         r[i, j] = max(0, min(255, Y + R_dif))
    #         g[i, j] = max(0, min(255, Y - G_dif))
    #         b[i, j] = max(0, min(255, Y + B_dif))
    #         # r[i, j] = max(0, min(255, y[i, j] + 1.402 * (v[i // 2, j // 2] - 128)))
    #         # g[i, j] = max(0, min(255, y[i, j] - 0.34414 * (u[i // 2, j // 2] - 128) - 0.71414 * (v[i // 2, j // 2] - 128)))
    #         # b[i, j] = max(0, min(255, y[i, j] + 1.772 * (u[i // 2, j // 2] - 128)))
    # rgb = cv2.merge([b, g, r])
    # return rgb


def jpg2avi(fps, image_dir, video_dir):
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
    # 调整顺序
    frames = sorted(os.listdir(image_dir), key=str2int)
    # w,h of image
    img = cv2.imread(os.path.join(image_dir, frames[0]))
    img_size = (img.shape[1], img.shape[0])
    # get seq name
    seq_name = 'videotest'
    # splice video_dir
    video_Path = os.path.join(video_dir, seq_name + '.avi')
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    # also can write like:fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    # if want to write .mp4 file, use 'MP4V'
    videoWriter = cv2.VideoWriter(video_Path, fourcc, fps, img_size)

    for frame in frames:
        f_path = os.path.join(image_dir, frame)
        image = cv2.imread(f_path)
        videoWriter.write(image)
        print(frame + " has been written!")

    videoWriter.release()
    return video_Path


def videoPlayer(filepath):
    cap = cv2.VideoCapture(filepath)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    while True:
        ret, image = cap.read()
        if ret:
            src = cv2.resize(image, (frame_width, frame_height), interpolation=cv2.INTER_CUBIC)
            cv2.imshow('cap video', src)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        time.sleep(1 / fps)


if __name__ == "__main__":
    # 将YUV文件以每一帧大小读取数据生成图像
    readYUV('BasketballDrill_832x480_50.yuv', 480, 832, start_frame=0)
    # 将所有图像合成为视频
    # video_path = jpg2avi(fps=50, image_dir='./yuv', video_dir='./video')
    # video_path = './video/videoTest.avi'
    # # 播放视频
    # videoPlayer(video_path)
    sys.exit()
