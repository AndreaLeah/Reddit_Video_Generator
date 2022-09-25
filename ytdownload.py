from pytube import YouTube
import subprocess
import time
import cv2
import os

import keys

# # # https://www.geeksforgeeks.org/pytube-python-library-download-youtube-videos/
#
#Where to save
SAVE_PATH = keys.SAVE_PATH
# Change link for new video
link = keys.link
video = keys.video
orig_video_filepath = keys.orig_video_filepath
full_video_filepath = keys.full_video_filepath


def resize_video():
    # https://stackoverflow.com/questions/7348505/get-dimensions-of-a-video-file
    vid = cv2.VideoCapture(orig_video_filepath)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

    print(width, height)

    if width < 1080 or height < 1920:
        # https://ottverse.com/change-resolution-resize-scale-video-using-ffmpeg/
        subprocess.call(['ffmpeg', '-i', orig_video_filepath, '-vf', 'scale=1080:1920', '-preset', 'slow', '-crf', '18', full_video_filepath])


def download_yt_video():
    yt = YouTube(link)

    # filters out all the files with "mp4" extension
    mp4files = yt.streams.filter(file_extension='mp4')
    # Selecting the stream by itag, 299 in this case is 1080p
    stream = yt.streams.get_by_itag(299)

    print(mp4files)

    # downloading the video
    stream.download(output_path=SAVE_PATH, filename=video)
    time.sleep(10)


download_yt_video()
resize_video()
# Delete original Yt video download
os.remove(orig_video_filepath)

