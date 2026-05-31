[](https://mediaarea.net/ru/MediaInfo/Download/Ubuntu)
1 найти Ubuntu 20.04 (Focal Fossa) Linux Mint 20.x
2 скачать CLI v25.04 requires libmediainfo0 это зависимость для mediainfo - файл libmediainfo0v5_25.04-1_amd64.xUbuntu_20.04.deb
3 установить sudo dpkg -i libmediainfo0v5_25.04-1_amd64.xUbuntu_20.04.deb
4 скачать mediainfo_25.04-1_amd64.xUbuntu_20.04.deb
5 установить sudo dpkg -i mediainfo_25.04-1_amd64.xUbuntu_20.04.deb

mediainfo --fullscan /home/stepan/temp/test_video/english.mp4
mediainfo --Inform="Video;%Duration%" /home/stepan/temp/test_video/english.mp4

Use the following commands:

1. To get the duration of video stream:
   $ mediainfo --Inform="Video;%Duration%" [inputfile]

2. To get the duration of the media file:
   $ mediainfo --Inform="General;%Duration%" [inputfile]

3. To get the duration of audio stream only:
   $ mediainfo --Inform="Audio;%Duration%" [inputfile]

4. To get values of more than one parameter:
   $ mediainfo --Inform="Video;%Width%,%Height%,%BitRate%,%FrameRate%" [inputfile]

mediainfo --Output="Video;%Duration%\n" *.mp4 | awk '{ sum += $1 } END { secs=sum/1000; h=int(secs/3600);m=int((secs-h*3600)/60);s=int(secs-h*3600-m*60); printf("%02d:%02d:%02d\n",h,m,s) }'

## ffmpeg

### install

sudo apt install ffmpeg

### commands

создает файл jpg с нарезкой из кадров [How to Create Thumbnail Sheets for Your Videos in Linux](https://www.maketecheasier.com/create-thumbnail-sheets-for-videos-linux/)
ffmpeg -ss 3 -i "/path/to/video/file.mp4" -frames 5 -vf "select=not(mod(n\,3000)),scale=320:240,tile=4x3" -vsync vfr -q:v 10 image-sheet-filename\_%03d.jpg

    -ss defines a time offset from the beginning of the video file. Most videos start with a title sequence, and in most cases it’s not useful having a thumbnail of that. With this switch, we instruct FFMPEG to ignore “X” seconds from the beginning of the video to skip its probably not-so-exciting introduction.
    -i sets the input file from which FFMPEG will pull its thumbnails.
    -frames defines the number of frames that will be recorded.
    -q:v sets the compression quality of the produced image files.

As for the most interesting but also complicated part of this command, we will have to expand a bit on it since it does three things at once. We are talking about this:

-vf "select=not(mod(n\,3000)),scale=320:240,tile=4x3"

The -vf at the beginning instructs FFMPEG to use a video filter. Select=not(mod(n\,3000)) is responsible for the selected frames in the final images. It divides the current frame’s number (“n”) with the provided number (“3000”). Has the video reached frame 3001? If we divide 3001 with the number 3000, we get 1, so this frame will be the first in the first produced image sheet. Have we reached frame 6001? Since 6001/3000 gives us 2, this will be the second frame, and so on. Thus, by reducing this number, you increase the frequency of frame selection and vice-versa.
With the scale=320:240 part, we set the dimensions of each thumbnail in the final thumbnail sheet. For best results, this should be a fraction of the original video’s resolution, taking into account its aspect ratio.
Finally, the tile=4x3 part of the command defines how the thumbnails will be arranged in each sheet.

1. Получить информацию медиа файла
   ffmpeg -i file_name

Хотя эта команда полезна, она отображает слишком много информации, которая не относится к
вашему файлу (информация о ffmpeg). Чтобы пропустить это, добавьте флаг -hide_banner:
ffmpeg -i video_file.mp4 -hide_banner
