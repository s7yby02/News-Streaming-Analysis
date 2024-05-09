from selenium.webdriver.common.by import By
import time
from functions import *

# Getting the chrome driver
driver = getDriver()

# Going to the link
# link = "https://www.youtube.com/watch?v=gCNeDWCI0vo&ab_channel=AlJazeeraEnglish"
link = "https://www.youtube.com/watch?v=YDfiTGGPYCk&ab_channel=LiveNOWfromFOX"
goToLink(link, driver)

playButton()

# Finding the captions container
caption_container = getCaptionsContainer(driver)
print("Caption container Found!!")


last_text="."
while True:

    try:
        # Extract all caption lines
        caption_lines = caption_container.find_elements(By.CLASS_NAME, "caption-visual-line")
        if len(caption_lines):
            for line in caption_lines:
                # print(line)
                # Extract text from each segment within a line
                text = line.text
                if text != last_text:
                    print(text)
                    last_text=text
        time.sleep(1.5)
    except:
        print('No caption found')
