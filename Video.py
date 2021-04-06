import tkinter
from time import sleep
from itertools import count
from threading import Thread
from tkinter.filedialog import askopenfilename
import pyaudio
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip

root = tkinter.Tk()
root.title("视频播放器")
root.geometry('860x240+200+100')

isplaying = False

lbVideo = tkinter.Label(root, bg='white')
lbVideo.pack(fill=tkinter.BOTH, expand=tkinter.YES)


def play_video(video):
    vw = video.w
    vh = video.h
    for frame in video.iter_frames(fps=video.fps / 2.5):
        if not isplaying:
            break
        w = root.winfo_width()
        h = root.winfo_height()
        ratio = min(w / vw, h / vh)
        size = (int(vw * ratio), int(vh * ratio))
        frame = Image.fromarray(frame).resize(size)
        frame = ImageTk.PhotoImage(frame)
        lbVideo['image'] = frame
        lbVideo.image = frame
        lbVideo.update()


def play_audio(audio):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=2,
                    rate=44100,
                    output=True)
    for chunk in audio.iter_frames():
        if not isplaying:
            break
        stream.write(chunk.astype('float32').tostring())
    p.terminate()


mainMenu = tkinter.Menu(root)
subMenu = tkinter.Menu(tearoff=0)


def open_video():
    global isplaying
    isplaying = False
    fn = askopenfilename(title='打开视频文件', filetypes=[('视频', '*.mp4')])
    if fn:
        root.title(f'正在播放"{fn}"')
        video = VideoFileClip(fn)
        audio = video.audio
        isplaying = True

        t1 = Thread(target=play_audio, args=(video,))
        t1.daemon = True
        t1.start()
        t2 = Thread(target=play_audio, args=(audio,))
        t2.daemon = True
        t2.start()


subMenu.add_command(label='打开视频文件', command=open_video)
mainMenu.add_cascade(label='文件', menu=subMenu)
root['menu'] = mainMenu


def exiting():
    global isplaying
    isplaying = False
    sleep(0.05)
    root.destroy()


root.protocol('WM_DELETE_WINDOW', exiting)

root.mainloop()