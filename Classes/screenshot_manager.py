import PIL.Image
from PIL import ImageDraw, ImageFont
from matplotlib import pyplot as plt
from selenium.common import NoSuchElementException
import keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import io
import functions.functions as f
import os

new_folder_path = keys.new_folder_path
index = keys.index

class Screenshot:

    def __init__(self):
        pass

    def firefox_webdriver(self):
        self.firefox_profile_path = keys.firefox_profile_path
        self.fp = webdriver.FirefoxProfile(self.firefox_profile_path)
        self.fp.set_preference('layout.css.devPixelsPerPx', '3.0')
        self.fox = webdriver.Firefox(self.fp)
        self.fox.set_window_position(0, 0)
        self.fox.set_window_size(470, 2000)
        self.fox.get(keys.url)
        time.sleep(3)

    def get_screenshots(self, p_tag_instance):

        self.firefox_webdriver()

        try:
            titlename = self.fox.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[3]').screenshot_as_png
            imageStream = io.BytesIO(titlename)
            t = PIL.Image.open(imageStream)

        except AttributeError:
            titlename = self.fox.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[3]').screenshot_as_png
            print(type(titlename))
            imageStream = io.BytesIO(titlename)
            t = PIL.Image.open(imageStream)

        # Add margin to Title Image
        t_new = f.add_margin(t, 10, 35, 26, 35, (26, 26, 26))
        base_width = 1242
        width_percent = (base_width / float(t_new.size[0]))
        hsize = int((float(t_new.size[1]) * float(width_percent)))
        t_new = t_new.resize((base_width, hsize), PIL.Image.ANTIALIAS)

        # Put logo area on top of title
        logo = PIL.Image.open(keys.a_top_png)
        # creating a new image and pasting the top.png on top of title (rv0ss_title)
        img3 = PIL.Image.new("RGB", (logo.width, logo.height + t_new.height))
        # pasting the awards (image_name,(position))
        img3.paste(logo, (0, 0))
        # pasting the title (image_name,(position))
        img3.paste(t_new, (0, logo.height))
        img3 = f.add_margin(img3, 25, 0, 0, 0, (26, 26, 26))
        plt.imshow(img3)

        # check for archived and locked icons, paste them if present
        try:
            archived = self.fox.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/i[1]')
        except NoSuchElementException:
            archived = None

        try:
            locked = self.fox.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/i[2]')
        except NoSuchElementException:
            locked = None

        icon1 = PIL.Image.open(keys.archive_png)
        icon2 = PIL.Image.open(keys.lock_png)

        if archived is not None and locked is not None:
            # Paste Icon1 on top of final pic
            plt.imshow(img3)
            img3.paste(icon1, (1088, 72))
            # Paste Icon2 on top of final pic
            plt.imshow(img3)
            img3.paste(icon2, (1142, 70))
        if archived is not None and locked is None:
            plt.imshow(img3)
            img3.paste(icon1, (1142, 70))
        if archived is None and locked is not None:
            plt.imshow(img3)
            img3.paste(icon2, (1142, 70))

        # Save Edited Image
        dir_path = keys.new_folder_path
        file_path = os.path.join(dir_path, keys.name_formatted)
        img3.save(file_path)

        # Format upper part of reddit title post. (awards, username, etc)
        # get XPath of the replaceable variables
        username = self.fox.find_element(By.XPATH,
                                    value='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/div/div/a')
        username = username.text

        date = self.fox.find_element(By.XPATH,
                                value='/ html / body / div[1] / div / div[2] / div[2] / div / div / div / div[2] / div[3] / div[1] / div[2] / div[1] / div / div[2] / div / div[1] / span[2]')
        date = date.text

        # Open Title Image
        img = PIL.Image.open(f"{keys.new_folder_path}rv{str(index)}ss_title.png")

        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(im=img)
        # Custom font style and font size
        myFont1 = ImageFont.truetype(font=keys.sf_pro_font, size=37)
        myFont2 = ImageFont.truetype(font=keys.arial_mtsdt_font, size=37)
        myFont3 = ImageFont.truetype(font=keys.arial_mtsdt_font, size=28)

        # Add Text to an image
        I1.text(xy=(160, 55), text="r/", font=myFont1, fill='rgb(139, 139, 139)')
        I1.text(xy=(185, 63), text="AmItheAsshole", font=myFont2, fill='rgb(139, 139, 139)')
        I1.text(xy=(159, 102), text=username, font=myFont1, fill='rgb(0, 119, 214)')
        # create bounding box to be able to measure length of x for the variable username string
        bbox = I1.textbbox((159, 102), username, font=myFont1)
        print(bbox)
        x_end = bbox[2]
        x = x_end + 14
        # x is the position of the next string relative to the variable previous string.
        I1.text(xy=(x, 116), text="•", font=myFont3, fill='rgb(139, 139, 139)')
        bbox = I1.textbbox((x, 102), "•", font=myFont3)
        print(bbox)
        x_end = bbox[2]
        x = x_end + 14
        I1.text(xy=(x, 102), text=date, font=myFont1, fill='rgb(139, 139, 139)')
        # proportionally resize width for video editing
        base_width = 860
        width_percent = (base_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((base_width, hsize), PIL.Image.ANTIALIAS)
        # Save the edited image
        img.save(f"{keys.new_folder_path}rv{str(index)}ss_title.png")

        p_tag = 1

        # individual P tag screenshots: P1
        self.fox.set_window_position(0, 0)
        self.fox.set_window_size(450, 2000)
        # Implicitly wait 20 seconds before continuing onto the next portion
        self.fox.implicitly_wait(20)

        # P tag screenshot XPath
        try:
            image = self.fox.find_element(By.XPATH,
                                     value='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[5]/div/p[' + str(p_tag) + ']').screenshot_as_png
        except NoSuchElementException:
            image = self.fox.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[4]/div/p[' + str(p_tag) + ']').screenshot_as_png

        imageStream = io.BytesIO(image)
        im = PIL.Image.open(imageStream)

        # Add margin to first p_tag of the page
        im_new = f.add_margin(im, 30, 0, 10, 35, (26, 26, 26))

        # proportionally resize width for video editing
        base_width = 860
        width_percent = (base_width / float(im_new.size[0]))
        hsize = int((float(im_new.size[1]) * float(width_percent)))
        im_new = im_new.resize((base_width, hsize), PIL.Image.ANTIALIAS)

        # Save the edited image
        dir_path = keys.new_folder_path
        name_formatted = f"rv{str(index)}ss{str(p_tag)}.png"
        file_path = os.path.join(dir_path, name_formatted)
        im_new.save(file_path)
        time.sleep(2)
        p_tag += 1

        for item in range(1, p_tag_instance):
            try:
                image = self.fox.find_element(By.XPATH,
                                         value='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[5]/div/p[' + str(
                                             p_tag) + ']').screenshot_as_png
            except NoSuchElementException:
                image = self.fox.find_element(By.XPATH,
                                         value='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[4]/div/p[' + str(
                                             p_tag) + ']').screenshot_as_png
            imageStream = io.BytesIO(image)
            im = PIL.Image.open(imageStream)
            w, h = im.size
            cropped_im = im.crop((0, 10, w, h))
            # original code had im_new = f.add_margin(cropped_im, 0, 20, 10, 25, (26, 26, 26)), p_tags > 1 don't have enough margin at top
            im_new = f.add_margin(cropped_im, 5, 30, 10, 35, (26, 26, 26))
            # proportionally resize width for video editing
            base_width = 860
            width_percent = (base_width / float(im_new.size[0]))
            hsize = int((float(im_new.size[1]) * float(width_percent)))
            im_new = im_new.resize((base_width, hsize), PIL.Image.ANTIALIAS)
            dir_path = new_folder_path
            # Save edited image
            name_formatted = f"rv{str(index)}ss{str(p_tag)}.png"
            file_path = os.path.join(dir_path, name_formatted)
            im_new.save(file_path)
            time.sleep(2)
            p_tag += 1

        #  Close Firefox App
        self.fox.quit()
