from moviepy.editor import *

def video_compress(folder):
    for file in os.listdir(os.path.join(folder)):
        if file.endswith('.mov') or  file.endswith('.mp4') :
              clip = VideoFileClip(os.path.join(folder,file))
              final = clip.fx(vfx.resize, width = 500,height = 500)
              final.write_videofile(os.path.join(folder,file))


folder = 'uploads/'

video_compress(folder)