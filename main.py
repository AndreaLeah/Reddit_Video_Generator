from lib.lib import *

def program_loop(url):

    # Variable Declaration
    index = keys.index

    for iteration in range(1):

        # Tracker Variables
        p_tag = 1
        p_tag_instance = 1

        # create indexed file folder within Reddit_Videos Folder
        os.mkdir(new_folder_path)

        # create videos folder within R_V indexed folder
        os.mkdir(video_folder_path)

        # Create reference file folder
        os.mkdir(reference_files_folder)

        # Instantiate HTML Parser Object
        parser = HTMLParser()

        # Parse the Reddit Website Title
        html = requests.get(url, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })
        htmlParse = BeautifulSoup(html.content, "html.parser")
        para_str = parser.parse_url_title()
        print(f'This is the para_str after para.text: {para_str}')

        # Title Keyword Conversion: AITA -> Am I the Asshole, etc
        para_str = f.keyword_conversion(para_str)

        # Instantiate Amazon Polly Class Object
        polly = AMZPOLLY()

        # Get TTS Audio from Title Text
        polly.request_title_speech_synthesis(para_str, index)

        # Find Number of P Tags on Page (p_tag_instance)
        p_tag_instance = parser.find_p_tag_instance(p_tag_instance)

        p_tag_instance = p_tag_instance - 4

        # Iterate through all the p tags on the page, create mp3 & keyword conversion
        for item in range(0, p_tag_instance):
            para_str = parser.parse_p_tag(p_tag)

            p_tag_str = f"p{str(p_tag)}"

            # Keyword Conversion
            f.keyword_conversion(para_str)
            print(f"Paragraph {p_tag} keyword conversion complete")

            polly.request_p_tag_speech_synthesis(para_str, index, p_tag_str)

            p_tag += 1

        # TITLE SCREENSHOT

        # Instantiate Screenshot Class
        screenshot = Screenshot()

        # Get Screenshots of all Elements
        screenshot.get_screenshots(p_tag_instance)

        # Video Configuration & Get Video Seconds
        vid_config = VidConfig(index)
        seconds = vid_config.get_video_seconds(index)

        # Remove Audio in Videofile
        vid_config.remove_audio_in_videofile(index)

        # Get length (in seconds) of title each p_tag audio
        audio_length = []
        # Get Audio Length of Title
        title_length = librosa.get_duration(filename=keys.wav_title_file2)
        print(title_length)
        # Append Title length to empty audio_length list
        audio_length.append(title_length)

        #Get Each p_tag Length
        p_tag = 1
        for audiofile in range(0, p_tag_instance):
            wav_file2 = f"{new_folder_path}rv{str(index)}p{str(p_tag)}cs.wav"
            p_tag_length = librosa.get_duration(filename=wav_file2)
            audio_length.append(p_tag_length)
            p_tag += 1

        audio_sum = sum(audio_length)
        seconds = float(seconds + 0.0)
        seconds_of_video = 0.00
        video_iteration = 0
        keep_iterating_video_count = True
        extra_video_iteration = 0
        subclip_seconds = 0

        while keep_iterating_video_count == True:
            # if video second amount < total audio second amount (title + all p_tags)
            if seconds_of_video < audio_sum:
                seconds_of_video = seconds_of_video + seconds
                if seconds_of_video < audio_sum:
                        video_iteration += 1
            if seconds_of_video == audio_sum:
                extra_video_iteration = 0
            if seconds_of_video > audio_sum:
                video_remainder = seconds_of_video - audio_sum
                subclip_seconds = seconds - video_remainder
                extra_video_iteration = 1
                keep_iterating_video_count = False

        # Resize original video to 1080x1920
        # output_urlvideo is the regular playback, resized video
        subprocess.call(['ffmpeg', '-i', keys.urlvideo1, '-vf', 'crop=1080:1920:0:0', '-preset', 'slow', '-crf', '18', keys.output_urlvideo])

        # Reverse and resize video to 1080x1920
        # keys.urlvideo_rev is the reversed playback, resized video
        subprocess.call(['ffmpeg', '-i', keys.output_urlvideo, '-vf', 'crop=1080:1920:0:0', '-preset', 'slow', '-crf', '18', '-vf', 'reverse', keys.urlvideo_rev])

        video_iteration2 = 0
        write_videofile_destination = f"{new_folder_path}Videos/rv{str(index)}vid{str(video_iteration2)}.mp4"

        # Generate & save videos for each video iteration & the subclip video, if applicable
        for iteration in range(0, video_iteration):
            # Note that even and odd are reversed here for the playback since the range number starts at 0, and even number, instead of 1, an odd number
            # Even numbers are normal playback
            if iteration % 2 != 0:
                video_iteration2 += 1
                even_clip = VideoFileClip(keys.urlvideo_rev)
                even_clip.write_videofile(write_videofile_destination)
            # Odd numbers are reverse speed playback
            if iteration % 2 == 0:
                video_iteration2 += 1
                odd_clip = VideoFileClip(keys.output_urlvideo)
                odd_clip.write_videofile(write_videofile_destination)
        if extra_video_iteration == 1:
            #get subclip
            video_iteration2 += 1
            # Normal playback speed
            if video_iteration2 % 2 != 0:
                subclip = VideoFileClip(keys.output_urlvideo)
                subclip = subclip.subclip(0, subclip_seconds)
                subclip.write_videofile(write_videofile_destination)
            # Reverse playback speed
            if video_iteration2 % 2 == 0:
                subclip = VideoFileClip(keys.urlvideo_rev)
                subclip = subclip.subclip(0, subclip_seconds)
                subclip.write_videofile(write_videofile_destination)

        total_videos = video_iteration + extra_video_iteration

        L = []
        # Get all videos created & concatenate them (literally multiple files to concatenate)
        for root, dirs, files in os.walk(keys.video_folder_path):
            # files.sort(): video files
            files = natsorted(files)
            for file in files:
                if os.path.splitext(file)[1] == '.mp4':
                    file_path = os.path.join(root, file)
                    video = VideoFileClip(file_path)
                    L.append(video)

        final_clip = concatenate_videoclips(L)
        final_clip.write_videofile(f"{keys.reference_files_plus_index}combined_video.mp4", fps=29.97, remove_temp=False)

        # Delete all of the individual video files after they are combined by Deleting the Videos Folder
        shutil.rmtree(keys.video_folder_path)

        # Combine all wav files in folder
        A = []
        for root, dirs, files in os.walk(keys.new_folder_path):
            # files.sort(): audio files
            files = natsorted(files)
            for file in files:
                if os.path.splitext(file)[1] == '.wav':
                    file_path = os.path.join(root, file)
                    audio = AudioFileClip(file_path)
                    A.append(audio)
        final_clip = concatenate_audioclips(A)
        final_clip.write_audiofile(f"{keys.reference_files_plus_index}combined_audio.wav")

        # Need to keep this p_tag above the screenshot variable
        p_tag = 1
        title_screenshot = f"{keys.new_folder_path_plus_index}ss_title.png"
        print(type(audio_length[1]))
        print(audio_length[1])

        os.chdir(keys.new_folder_path)
        print(os.listdir())

        # Overlay Images Onto Video
        vid_config.overlay_images_onto_video(p_tag_instance, index, audio_length, title_screenshot, p_tag)

        # Combine Audio and Video Files
        vid_config.combine_audio_and_video_files(new_folder_path, index)

        index += 1

program_loop(keys.url)
