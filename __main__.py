from __future__ import unicode_literals

import subprocess
import yaml
import threading
import os
import tkinter as tk
import datetime
import math
import time
import PyQt5

from tkinter import filedialog
from mutagen.mp3 import MP3
from subprocess import CREATE_NO_WINDOW, PIPE
from tkinter import ttk
from functools import partial

current_playlist = None
current_thumbnail = None
current_title = None

# Default values
options_dict = {}
keep_order = True
generate_timestamps = False
normalize_audio = True
video_bitrate = 1000000
audio_bitrate = 128000
ip_type = ""
print(options_dict)

ignore_playlist = False  # NOT AN OPTION YET
ip_types = ["", "-4", "-6", "", "-4", "-6"]  # NOT AN OPTION

currently_rendering = False  # Important to disable the start button

# Shortcuts / Helpful info
tracklist = os.getcwd() + '\\tracklist'
tracklist_size = 0


# Useful functions
def load_config():
    global options_dict
    global keep_order
    global generate_timestamps
    global normalize_audio
    global video_bitrate
    global audio_bitrate
    global ip_type
    with open('config.yaml') as file:
        options_dict = yaml.load(file, Loader=yaml.Loader)
        print(options_dict)
    keep_order = options_dict['keep_order']
    generate_timestamps = options_dict['generate_timestamps']
    normalize_audio = options_dict['normalize_audio']
    video_bitrate = options_dict['video_bitrate']
    audio_bitrate = options_dict['audio_bitrate']
    ip_type = options_dict['ip_type']


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
        print(keep_order)
        start_label.config(
            text="Title: " + title_entry.get() + "\nPlaylist: " + playlist_entry.get() + "\nThumbnail: " + current_thumbnail + "\n" + "\nVideo Bitrate: " + str(
                video_bitrate) + "\nAudio Bitrate: " + str(audio_bitrate) + "\nGenerate Timestamps: " + str(
                generate_timestamps) + "\nPerserve Playlist Order: " + str(keep_order))

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
            if self.count_label is not None:
                self.count_label.forget()

    def playlist_download(playlist, ip):
        global ip_type
        print(ip_type)
        # Start the count
        count = Count("Downloading mp3s from playlist")
        count.start()

        p = subprocess.Popen(['youtube-dlc', ip, '--format', 'bestaudio', '-o',
                              os.getcwd() + '\\tracklist\\%(playlist_index)s-%(title)s.%(ext)s', '-x',
                              '--extract-audio',
                              '--audio-format', 'mp3', '--audio-quality', str(audio_bitrate), '-ciw', playlist],
                             stdin=PIPE, stderr=PIPE, stdout=PIPE, creationflags=CREATE_NO_WINDOW)

        # Progress Bar
        print(ip)
        global tracklist_size
        tracklist_size = 0
        current_download = tk.DoubleVar()
        bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate', variable=current_download)
        bar.pack()
        completed_out_of_label = tk.Label(root, text=str(int(current_download.get())) + "/" + str(tracklist_size))
        completed_out_of_label.pack()
        for line in p.stdout:
            print(line)
            string_line = str(line)
            if string_line.startswith('b\'[download] Downloading video'):
                numbers = string_line[string_line.index('video') + 6:len(string_line) - 3]
                current_download.set(int(numbers[:numbers.index('of') - 1]))
                tracklist_size = int(numbers[numbers.index('of') + 3:])
                bar.config(maximum=tracklist_size)
                completed_out_of_label.config(text=str(int(current_download.get())) + "/" + str(tracklist_size))
                root.update_idletasks()
        for line in p.stderr:
            print(line)
            string_line = str(line)
            if string_line.startswith("b\'ERROR: Unable to download webpage: "):
                print(ip_types.index(ip))
                bar.forget()
                completed_out_of_label.forget()
                count.stop()
                del count
                playlist_download(playlist, ip_types[ip_types.index(ip) + 1])
                return

        bar.forget()
        completed_out_of_label.forget()

        # Stop the count
        count.stop()
        del count

    def generate_tracklist():
        elapsed_time = 0
        f = open('tracklist.txt', 'w')
        f.close()
        for track in os.listdir(os.getcwd() + '\\tracklist'):
            if track.endswith('.mp3'):
                timestamp = str(datetime.timedelta(seconds=math.floor(elapsed_time)))
                elapsed_time += MP3(os.getcwd() + '\\tracklist\\' + track).info.length
                print(timestamp)
                f = open("tracklist.txt", "a", encoding='utf-8')
                trackname = os.path.splitext(os.path.basename(track))[0]
                if keep_order:
                    trackname = trackname[trackname.index('-') + 1:]
                f.write(timestamp + ' - ' + trackname + '\n')
                f.close()

    def compile(thumbnail, title):
        # Start the count
        count = Count("Concatenating .mp3 videos")
        count.start()

        # Concat mp4s
        for filename in os.listdir(os.getcwd() + "\\tracklist"):
            if filename.endswith('.mp3'):
                f = open("concat.txt", "a", encoding='utf-8')
                entry = 'file ' + '\'' + os.getcwd() + '\\tracklist\\'
                entry += filename.replace("\'", "\'\\\'\'")
                entry += '\'\n'
                f.write(entry)
                f.close()

        subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', "concat.txt", 'big_audio.mp3'],
                       creationflags=CREATE_NO_WINDOW)

        # Stop the count
        count.stop()
        del count

        if normalize_audio:
            # Start the count
            count = Count("Normalizing Audio")
            count.start()

            subprocess.run(['ffmpeg', '-i', 'big_audio.mp3', '-b:a', str(audio_bitrate), '-filter_complex', 'loudnorm',
                            'normalized_audio.mp3'], creationflags=CREATE_NO_WINDOW)
            os.remove('big_audio.mp3')
            os.rename('normalized_audio.mp3', 'big_audio.mp3')

            # Stop the count
            count.stop()
            del count

        # Start the count
        count = Count("Generating \"" + title + ".mp4\"")
        count.start()

        subprocess.run(
            ['ffmpeg', '-y', '-loop', '1', '-framerate', '5', '-i', thumbnail, '-i', 'big_audio.mp3', '-c:v', 'libx264',
             '-tune', 'stillimage', '-c:a', 'aac', '-b:v', str(video_bitrate), '-b:a', str(audio_bitrate), '-pix_fmt',
             'yuv420p', '-vf', 'crop=trunc(iw/2)*2:trunc(ih/2)*2', '-movflags', '+faststart', '-shortest', '-fflags',
             '+shortest', '-max_interleave_delta', '100M', title + '.mp4'], creationflags=CREATE_NO_WINDOW)

        # Stop the count
        count.stop()
        del count

    def clean_up(title):
        # Clean up, clean up. Everybody do your share.

        for filename in os.listdir(tracklist):
            if filename.endswith('.mp3'):
                os.remove(tracklist + '\\' + filename)

        if os.path.isfile("concat.txt"):
            os.remove("concat.txt")

        if os.path.isfile("big_audio.mp3"):
            os.remove("big_audio.mp3")

    def start_compiling():
        # Grab globals
        global current_playlist
        global current_title
        global current_thumbnail
        global currently_rendering
        global generate_timestamps
        global ignore_playlist
        global ip_type

        currently_rendering = True

        # Initialize new variables so the user may play with the variables while rendering
        this_playlist = current_playlist
        this_title = current_title
        this_thumbnail = current_thumbnail

        if not ignore_playlist:
            clean_up(this_title)

        # Deactivate UI
        start_button.config(state=tk.DISABLED)
        fileMenu.entryconfig("Settings", state=tk.DISABLED)

        # Run main functions
        clean_up(this_title)
        playlist_download(this_playlist, ip_type)
        if generate_timestamps:
            generate_tracklist()
        compile(this_thumbnail, this_title)
        time.sleep(5)
        clean_up(this_title)

        # Reactivate UI
        start_button.config(state=tk.NORMAL)
        fileMenu.entryconfig("Settings", state=tk.NORMAL)

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
    version_label = tk.Label(root, text="Version Number: v0.1.7")
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

    # Menus
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    fileMenu = tk.Menu(menubar)

    def update_config(option, state, widget):
        global options_dict
        if widget == "check":
            options_dict[option] = bool(state.get())
        else:
            options_dict[option] = state.get()
        with open('config.yaml', 'w') as outfile:
            yaml.dump(options_dict, outfile, default_flow_style=False)
        print(options_dict)

    def main_screen():
        # Clean up
        for widget in root.pack_slaves():
            widget.forget()

        for widget in root.grid_slaves():
            widget.destroy()

        # New Window
        root.geometry("600x400")

        # New objects
        main_label.pack()
        title_entry_label.pack()
        title_entry.pack()
        playlist_entry_label.pack()
        playlist_entry.pack()
        thumbnail_button.pack()
        empty_label.pack()
        start_button.pack()

    def settings_screen():
        global options_dict
        # New Window
        root.geometry("600x600")

        # Clean up
        for widget in root.pack_slaves():
            widget.forget()

        # New objects
        settings_label = tk.Label(root, text="Compilation Settings", font=30, pady=20)
        settings_label.grid(row=0, column=2)
        l1 = tk.Label(root)
        l1.grid(row=1, column=0, pady=10)
        l2 = tk.Label(root, text="Keep playlist order")
        l2.grid(row=2, column=0)
        l3 = tk.Label(root, text="Generate timestamps (.txt)")
        l3.grid(row=2, column=2)
        l4 = tk.Label(root, text="Normalize all audio")
        l4.grid(row=2, column=4)
        l5 = tk.Label(root, text="Video bitrate")
        l5.grid(row=5, column=0)
        l6 = tk.Label(root, text="Audio bitrate")
        l6.grid(row=5, column=2)
        l7 = tk.Label(root, text="IPvX (Blank = Default)")
        l7.grid(row=5, column=4)

        chvar1 = tk.IntVar()
        chvar1.set(options_dict['keep_order'])
        ch1 = tk.Checkbutton(root, variable=chvar1)
        ch1.grid(row=3, column=0)
        ch1.config(command=partial(update_config, "keep_order", chvar1, "check"))

        chvar2 = tk.IntVar()
        chvar2.set(options_dict['generate_timestamps'])
        ch2 = tk.Checkbutton(root, variable=chvar2)
        ch2.grid(row=3, column=2)
        ch2.config(command=partial(update_config, "generate_timestamps", chvar2, "check"))

        chvar3 = tk.IntVar()
        chvar3.set(options_dict['normalize_audio'])
        ch3 = tk.Checkbutton(root, variable=chvar3)
        ch3.grid(row=3, column=4)
        ch3.config(command=partial(update_config, "normalize_audio", chvar3, "check"))

        l8 = tk.Label(root)
        l8.grid(row=4, column=0, pady=50)

        class Bitrate(tk.Entry):
            def __init__(self, option, master=None, **kwargs):
                self.var = tk.StringVar()
                self.option = option
                tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
                self.old_value = ''
                self.var.trace('w', self.check)
                self.get, self.set = self.var.get, self.var.set

            def check(self, *args):
                if self.get().isdigit() or self.get() == "":
                    # the current value is only digits; allow this
                    self.old_value = self.get()
                    update_config(self.option, self.var, "entry")
                else:
                    # there's non-digit characters in the input; reject this
                    self.set(self.old_value)

        # Video Bitrate
        lotfi1 = Bitrate("video_bitrate", root)
        lotfi1.var.set(options_dict['video_bitrate'])
        lotfi1.grid(row=6, column=0)

        # Audio Bitrate
        lotfi2 = Bitrate("audio_bitrate", root)
        lotfi2.var.set(options_dict['audio_bitrate'])
        lotfi2.grid(row=6, column=2)

        # IP Config Setting
        options = [
            "",
            "-4",
            "-6"
        ]
        clicked = tk.StringVar()
        clicked.set(options_dict['ip_type'])
        clicked.trace("w", lambda name, index, mode,: update_config("ip_type", clicked, "dropdown"))
        optnmenu = tk.OptionMenu(root, clicked, *options)
        optnmenu.grid(row=6, column=4)

        l9 = tk.Label(root)
        l9.grid(row=7, column=0, pady=50)



        root.columnconfigure(5, weight=0)
        root.columnconfigure(4, weight=1)
        root.columnconfigure(3, weight=1)
        root.columnconfigure(2, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)



        # Back Button
        back = tk.Button(root, text="Save and Return to Compiler", command=main_screen)
        back.grid(row=8, column=2)

    #More Menu stuffs
    menubar.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="Settings", command=settings_screen)

    begin_button = tk.Button(root, text="Begin", command=main_screen)
    info_label.pack()
    begin_button.pack()
    version_label.pack()
    root.mainloop()

    # Run the program
    root.mainloop()


t1 = threading.Thread(target=root_program)
t1.run()
