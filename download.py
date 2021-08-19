from __future__ import unicode_literals
import subprocess
from subprocess import PIPE, CREATE_NO_WINDOW
import os
import youtube_dlc

import util


def playlist_download(window, link, audio_bitrate):
    window.progress.setFormat("Downloading playlist: %p%")

    class MyLogger(object):
        def __init__(self):
            self.download_progress = 0
            self.current_download = 0

        def debug(self, msg):
            print("\n" + msg)
            if msg.startswith('[download] Downloading video'):
                self.current_download = int(msg[msg.index('video') + 6:].split(" of ")[0])
                self.download_progress = 0
                tracklist_size = int(msg[msg.index('video') + 6:].split(" of ")[1])
                window.progress.setMaximum(tracklist_size * 100)
            if '[download]' in msg and "%" in msg:
                self.download_progress = float(
                    msg[:msg.index('%')].split(" ")[len(msg[:msg.index('%')].split(" ")) - 1])
            window.progress.setValue(self.download_progress + (self.current_download - 1) * 100)

        def warning(self, msg):
            print('warn: ' + msg)

        def error(self, msg):
            print('err: ' + msg)

    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': os.getcwd() + '/tracklist/%(playlist_index)s-%(title)s.%(ext)s',
        'ignoreerrors': True,
        'nooverwrites': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': str(audio_bitrate),
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dlc.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


def ambience_download(window, amb, audio_bitrate):
    window.progress.setValue(0)
    for ambience in amb:
        if util.valid_link(ambience['link']):
            window.progress.setFormat("Downloading ambience: %p%")
            window.progress.setMaximum(100)
            file_path=None

            class MyLogger(object):
                def __init__(self):
                    self.download_progress = 0

                def debug(self, msg):
                    print("\n" + msg)
                    if '[download]' in msg and "%" in msg:
                        self.download_progress = float(
                            msg[:msg.index('%')].split(" ")[len(msg[:msg.index('%')].split(" ")) - 1])
                    window.progress.setValue(self.download_progress + (self.current_download - 1) * 100)
                    if '[ffmpeg]' in msg and "ambience" in msg:
                        global file_path
                        file_path = msg[msg.index('ambience'):]

                def warning(self, msg):
                    print('warn: ' + msg)

                def error(self, msg):
                    print('err: ' + msg)

            def my_hook(d):
                if d['status'] == 'finished':
                    print('Done downloading, now converting ...')

            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': '/ambience/%(title)s.%(ext)s',
                'ignoreerrors': True,
                'nooverwrites': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': str(audio_bitrate),
                }],
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }
            with youtube_dlc.YoutubeDL(ydl_opts) as ydl:
                ydl.download([ambience['link']])

            p = subprocess.Popen(
                ['ffmpeg', '-i', 'big_audio.mp3', '-b:a', str(audio_bitrate), '-filter_complex', 'loudnorm',
                 'normalized_audio.mp3'], stdin=PIPE, stderr=subprocess.STDOUT, stdout=PIPE,
                creationflags=CREATE_NO_WINDOW, universal_newlines=True)
