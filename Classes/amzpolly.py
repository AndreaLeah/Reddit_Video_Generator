import sys
from contextlib import closing
import boto3
import ffmpy
from botocore.exceptions import BotoCoreError, ClientError
import os
import subprocess
from pydub import AudioSegment
import keys


# I had to list region_name argument & provide a parameter
# https://docs.aws.amazon.com/general/latest/gr/pol.html
# https://stackoverflow.com/questions/67752721/botocore-exceptions-noregionerror-you-must-specify-a-region-when-deploying-t


class AMZPOLLY:
    def __int__(self):
        pass

    def request_title_speech_synthesis(self, para_str, index):
        # Variables
        rv_str_index = f'rv{str(index)}'

        # set client API as polly services
        self.polly = boto3.client('polly')

        try:
            # Request speech synthesis
            response = self.polly.synthesize_speech(
                Text=para_str,
                OutputFormat='mp3',
                VoiceId='Matthew',
            )
            print("Title MP3 file Generated")
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(keys.new_folder_path, f"{rv_str_index}p_title.mp3")
                print("Indexed folder created in Reddit_Videos Folder")
                try:
                    # Change audiofile type from mp3 to wav
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                        print("Title mp3 file written to indexed rv folder")

                        # Convert mp3 to wav
                        dst = f"{keys.new_folder_path}{rv_str_index}p_title.wav"
                        subprocess.call(['ffmpeg', '-i', output,
                                         dst])
                        # remove/delete mp3 file after wav conversion complete
                        os.remove(f"{keys.new_folder_path}{rv_str_index}p_title.mp3")

                        # Change speed of audiofile wav without changing pitch
                        wav_title_file = f"{keys.new_folder_path}{rv_str_index}p_title.wav"
                        wav_title_file2 = f"{keys.new_folder_path}{rv_str_index}c_title.wav"

                        ff = ffmpy.FFmpeg(inputs={wav_title_file: None}, outputs={wav_title_file2: ["-filter:a", "atempo=1.2"]})
                        ff.run()
                        os.remove(wav_title_file)

                        # Add .2  seconds of silence to the beginning of each title audiofile
                        audio_in_file = f"{keys.new_folder_path}{rv_str_index}c_title.wav"
                        audio_out_file = f"{keys.new_folder_path}{rv_str_index}cs_title.wav"

                        # create 1 sec of silence audio segment
                        one_sec_segment = AudioSegment.silent(duration=200)  # duration in milliseconds
                        # read wav file to an audio segment
                        song = AudioSegment.from_wav(audio_in_file)
                        # Add above two audio segments
                        final_song = one_sec_segment + song
                        # Save modified audio
                        final_song.export(audio_out_file, format="wav")
                        os.remove(audio_in_file)

                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

    def request_p_tag_speech_synthesis(self, para_str, index, p_tag_str):
        # set client API as polly services
        self.polly = boto3.client('polly')

        # Variables
        rv_str_index = f'rv{str(index)}'
        editing_file_path = f"{keys.new_folder_path}{rv_str_index}{p_tag_str}"

        try:
            # Request speech synthesis
            response = self.polly.synthesize_speech(Text=para_str, OutputFormat='mp3', VoiceId='Matthew')
            print("<p> mp3 file generated")
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)
        # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(
                    keys.new_folder_path, f"{rv_str_index}p_title.mp3")

                try:
                    # Change p_tag audiofile type from mp3 to wav
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                        print("<p> mp3 file written to chosen folder (rv indexed folder)")
                        # Convert mp3 to wav
                        dst = f"{keys.new_folder_path}{rv_str_index}p_title.wav"
                        # convert mp3 to wav
                        subprocess.call(['ffmpeg', '-i', output,
                                         dst])
                        print('Mp3 to wav conversion complete')
                        # remove/delete mp3 file after wav conversion complete
                        os.remove(output)

                        # Speed up audiofile without changing pitch
                        # https://stackoverflow.com/questions/45441557/how-to-change-speed-of-a-wav-file-while-retaining-the-sampling-frequency-in-pyth
                        wav_file = dst
                        wav_file2 = f"{editing_file_path}c.wav"
                        ff = ffmpy.FFmpeg(inputs={wav_file: None}, outputs={wav_file2: ["-filter:a", "atempo=1.2"]})
                        ff.run()
                        os.remove(wav_file)

                        # Adds .4 seconds to the beginning of each p_tag audio & saves it
                        # https://stackoverflow.com/questions/46757852/adding-silent-frame-to-wav-file-using-python
                        # This needs changed from 'changed.wav' to 'c.wav'
                        audio_in_file = wav_file2
                        audio_out_file = f"{editing_file_path}cs.wav"
                        # create .4 sec of silence audio segment
                        one_sec_segment = AudioSegment.silent(duration=400)  # duration in milliseconds
                        # read wav file to an audio segment
                        song = AudioSegment.from_wav(audio_in_file)
                        # Add above two audio segments
                        final_song = one_sec_segment + song
                        # Either save modified audio
                        final_song.export(audio_out_file, format="wav")
                        os.remove(audio_in_file)

                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)
        print("This is the end of the iteration")
