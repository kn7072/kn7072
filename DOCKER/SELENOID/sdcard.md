# Создать карту
https://developer.android.com/studio/command-line/mksdcard
https://blog.jayway.com/2009/04/22/working-with-sd-cards-in-the-android-emulator/
https://xjaphx.wordpress.com/2011/06/26/create-and-use-emulated-sd-card/

3. Browse SD Card
There are many ways to browse SD Card, however, I will just tell you two common ways:
a. In Eclipse, open DDMS Perspective, and open File Explorer view, you can browse /sdcard directory.
In this mode, you can drag and drop files.
b. Using commandline, go to adb shell by typing:
1 __adb -e shell__

Then access to /sdcard directory by typing:
# __cd /sdcard__

You can use push/pull from adb shell to put files into sdcard or get files from it.


__adb push /tmp/Download/IMG_2019_03_Disk_Autotest.jpg /sdcard/Download__
__fdisk -l sdcard.img__
