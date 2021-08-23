import re
import os
import datetime
import math
from mutagen.mp3 import MP3
from PIL import Image
def valid_link(link):
    if re.search('(?:https?:\\/\\/)?(?:www\\.)?youtu\\.?be(?:\\.com)?\\/?.*(?:watch|embed)?(?:.*v=|v\\/|\\/)([\\w\\-_]+)\\&?', link):
        return True
    else: return False

def valid_filename(string):
    return "".join(i for i in string if i not in "\/:*?<>|")

def generate_tracklist(config):
    elapsed_time = 0
    f = open('tracklist.txt', 'w')
    f.close()
    for track in os.listdir(os.getcwd() + '\\tracklist'):
        if track.endswith('.mp3'):
            timestamp = str(datetime.timedelta(seconds=math.floor(elapsed_time)))
            elapsed_time += MP3(os.getcwd() + '\\tracklist\\' + track).info.length
            print(timestamp)
            if config.options_dict['generate_timestamps']:
                f = open("tracklist.txt", "a", encoding='utf-8')
                trackname = os.path.splitext(os.path.basename(track))[0]
                if config.options_dict['keep_order']:
                    trackname = trackname[trackname.index('-') + 1:]
                f.write(timestamp + ' - ' + trackname + '\n')
                f.close()
    return elapsed_time

def clean_up():
    # Clean up, clean up. Everybody do your share.

    if not os.path.isdir(os.path.join(os.getcwd(),"tracklist")):
        os.mkdir(os.path.join(os.getcwd(),"tracklist"))
    for filename in os.listdir(os.path.join(os.getcwd(),"tracklist")):
        os.remove(os.path.join(os.path.join(os.getcwd(),"tracklist"),filename))

    if not os.path.isdir(os.path.join(os.getcwd(),"ambience")):
            os.mkdir(os.path.join(os.getcwd(),"ambience"))
    for filename in os.listdir(os.path.join(os.getcwd(),"ambience")):
        os.remove(os.path.join(os.path.join(os.getcwd(),"ambience"),filename))

    if os.path.isfile("concat.txt"):
        os.remove("concat.txt")

    if os.path.isfile("big_audio.mp3"):
        os.remove("big_audio.mp3")

    if os.path.isfile("normalized_audio.mp3"):
        os.remove("normalized_audio.mp3")

    if os.path.isfile("thumbnail.png"):
        os.remove("thumbnail.png")

def stretch_image(path):
    with Image.open(path) as im:
        print(im.width)
        print(im.height)
        size = (1280,720)
        if im.width > im.height:
            width = 80 * round(im.width/80)
            size = (width, int(45*(width/80)))
        elif im.height > im.width:
            height = 45 * round(im.width/45)
            size = (int(80*(height/45)), height)
        else:
            width = 80 * round(im.width/80)
            size = (width, int(45*(width/80)))
        im = im.resize(size)
        im.save("thumbnail.png", "PNG")
        return "thumbnail.png"