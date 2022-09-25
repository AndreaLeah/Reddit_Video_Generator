import subprocess
import shlex
from moviepy.video.io.VideoFileClip import VideoFileClip
import cv2
import datetime
import os
import keys


class VidConfig:
    def __init__(self, index):
        self.vid = keys.vid

    def get_video_seconds(self, index):
        # Video Configuration
        data2 = cv2.VideoCapture(self.vid)

        # count the number of frames
        frames = float(data2.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = float(data2.get(cv2.CAP_PROP_FPS))
        # calculate duration of the video
        print(f'This is the frame count: {frames}')
        print(f'This is the fps: {fps}')
        seconds = float(frames / fps)
        video_time = str(datetime.timedelta(seconds=seconds))

        # calculate resolution of video
        height = data2.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = data2.get(cv2.CAP_PROP_FRAME_WIDTH)

        return seconds

    def remove_audio_in_videofile(self, index):
        # Remove any audio in the videofile
        videoclip = VideoFileClip(self.vid)
        new_clip = videoclip.without_audio()
        new_clip.write_videofile(f"{keys.reference_files_plus_index}orig_video.mp4")
        # os.remove(vid)

    def overlay_images_onto_video(self, p_tag_instance, index, audio_length, title_screenshot, p_tag):
        for item in range(0, p_tag_instance + 2):

            # Variable Declarations
            screenshot = f"{keys.new_folder_path_plus_index}ss{str(p_tag)}.png"
            video_input = f"{keys.new_folder_path}ReferenceFiles/final_video{str(p_tag)}.mp4"
            video_output = f"{keys.new_folder_path}ReferenceFiles/final_video{str(p_tag + 1)}.mp4"
            combined_video = f"{keys.new_folder_path}ReferenceFiles/rv{str(index)}combined_video.mp4"
            video_final_version = f"{keys.new_folder_path}ReferenceFiles/rv{str(index)}_final_audioless_video.mp4"

            p_tag2 = p_tag + 1
            z = audio_length[0] + 0.2
            a = sum(audio_length[0:p_tag]) + 0.2
            b = sum(audio_length[0:p_tag2]) + 0.2
            c = sum(audio_length[0:p_tag]) + 0.2
            d = sum(audio_length)

            # Title Overlay on Video
            if item == 0:
                p_tag = 0
                command = (f"ffmpeg -y -i {combined_video} -i {title_screenshot} -c:v libx264 -filter_complex \"[0:v][1:v] overlay=110:424:enable='between(t,0,{z})'\" -pix_fmt yuv420p -c:a aac -strict experimental {video_input}")
                subprocess.run(shlex.split(command))
                print(f'item == 0 if statement is not being skipped, the p_tag is: {p_tag}')
                print(a)
                print(b)

            # P_Tag Overlay on Video
            if 1 <= item < p_tag_instance:
                print(f'At the elif statement, before the video creation commences, the p_tag is: {p_tag}')
                command = (f"ffmpeg -y -i {video_input} -i {screenshot} -c:v libx264 -filter_complex \"[0:v][1:v] overlay=110:424:enable='between(t,{a},{b})'\" -pix_fmt yuv420p -c:a aac -strict experimental {video_output}")
                subprocess.run(shlex.split(command))
                os.remove(video_input)

            # Last P_Tag Overlay on Video
            if item == p_tag_instance:
                command = (f"ffmpeg -y -i {video_input} -i {screenshot} -c:v libx264 -filter_complex \"[0:v][1:v] overlay=110:424:enable='between(t,{c},{d})'\" -pix_fmt yuv420p -c:a aac -strict experimental {video_final_version}")
                subprocess.run(shlex.split(command))
                os.remove(video_input)

            print(f'end of for loop has been reached, p_tag is {p_tag} right before we are adding 1 to it')
            print(f'this is the total of the p_tag_instance: {p_tag_instance}')
            p_tag += 1

    def combine_audio_and_video_files(self, new_folder_path, index):
        # Combine video & audio combined files together
        # https://stackoverflow.com/questions/61831571/video-editing-in-python-combining-a-mp3-and-mp4-file-in-python-using-mhmovie
        video_final_version = f"{new_folder_path}ReferenceFiles/rv{str(index)}_final_audioless_video.mp4"
        combined_audio = f"{new_folder_path}ReferenceFiles/rv{str(index)}combined_audio.wav"
        combined_video = new_folder_path + 'ReferenceFiles/' + 'rv' + str(index) + 'combined_video.mp4'
        finalized_output = f"{new_folder_path}rv{str(index)}video.mp4"

        # concatenate video and audio file
        subprocess.call(['ffmpeg', '-i', combined_audio, '-i', video_final_version, finalized_output])
