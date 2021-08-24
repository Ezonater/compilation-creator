import os
import subprocess
from subprocess import CREATE_NO_WINDOW, PIPE
from PIL import Image


def compile(window, title, thumbnail, audio_bitrate, video_bitrate, normalize, ambience, total_length):
    print(thumbnail, audio_bitrate, video_bitrate, normalize, total_length)
    concat(window, total_length)
    if normalize:
        normalize_audio(window, audio_bitrate, total_length)
    if ambience:
        add_ambience(window, total_length)
    generate_mp4(window, title, thumbnail, audio_bitrate, video_bitrate, total_length)


def concat(window, total_length):
    print('big audio creation')
    window.progress_update.emit(['format', "Concatenating mp3s: %p%"])
    window.progress_update.emit(['maximum', total_length])
    window.progress_update.emit(['increment', 0])
    for filename in os.listdir(os.getcwd() + "\\tracklist"):
        if filename.endswith('.mp3'):
            f = open("concat.txt", "a", encoding='utf-8')
            entry = 'file ' + '\'' + os.getcwd() + '\\tracklist\\'
            entry += filename.replace("\'", "\'\\\'\'")
            entry += '\'\n'
            f.write(entry)
            f.close()
    p = subprocess.Popen(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', "concat.txt", os.path.join(os.getcwd(),'big_audio.mp3')],
                         stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=PIPE, creationflags=CREATE_NO_WINDOW,
                         universal_newlines=True)
    for line in p.stdout:
        string_line = str(line)
        if "time=" in string_line:
            time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
            h, m, s = time.split(':')
            s, ms = s.split('.')
            seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
            print(seconds_time)
            window.progress_update.emit(['increment', seconds_time])
    window.progress_update.emit(['increment', 100])


def normalize_audio(window, audio_bitrate, total_length):
    print('normalize')
    window.progress_update.emit(['format', "Normalizing audio: %p%"])
    window.progress_update.emit(['maximum', total_length])
    window.progress_update.emit(['increment', 0])
    p = subprocess.Popen(['ffmpeg', '-i', os.path.join(os.getcwd(),'big_audio.mp3'), '-b:a', str(audio_bitrate), '-filter_complex', 'loudnorm',
                          'normalized_audio.mp3'], stdin=PIPE, stderr=subprocess.STDOUT, stdout=PIPE,
                         creationflags=CREATE_NO_WINDOW, universal_newlines=True)
    for line in p.stdout:
        print(line)
        string_line = str(line)
        if "time=" in string_line:
            time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
            h, m, s = time.split(':')
            s, ms = s.split('.')
            seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
            print(seconds_time)
            window.progress_update.emit(['increment', seconds_time])
    window.progress_update.emit(['increment', 100])
    os.remove('big_audio.mp3')
    os.rename('normalized_audio.mp3', 'big_audio.mp3')

def add_ambience(window, total_length):
    for audio in os.listdir(os.path.join(os.getcwd(),"ambience")):
        window.progress_update.emit(['format', "Ambience mixing: %p%"])
        window.progress_update.emit(['maximum', total_length])
        window.progress_update.emit(['increment', 0])
        p = subprocess.Popen(['ffmpeg', '-i', 'big_audio.mp3', '-i', os.path.join(os.getcwd(),"ambience",audio), '-filter_complex', 'amerge=inputs=2', '-ac',
                            '2', 'ambience_audio.mp3'], stdin=PIPE, stderr=subprocess.STDOUT, stdout=PIPE,
                            creationflags=CREATE_NO_WINDOW, universal_newlines=True)
        for line in p.stdout:
            print(line)
            string_line = str(line)
            if "time=" in string_line:
                time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
                h, m, s = time.split(':')
                s, ms = s.split('.')
                seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
                print(seconds_time)
                window.progress_update.emit(['increment', seconds_time])
        window.progress_update.emit(['increment', 100])
        os.remove('big_audio.mp3')
        os.rename('ambience_audio.mp3', 'big_audio.mp3')

def generate_mp4(window, title, thumbnail, audio_bitrate, video_bitrate, total_length):
    window.progress_update.emit(['format', "Generating output: %p%"])
    window.progress_update.emit(['maximum', total_length])
    window.progress_update.emit(['increment', 0])
    p = subprocess.Popen(
        ['ffmpeg', '-y', '-loop', '1', '-framerate', '5', '-i', thumbnail, '-i', 'big_audio.mp3', '-c:v', 'libx264',
         '-tune', 'stillimage', '-c:a', 'aac', '-b:v', str(video_bitrate), '-b:a', str(audio_bitrate), '-pix_fmt',
         'yuv420p', '-vf', 'crop=trunc(iw/2)*2:trunc(ih/2)*2', '-movflags', '+faststart', '-shortest', '-fflags',
         '+shortest', '-max_interleave_delta', '100M', title + '.mp4'], stdout=PIPE, stderr=subprocess.STDOUT, creationflags=CREATE_NO_WINDOW, universal_newlines=True)
    for line in p.stdout:
        print(line)
        string_line = str(line)
        if "time=" in string_line:
            time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
            h, m, s = time.split(':')
            s, ms = s.split('.')
            seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
            print(seconds_time)
            window.progress_update.emit(['increment', seconds_time])
