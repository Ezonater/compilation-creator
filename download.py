import subprocess
from subprocess import CREATE_NO_WINDOW, PIPE
def playlist_download(link, audio_bitrate, ip):
        # Start the count
        
        p = subprocess.Popen(['youtube-dlc', ip, '--format', 'bestaudio', '-o',
                              os.getcwd() + '\\tracklist\\%(playlist_index)s-%(title)s.%(ext)s', '-x',
                              '--extract-audio',
                              '--audio-format', 'mp3', '--audio-quality', str(audio_bitrate), '-ciw', link],
                             stdin=PIPE, stderr=PIPE, stdout=PIPE, creationflags=CREATE_NO_WINDOW)

        # Progress Bar
        global tracklist_size
        tracklist_size = 0
        current_download = 0
        for line in p.stdout:
            print(line)
            string_line = str(line)
            if string_line.startswith('b\'[download] Downloading video'):
                numbers = string_line[string_line.index('video') + 6:len(string_line) - 3]
                current_download = int(numbers[:numbers.index('of') - 1])
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