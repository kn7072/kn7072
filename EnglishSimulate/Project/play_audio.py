# coding="utf-8"
# import playsound
import pygame as pg


def play_sound(word, volume=0.8):
    """
    stream music with mixer.music module in a blocking manner
    this will stream the sound from disk while playing
    """
    path_file = 'audio/{word}.mp3'.format(word=word)
    # playsound.playsound('audio/{word}.mp3'.format(word=word), True)
    # set up the mixer
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 2048  # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    # volume value 0.0 to 1.0
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(path_file)
        print("Music file {} loaded!".format(path_file))
    except pg.error:
        print("File {} not found! ({})".format(path_file, pg.get_error()))
        return
    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


if __name__ == "__main__":
    play_sound("home")

