import time
import cv2
import threading


class Producer(threading.Thread):
    def __init__(self, str):
        super(Producer, self).__init__()
        self.str = str
        self.cap = cv2.VideoCapture(self.str)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        print(self.fps)
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print(size)
        fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
        # 定义视频文件输入对象
        self.outVideo = cv2.VideoWriter('saveDir.avi', fourcc, self.fps, size)
        cv2.namedWindow("cap video", 0)

    def run(self):
        print('in producer')
        while True:
            ret, image = self.cap.read()
            if ret:
                cv2.imshow('cap video', image)
                self.outVideo.write(image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.outVideo.release()
                self.cap.release()
                cv2.destroyAllWindows()
                break
            time.sleep(1 / self.fps)


if __name__ == '__main__':
    print('run program')
    rtsp_str = './video/videoTest.avi'
    producer = Producer(rtsp_str)
    producer.run()
