from moviepy.editor import *
import os
from natsort import natsorted

L =[]

for root, dirs, files in os.walk("/mnt/d/Data/Cloud/OneDrive/UFABC/Computacao/IA/super-mario-world-pbacellar/super-intelligent-mario/results/recordings"):

    #files.sort()
    files = natsorted(files)
    for file in files:
        if os.path.splitext(file)[1] == '.mp4':
            filePath = os.path.join(root, file)
            video = VideoFileClip(filePath)
            L.append(video)

final_clip = concatenate_videoclips(L)
final_clip.to_videofile("output.mp4",audio=False, fps=30, remove_temp=False)