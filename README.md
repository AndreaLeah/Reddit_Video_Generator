# **This is a python script to fully automate video creation using Reddit posts.**


**Basic Overview:**
This fully automates screenshots (Selenium Webdriver, Firefox), text to speech conversion (Amazon Polly), and video generation (ffmpeg) for reddit posts. A ytdownload.py file has been included if you would like to source and download your video from eligible YouTube videos. It is set to choose 1080p, and to resize the video to 1080x1920 resolution.


### **Steps:**
1. Create a keys.py file
2. Keys.py file should include the following variables:

    **ytdownload.py Variables:**  
    link = 'YouTube video link you'd like to download and resize'
    video = "the name you'd like to save the downloaded video as"
    orig_video_filepath = "absolute path of video variable"
    full_video_filepath = "absolute path for resized variable to go, with name extension included"

    **main.py Variables:**  
    url = 'url of Reddit Post'
    vid = 'local video file to use for video background' (Make sure the video is of a minimum resolution of 1080x1920 before starting)
    firefox_profile_path = 'FireFox Profile absolute file path that you wish to use for the Selenium Webdriver screenshots'
    amazon_post_url = '/v1/speech HTTP/1.1'
    index = 0 
    SAVE_PATH = '/Users/<your name>/Documents/Reddit_Videos/'
    new_folder_path = f"/Users/<your name>/Documents/Reddit_Videos/rv{str(index)}/"
    video_folder_path = f"{new_folder_path}Videos/"
    reference_files_folder = f"{new_folder_path}ReferenceFiles/"

    name_formatted = f"rv{str(index)}ss_title.png" # this is the title screenshot

    wav_title_file2 = f"{new_folder_path}rv{str(index)}cs_title.wav" # another title screenshot edit along the pathway
    urlvideo1 = f"{new_folder_path}ReferenceFiles/rv{str(index)}orig_video.mp4"
    output_urlvideo = f"{new_folder_path}ReferenceFiles/rv{str(index)}resized_video.mp4"
    urlvideo_rev = f"{new_folder_path}ReferenceFiles/rv{str(index)}resized_reversed_video.mp4"
    reference_files_plus_index = f"{new_folder_path}ReferenceFiles/rv{str(index)}"
    new_folder_path_plus_index = f"{new_folder_path}rv{str(index)}"
    
    **The following items are not included in the files:**  
    sf_pro_font = '/Users/<your name>/Documents/Reddit_Video_Generator/Fonts/<insert font here>'
    arial_mtsdt_font = '/Users/<your name>/Documents/Reddit_Video_Generator/Fonts/<insert font here>'
    SFProTextReg = '/Users/<your name>/Library/Fonts/<insert font here>'
    a_top_png = '/Users/<your name>/Documents/Reddit_Video_Generator/Screenshot_Files/atop1.png' # subreddit logo circle and black area
    archive_png = '/Users/<your name>/Documents/Reddit_Video_Generator/Screenshot_Files/archive.png' # archive icon
    lock_png = '/Users/<your name>/Documents/Reddit_Video_Generator/Screenshot_Files/lock.png' # lock icon
    
3. Download requirements.txt file.





