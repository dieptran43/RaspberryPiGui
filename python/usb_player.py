import os
from pygame import mixer
from print_handler import printer


skipped = False
previous = False
paused = False
volume = 1.0

print = printer

def start(directory):
    global paused
    global skipped
    global previous
    was_paused = False
    files = []
    for (dirpath, _, filenames) in os.walk(directory):
        for file in filenames:
            files.append(os.path.join(dirpath, file))
    i = 0
    for _ in files:
        if files[i].split('.')[-1].lower() not in ['mp3', 'waw', 'wma']:
            del files[i]
        else:
            i += 1
        print(f'Size: {len(files)}', 'USB', end='')
    
    mixer.init()
    i = 0
    fail_count = 0
    while i < len(files):
        try:
            if fail_count > 5:
                break
            item = files[i]
            i+=1
            print(f'Now playing {item}', 'USB')
            mixer.music.load(item)
            mixer.music.set_volume(volume)
            mixer.music.play()
            while True:
                if mixer.music.get_volume() != volume:
                    mixer.music.set_volume(volume)
                if not mixer.music.get_busy() and not paused:
                    break
                if skipped:
                    mixer.music.stop()
                    skipped = False
                if paused:
                    mixer.music.pause()
                    was_paused=True
                elif was_paused:
                    mixer.music.unpause()
                    was_paused=False
                if previous:
                    i -= 2
                    mixer.music.stop()
                    previous = False
                pass
            if fail_count != 0:
                fail_count = 0
        except Exception as ex:
            print('Exception occured during playback', 'USB')
            print(f'Exception: {ex}', 'USB')
            fail_count += 1

def pause(a=None):
    global paused
    paused = not paused

def skip(a=None):
    global skipped
    skipped = True

def set_volume(_volume):
    global volume
    volume = (float(_volume)/100)

def prev(a=None):
    global previous
    previous = True

if __name__=="__main__":
    def Player():
        start('../test/Test')
    import threading
    player = threading.Thread(target=Player)
    player.name = 'Player'
    player.start()
    while True:
        a = input('> ')
        if a == 'pause':
            pause()
        elif a == 'skip':
            skip()
        elif a == 'prev':
            prev()
        elif "volume" in a:
            set_volume(a.split(' ')[-1])
