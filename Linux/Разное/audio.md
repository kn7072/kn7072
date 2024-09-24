$ aplay -l
amixer controls

Мне потребовалось три дня, чтобы узнать, как использовать его на Raspberry Pi. Я создал команду оболочки. Если вы хотите использовать звук через разъем 3,5 мм, просто напишите. Вы можете подключить кабель HDMI.

sudo bash -c 'echo -e " defaults.pcm.card 1 \ndefaults.ctl.card 1" > /etc/asound.conf'
если вы хотите использовать аудиовыход HDMI, просто измените число 1 на 0.

sudo bash -c 'echo -e " defaults.pcm.card 0 \ndefaults.ctl.card 0" > /etc/asound.conf'




https://www.raspberrypi.com/news/latest-raspberry-pi-os-update-may-2020/



https://debianforum.ru/index.php?topic=8249.0
УРА!!!!!!!! работает! сделал так:
cat /proc/asound/cards
 0 [Intel          ]: HDA-Intel - HDA Intel
                      HDA Intel at 0xf7e14000 irq 45
 1 [PCH            ]: HDA-Intel - HDA Intel PCH
                      HDA Intel PCH at 0xf7e10000 irq 45
 2 [Generic        ]: HDA-Intel - HD-Audio Generic
                      HD-Audio Generic at 0xf7d40000 irq 46
далее зашол в /usr/share/alsa/alsa.conf
# defaults

 defaults.ctl.card 0
 defaults.pcm.card 0

и поменял 0 на 1) и все заработало!!!!

Всем спасибо! как то так!)


https://redos.red-soft.ru/base/arm/sound-redos/pulseaudio/?ysclid=lrwankdago829005002

pactl set-sink-volume <имя_устройства_вывода> <уровень_громкости>

Стоит отметить, что уровень громкости вводится от 0 до 65535 (от 0% до 100%). Если попытаться выставить громкость больше, чем на 65535, то звук будет выводится с усилением (и будет указываться больше, чем 100%). Слишком большое усиление может искажать звук.


alsa_output.usb-Logitech_Logitech_USB_Headset_000000000000-00.analog-stereo
bluez_sink.41_42_81_08_D9_83.a2dp_sink

pactl set-sink-volume  bluez_sink.74_45_CE_15_F4_BB.a2dp_sink 15535


Приостановка звука
Источник звука можно заглушить командой вида:

pactl suspend-sink bluez_sink.74_45_CE_15_F4_BB.a2dp_sink true  -выключит звук


Громкость звука в приложениях
pactl list sink-inputs

Для определения номера выхода источника команда будет выглядеть следующим образом:
pactl list source-outputs

pactl move-sink-input <номер_входа_аудиоприёмника> <имя_источника>

pactl move-sink-input 25 alsa_output.usb-Logitech_Logitech_USB_Headset_000000000000-00.analog-stereo
pactl move-sink-input 25 bluez_sink.74_45_CE_15_F4_BB.a2dp_sink



https://askubuntu.com/questions/78174/play-sound-through-two-or-more-outputs-devices
pactl load-module module-combine-sink


pactl load-module module-combine-sink sink_name=combination-sink sink_properties=device.description=myCombinationSink slaves=bluez_sink.41_42_81_08_D9_83.a2dp_sink,bluez_sink.74_45_CE_15_F4_BB.a2dp_sink channels=2
