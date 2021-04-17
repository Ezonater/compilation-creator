from __future__ import unicode_literals

import subprocess

import yaml
import threading
import youtube_dlc
import os
import ffmpeg
import tkinter as tk
import datetime
import math
import time
import collections
import copy

from tkinter import filedialog
from mutagen.mp3 import MP3
from subprocess import CREATE_NO_WINDOW

current_playlist = None
current_thumbnail = None
current_title = None

# Default values
video_bitrate = 1000000
audio_bitrate = 128000
generate_timestamps = False

currently_rendering = False

# Shortcuts
tracklist = os.getcwd() + '\\tracklist'


# Useful functions
def load_config():
    global generate_timestamps
    global video_bitrate
    global audio_bitrate
    with open(os.getcwd() + '\\config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        generate_timestamps = config['generate_timestamps']
        video_bitrate = config['video_bitrate']
        audio_bitrate = config['audio_bitrate']
        print(generate_timestamps)


load_config()


def root_program():
    # Important parameters
    global current_playlist
    global current_thumbnail
    global current_title

    # Initialize the program
    root = tk.Tk()
    root.title('Compilation++')
    root.iconphoto(False, tk.PhotoImage(file="icon.png"))

    def render_info():
        start_label.config(
            text="Title: " + title_entry.get() + "\nPlaylist: " + playlist_entry.get() + "\nThumbnail: " + current_thumbnail + "\n" + "\nVideo Bitrate: " + str(
                video_bitrate) + "\nAudio Bitrate: " + str(audio_bitrate) + "\nGenerate Timestamps?: " + str(
                generate_timestamps))

    def check_start_button():
        if (playlist_entry.get() != "") & (title_entry.get() != "") & (current_thumbnail is not None) & (
                current_thumbnail != ""):
            if playlist_entry.get()[:38] == "https://www.youtube.com/playlist?list=":
                if not currently_rendering:
                    start_button.config(state=tk.NORMAL)
                    render_info()
                start_label.pack()
            else:
                start_label.forget()
                start_button.config(state=tk.DISABLED)
                start_label.config(text="Please enter a valid YouTube playlist link.")
                start_label.pack()
        else:
            start_label.forget()
            start_button.config(state=tk.DISABLED)

    def playlist_update(sv):
        global current_playlist
        current_playlist = sv.get()
        check_start_button()

    def title_update(sv):
        global current_title
        current_title = sv.get()
        check_start_button()

    def browseFiles():
        filetime = filedialog.askopenfilename(initialdir="/Pictures",
                                              title="Select a File",
                                              filetypes=(("Image files",
                                                          "*.png* *.jpg*"),
                                                         ("all files",
                                                          "*.*")))
        global current_thumbnail
        current_thumbnail = filetime
        if start_label.winfo_exists():
            render_info()
        check_start_button()
        print(os.path.splitext(os.path.basename(current_thumbnail))[0])

    class Count:
        continue_count = True
        process_name = None
        count_label = None

        def __init__(self, process_name):
            self.process_name = process_name

        def count(self):
            time_elapsed = 0
            self.count_label = tk.Label(root, text="Time Elapsed: ")
            self.count_label.pack()
            while self.continue_count:
                time.sleep(1)
                time_elapsed += 1
                self.count_label.config(
                    text=self.process_name + ": " + str(datetime.timedelta(seconds=math.floor(time_elapsed))))

        def start(self):
            t2 = threading.Thread(target=self.count)
            t2.start()

        def stop(self):
            self.continue_count = False
            self.count_label.forget()

    def playlist_download(playlist):
        # Start the count
        count = Count("Downloading mp3s from playlist")
        count.start()

        # Downloading the videos
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.getcwd() + '\\tracklist\\%(title)s.%(ext)s',
            # 'simulate': 'true',
            # ONLY TURN THIS OFF WHEN DEBUGGING AND YOU ALREADY HAVE MP3s
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }],
        }
        with youtube_dlc.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist])

        # Stop the count
        count.stop()
        del count

    def generate_tracklist():
        # Start the count
        count = Count("Generating tracklist")
        count.start()

        elapsed_time = 0
        f = open('tracklist.txt', 'w')
        f.close()
        for track in os.listdir(os.getcwd() + '\\tracklist'):
            if track.endswith('.mp3'):
                timestamp = str(datetime.timedelta(seconds=math.floor(elapsed_time)))
                elapsed_time += MP3(os.getcwd() + '\\tracklist\\' + track).info.length
                print(timestamp)
                f = open("tracklist.txt", "a", encoding='utf-8')
                f.write(timestamp + ' - ' + os.path.splitext(os.path.basename(track))[0] + '\n')
                f.close()
        # Stop the count
        count.stop()
        del count

    def compile(thumbnail, title):
        # Start the count
        count = Count("Generating thumbnail")
        count.start()

        completelist = []

        # Generate thumbnail video
        subprocess.call(['ffmpeg', '-i', str(thumbnail), '-b:v', str(video_bitrate), '-b:a', str(audio_bitrate), str(
            os.getcwd() + '\\thumbnail\\' + os.path.splitext(os.path.basename(thumbnail))[0] + '.mp4')], creationflags=CREATE_NO_WINDOW)

        # Stop the count
        count.stop()
        del count

        # Start the count
        count = Count("Generating mp3 videos")
        count.start()

        # Generate mp3 videos
        for filename in os.listdir(tracklist):
            if filename.endswith('.mp3'):
                subprocess.call(['ffmpeg', '-i', str(tracklist + '\\' + filename), '-b:v', str(video_bitrate), '-b:a',
                                 str(audio_bitrate),
                                 str(tracklist + '\\mp4\\' + os.path.splitext(filename)[0] + '.mp4')], creationflags=CREATE_NO_WINDOW)

        # Stop the count
        count.stop()
        del count

        # Start the count
        count = Count("Generating mp3 + thumbnail videos")
        count.start()

        # Generate thumbnail + mp3 videos
        for filename in os.listdir(tracklist + '\\mp4'):
            if filename.endswith('.mp4'):
                f = open("concat.txt", "a", encoding='utf-8')
                entry = 'file ' + '\'' + tracklist + '\\mp4\\full\\'
                entry += filename.replace("\'", "\'\\\'\'")
                entry += '\'\n'
                f.write(entry)
                subprocess.call(['ffmpeg',
                                 '-i',
                                 str(os.getcwd() + '\\thumbnail\\' + os.listdir(os.getcwd() + '\\thumbnail\\')[0]),
                                 '-i', str(tracklist + '\\mp4\\' + filename),
                                 '-b:v', str(video_bitrate), '-b:a', str(audio_bitrate),
                                 '-c', 'copy', str(tracklist + '\\mp4\\full\\' + filename)], creationflags=CREATE_NO_WINDOW)
                f.close()

        # Stop the count
        count.stop()
        del count

        # Start the count
        count = Count("Concatenating videos")
        count.start()

        # Concatenate
        subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy', str(title) + '.mp4'], creationflags=CREATE_NO_WINDOW)

        # Stop the count
        count.stop()
        del count

    def clean_up():
        # Start the count
        count = Count("Clean up files")
        count.start()

        # Clean up, clean up. Everybody do your share.

        for filename in os.listdir(tracklist + '\\mp4'):
            if filename.endswith('.mp4'):
                os.remove(tracklist + '\\mp4\\' + filename)

        for filename in os.listdir(tracklist + '\\mp4\\full'):
            if filename.endswith('.mp4'):
                os.remove(tracklist + '\\mp4\\full\\' + filename)

        for filename in os.listdir(os.getcwd() + '\\thumbnail'):
            if filename.endswith('.mp4'):
                os.remove(os.getcwd() + '\\thumbnail\\' + filename)

        for filename in os.listdir(os.getcwd()):
            if filename.endswith('.mp4'):
                if filename != (current_title + '.mp4'):
                    os.remove(os.getcwd() + '\\' + filename)

        for filename in os.listdir(tracklist):
            if filename.endswith('.mp3'):
                os.remove(tracklist + '\\' + filename)

        os.remove("concat.txt")

        # Stop the count
        count.stop()
        del count

    def start_compiling():
        # Grab globals
        global current_playlist
        global current_title
        global current_thumbnail
        global currently_rendering
        global generate_timestamps

        currently_rendering = True

        # Initialize new variables so the user may play with the variables while rendering
        this_playlist = current_playlist
        this_title = current_title
        this_thumbnail = current_thumbnail

        # Deactivate UI
        start_button.config(state=tk.DISABLED)

        # Run main functions
        playlist_download(this_playlist)
        if generate_timestamps:
            generate_tracklist()
        compile(this_thumbnail, this_title)
        clean_up()

        # Reactivate UI
        start_button.config(state=tk.NORMAL)

        currently_rendering = False

    def start_threading():
        t2 = threading.Thread(target=start_compiling)
        t2.start()

    # Add the stuffs
    empty_label = tk.Label(root)
    thumbnail_button = tk.Button(root, text="Pick a Thumbnail", command=browseFiles)
    info_label = tk.Label(root, text="This program was created by Ezonater.\n"
                                     "This project uses resources from youtube-dlc and ffmpeg-python.\n"
                                     "Please note that this program is still in development.\n"
                                     "There still may be tweaks to be made.")
    main_label = tk.Label(root, text="Compilation Generator", font=30, pady=20)
    version_label = tk.Label(root, text="Version Number: 1.0.0")
    playlist_entry_label = tk.Label(root, text="Enter your playlist here:")
    playlist_text_variable = tk.StringVar()
    playlist_text_variable.trace("w",
                                 lambda name, index, mode,
                                        playlist_text_variable=playlist_text_variable,: playlist_update(
                                     playlist_text_variable))
    playlist_entry = tk.Entry(root, textvariable=playlist_text_variable, width=80)
    title_entry_label = tk.Label(root, text="Enter your title here:")
    title_text_variable = tk.StringVar()
    title_text_variable.trace("w", lambda name, index, mode, title_text_variable=title_text_variable,: title_update(
        title_text_variable))
    title_entry = tk.Entry(root, textvariable=title_text_variable, width=50)

    start_label = tk.Label(root, text="Title: " + str(current_title) + "\nPlaylist: " + str(current_playlist), pady=30)
    start_button = tk.Button(root, text="Start!", state=tk.DISABLED, command=start_threading)

    error_text_variable = tk.StringVar()
    error_label = tk.Label(root, textvariable=error_text_variable)

    def settings():
        subprocess.call('config.yaml', shell=True)
        load_config()
        render_info()

    def next_screen():
        # New Window
        root.geometry("600x600")

        # Clean up
        begin_button.forget()
        info_label.forget()
        version_label.forget()

        # New objects
        main_label.pack()
        title_entry_label.pack()
        title_entry.pack()
        playlist_entry_label.pack()
        playlist_entry.pack()
        thumbnail_button.pack()
        empty_label.pack()
        start_button.pack()

        # Menus
        menu = tk.Menu(root)
        root.config(menu=menu)
        fileMenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Settings", command=settings)

    begin_button = tk.Button(root, text="Begin", command=next_screen)
    info_label.pack()
    begin_button.pack()
    version_label.pack()
    root.mainloop()

    # Run the program
    root.mainloop()


t1 = threading.Thread(target=root_program)
t1.run()
