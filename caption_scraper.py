from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)  
driver.get("https://www.youtube.com/watch?v=nssOuD9EcVk&ab_channel=RunThat")
# driver.get("https://www.google.com")


caption_button = driver.find_element(By.CLASS_NAME, "ytp-subtitles-button")
# print(caption_button)
caption_button.click()
print("caption button clicked")

play_button = driver.find_element(By.CLASS_NAME, "ytp-large-play-button")

# This one is to handle the play button that can appear in case the video didn't start playing automatically
try:
    play_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ytp-large-play-button"))
    )
    play_button.click()
    print("play button clicked") 
except TimeoutException:
    print("The video started playing automatically.")

time.sleep(3) # to skip this caption at first: "caption button clicked play button clicked"

caption_container = driver.find_element(By.CLASS_NAME, "ytp-caption-window-container")
# print(caption_container)
while True:

    try:
        # Extract all caption lines
        caption_lines = caption_container.find_elements(By.CLASS_NAME, "caption-visual-line")
        if len(caption_lines):
            for line in caption_lines:
                # Extract text from each segment within a line
                text = line.text
                print(text) 
                # caption_lines = caption_container.find_elements(By.CLASS_NAME, "caption-visual-line")
        time.sleep(1.5)
    except:
        print('No caption found')
        # caption_container = driver.find_element(By.CLASS_NAME, "ytp-caption-window-container")
