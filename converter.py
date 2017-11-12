# load libraries

import os
from random import randint
import numpy as np
import cv2
from PIL import Image
import PIL.ImageOps
from moviepy.editor import *

# load clip & get frame count

clip = VideoFileClip(“SOURCEFILE”) #.subclip(10,10) #CompositeVideoClip([sourceB, sourceA])
frameCount = int(clip.fps * clip.duration) # count number of frames or set a constant /// int(100) #
print('video frame count: ' + str(frameCount))
print(clip.duration)
frameArray = []



# divide into frames, convert each frame to 1-bit, blend each frame with a Canny-edged version, save

for i in range(frameCount):


    position = i / clip.fps # count frame position
    clip.save_frame(‘/FOLDER/screen.jpg', t=position) # save color frame with moviepy
    image_file = Image.open('/FOLDER/screen.jpg') # open saved frame in PIL
    qualityNum = 100

    image_file = image_file.resize((960, 540)) # resize to get bigger grain
    qualityNum = 100 #abs((i % 7)-3) + randint(1,3) # set image quality

    image_file.save('/FOLDER/screen.jpg', 'JPEG', quality=qualityNum) # save resized frame for further use
    pre_edges = cv2.imread('/FOLDER/screen.jpg',0) # open frame in CV
    edges = cv2.Canny(pre_edges, 20, 150) # add Canny edges
    edges = cv2.imwrite('/FOLDER/screen_edges.jpg', edges) # save image with edges for further use
    image_file = Image.open('/FOLDER/screen.jpg') # open frame
    image_edges = Image.open('/FOLDER/screen_edges.jpg') # open edges in PIL
    image_file = Image.composite(image_edges, image_file, image_edges) # overlay 1-bit and edges

    image_file = image_file.convert('1') # convert image to 1-bit black and white
    image_file = image_file.resize((1920, 1080)) # resize to get hd without aliasing
    #if randint(0,9) < 0: # flicker
    #  image_file = PIL.ImageOps.invert(image_file)
    image_file = image_file.convert('RGB') # convert image to RGB

    poz = str(i)
    if i < 10: # fix image numbers
        poz = '0000' + poz
    elif i < 100:
        poz = '000' + poz
    elif i < 1000:
        poz = '00' + poz
    elif i < 10000:
        poz = '0' + poz
    filename = '/FOLDER/test/screen' + poz + '.png'
    image_file.save(filename, 'PNG', quality=qualityNum)
    frameArray.append(filename)
    progress = str(int(i * 100 / frameCount))
    print(filename + ' saved, progress: ' + progress + '%') # write progress
os.remove('/FOLDER/screen.jpg')
#os.remove('/FOLDER/screen_edges.jpg')

# create sequence



result = ImageSequenceClip(frameArray, fps=25)
result = result.to_videofile('/FOLDER/test/result.mp4', fps=25) # many options available
