import subprocess
from subprocess import CREATE_NO_WINDOW, PIPE
import os


def playlist_download(window, link, audio_bitrate, ip):
    # Start the count
    window.progress.setFormat("Downloading playlist: %p%")
    p = subprocess.Popen(['youtube-dlp', ip, '--format', 'bestaudio', '-o',
                          os.getcwd() + '\\tracklist\\%(playlist_index)s-%(title)s.%(ext)s', '-x',
                          '--extract-audio',
                          '--audio-format', 'mp3', '--audio-quality', str(audio_bitrate), '-ciw', link],
                         stdin=PIPE, stderr=PIPE, stdout=PIPE, creationflags=CREATE_NO_WINDOW)

    # Progress Bar
    for line in p.stdout:
        print(line)
        string_line = str(line)
        if string_line.startswith('b\'[download] Downloading video'):
            numbers = string_line[string_line.index('video') + 6:len(string_line) - 3]
            current_download = int(numbers[:numbers.index('of') - 1])
            tracklist_size = int(numbers[numbers.index('of') + 3:])
            window.progress.setMaximum(tracklist_size)
            window.progress.setValue(current_download)
    # for line in p.stderr:
    #     print(line)
    #     string_line = str(line)
    #     if string_line.startswith("b\'ERROR: Unable to download webpage: "):
    #         return
