from __future__ import unicode_literals

from tkinter import filedialog

import youtube_dlc
import os
import ffmpeg
import tkinter as tk

# Important parameters
current_playlist = None
current_thumbnail = None
current_title = None

# Default values
video_bitrate = 1500000
audio_bitrate = 256000

# Initialize the program
root = tk.Tk()
root.title('Compilation Software')
root.geometry("300x100")


def check_start_button():
    if (playlist_entry.get() != "") & (title_entry.get() != "") & (current_thumbnail is not None):
        if playlist_entry.get()[:38] == "https://www.youtube.com/playlist?list=":
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
    current_playlist = sv
    check_start_button()


def title_update(sv):
    global current_title
    current_title = sv
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


def start():
    global current_playlist
    global current_thumbnail
    global current_title


# Add the stuffs
thumbnail_button = tk.Button(root, text="Pick a Thumbnail", command=browseFiles)
info_label = tk.Label(root, text="Please note that this program is still in development.")
main_label = tk.Label(root, text="Compilation Generator", font=30, pady=20)
playlist_entry_label = tk.Label(root, text="Enter your playlist here:")
playlist_text_variable = tk.StringVar()
playlist_text_variable.trace("w",
                             lambda name, index, mode, playlist_text_variable=playlist_text_variable,: playlist_update(
                                 playlist_text_variable))
playlist_entry = tk.Entry(root, textvariable=playlist_text_variable)
title_entry_label = tk.Label(root, text="Enter your title here:")
title_text_variable = tk.StringVar()
title_text_variable.trace("w", lambda name, index, mode, title_text_variable=title_text_variable,: title_update(
    title_text_variable))
title_entry = tk.Entry(root, textvariable=title_text_variable)

start_label = tk.Label(root, text="Title: " + str(current_title) + "\nPlaylist: " + str(current_playlist), pady=30)
start_button = tk.Button(root, text="Start!", state=tk.DISABLED)
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

    # New objects
    main_label.pack()
    title_entry_label.pack()
    title_entry.pack()
    playlist_entry_label.pack()
    playlist_entry.pack()
    thumbnail_button.pack()
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
root.mainloop()

# Run the program
root.mainloop()

# Downloading the videos
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.getcwd() + '\\tracklist\\%(title)s.%(ext)s',
    'simulate': 'true',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dlc.YoutubeDL(ydl_opts) as ydl:
    ydl.download([current_playlist])

tracklist = os.getcwd() + '\\tracklist'
songlist = []

(
    ffmpeg
        .input(current_thumbnail)
        .output(os.getcwd() + '\\thumbnail\\' + os.path.splitext(os.path.basename(current_thumbnail))[0] + '.mp4',
                audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)
        .run()
)

for filename in os.listdir(tracklist):
    if filename.endswith('.mp3'):
        (
            ffmpeg
                .input(tracklist + '\\' + filename)
                .output(tracklist + '\\mp4\\' + os.path.splitext(filename)[0] + '.mp4', audio_bitrate=audio_bitrate,
                        video_bitrate=video_bitrate)
                .run()
        )

for filename in os.listdir(tracklist + '\\mp4'):
    if filename.endswith('.mp4'):
        video_video = ffmpeg.input(os.getcwd() + '\\thumbnail\\' + os.listdir(os.getcwd() + '\\thumbnail\\')[0])
        audio_video = ffmpeg.input(tracklist + '\\mp4\\' + filename)
        v1 = video_video.video
        a1 = audio_video.audio
        ffmpeg.output(v1, a1, tracklist + '\\mp4\\full\\' + filename, audio_bitrate=audio_bitrate,
                      video_bitrate=video_bitrate).run()

# Create base video
in1 = ffmpeg.input(tracklist + '\\mp4\\full\\' + os.listdir(tracklist + '\\mp4\\full')[0])
in2 = ffmpeg.input(tracklist + '\\mp4\\full\\' + os.listdir(tracklist + '\\mp4\\full')[1])
stupidlist = []
v1 = in1.video
v2 = in2.video
a1 = in1.audio
a2 = in2.audio
joined = ffmpeg.concat(v1, a1, v2, a2, v=1, a=1).node
v3 = joined[0]
a3 = joined[1]
ffmpeg.output(v3, a3, '0.mp4', audio_bitrate=audio_bitrate, video_bitrate=video_bitrate).run()

final_name = 0

for _ in range(len(os.listdir(tracklist + '\\mp4\\full\\')) - 2):
    in1 = ffmpeg.input(str(_) + '.mp4')
    in2 = ffmpeg.input(tracklist + '\\mp4\\full\\' + os.listdir(tracklist + '\\mp4\\full')[_ + 2])
    v1 = in1.video
    v2 = in2.video
    a1 = in1.audio
    a2 = in2.audio
    joined = ffmpeg.concat(v1, a1, v2, a2, v=1, a=1).node
    v3 = joined[0]
    a3 = joined[1]
    ffmpeg.output(v3, a3, str(_ + 1) + '.mp4', audio_bitrate=audio_bitrate, video_bitrate=video_bitrate).run()
    final_name = str(_ + 1)

os.rename(final_name + '.mp4', current_title + '.mp4')

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

# proc  = subprocess.Popen(
# [
# os.getcwd() + '\\venv\\ffmpeg\\bin\\ffmpeg.exe'
# ]
# )
