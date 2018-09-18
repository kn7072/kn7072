# coding="utf-8"
import playsound


def play_sound(word):
    playsound.playsound('audio/{word}.mp3'.format(word=word), True)

