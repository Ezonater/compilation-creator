from __future__ import unicode_literals
from tkinter import filedialog
from mutagen.mp3 import MP3

import yaml
import threading
import youtube_dlc
import os
import ffmpeg
import tkinter as tk
import datetime
import math

current_playlist = None
current_thumbnail = None
current_title = None

# Default values
video_bitrate = 1500000
audio_bitrate = 256000
generate_timestamps = False

currently_rendering = False

with open(os.getcwd() + '\\config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    generate_timestamps = config['generate_timestamps']
    print(generate_timestamps)

# Shortcuts
tracklist = os.getcwd() + '\\tracklist'

def root_program():
    # Important parameters
    global current_playlist
    global current_thumbnail
    global current_title

    # Initialize the program
    root = tk.Tk()
    root.title('Compilation Software')

    def check_start_button():
        if (playlist_entry.get() != "") & (title_entry.get() != "") & (current_thumbnail is not None):
            if playlist_entry.get()[:38] == "https://www.youtube.com/playlist?list=":
                if not currently_rendering:
                    start_button.config(state=tk.NORMAL)
                start_label.config(
                    text="Title: " + title_entry.get() + "\nPlaylist: " + playlist_entry.get() + "\nThumbnail: " + current_thumbnail)
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
            start_label.config(
                text="Title: " + title_entry.get() + "\nPlaylist: " + playlist_entry.get() + "\nThumbnail: " + current_thumbnail)
        check_start_button()
        print(os.path.splitext(os.path.basename(current_thumbnail))[0])

    def playlist_download(playlist):
        # Downloading the videos
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.getcwd() + '\\tracklist\\%(title)s.%(ext)s',
            # 'simulate': 'true',
            # ONLY TURN THIS OFF WHEN DEBUGGING AND YOU ALREADY HAVE MP3s
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dlc.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist])

    def generate_tracklist():
        elapsed_time = 0
        for track in os.listdir(os.getcwd() + '\\tracklist'):
            if track.endswith('.mp3'):
                timestamp = str(datetime.timedelta(seconds=math.floor(elapsed_time)))
                elapsed_time += MP3(os.getcwd() + '\\tracklist\\' + track).info.length
                print(timestamp)

    def compile(thumbnail, title):
        completelist = []
        # Generate thumbnail video
        (
            ffmpeg
                .input(thumbnail)
                .output(os.getcwd() + '\\thumbnail\\' + os.path.splitext(os.path.basename(thumbnail))[0] + '.mp4',
                        audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)
                .run()
        )

        # Generate mp3 videos
        for filename in os.listdir(tracklist):
            if filename.endswith('.mp3'):
                (
                    ffmpeg
                        .input(tracklist + '\\' + filename)
                        .output(tracklist + '\\mp4\\' + os.path.splitext(filename)[0] + '.mp4',
                                audio_bitrate=audio_bitrate,
                                video_bitrate=video_bitrate)
                        .run()
                )

        # Generate thumbnail + mp3 videos
        for filename in os.listdir(tracklist + '\\mp4'):
            if filename.endswith('.mp4'):
                video_video = ffmpeg.input(os.getcwd() + '\\thumbnail\\' + os.listdir(os.getcwd() + '\\thumbnail\\')[0])
                audio_video = ffmpeg.input(tracklist + '\\mp4\\' + filename)
                v1 = video_video.video
                a1 = audio_video.audio
                ffmpeg.output(v1, a1, tracklist + '\\mp4\\full\\' + filename, audio_bitrate=audio_bitrate,
                              video_bitrate=video_bitrate).run()
                completelist.append(v1)
                completelist.append(a1)

        # Concatenate
        joined = ffmpeg.concat(*completelist, v=1, a=1).node
        v3 = joined[0]
        a3 = joined[1]
        ffmpeg.output(v3, a3, title + '.mp4', audio_bitrate=audio_bitrate, video_bitrate=video_bitrate).run()

    def clean_up():
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

        # Deactivate UI
        title_entry.config(state=tk.NORMAL)
        playlist_entry.config(state=tk.NORMAL)
        thumbnail_button.config(state=tk.NORMAL)
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
    playlist_entry = tk.Entry(root, textvariable=playlist_text_variable, width=50)
    title_entry_label = tk.Label(root, text="Enter your title here:")
    title_text_variable = tk.StringVar()
    title_text_variable.trace("w", lambda name, index, mode, title_text_variable=title_text_variable,: title_update(
        title_text_variable))
    title_entry = tk.Entry(root, textvariable=title_text_variable)

    start_label = tk.Label(root, text="Title: " + str(current_title) + "\nPlaylist: " + str(current_playlist), pady=30)
    start_button = tk.Button(root, text="Start!", state=tk.DISABLED, command=start_threading)
    error_text_variable = tk.StringVar()
    error_label = tk.Label(root, textvariable=error_text_variable)

    def settings():
        print("hi")

    def next_screen():
        # New Window
        root.title("This is the main menu")
        root.geometry("400x400")

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
