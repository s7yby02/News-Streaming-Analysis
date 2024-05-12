from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from kafka import KafkaProducer

def getDriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options) 
    return driver

def goToLink(link:str, driver: webdriver.Chrome) -> None:
    driver.get(link)

def playButton(driver: webdriver.Chrome) -> None:
    """
    This one is to handle the play button that can appear in case the video didn't start playing automatically
    """
    try:
        play_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ytp-large-play-button"))
        )
        play_button.click()
        print("play button clicked") 
    except TimeoutException:
        print("The video started playing automatically.")

def getCaptionsContainer(driver: webdriver.Chrome) -> WebElement:
    caption_container = driver.find_element(By.CLASS_NAME, "ytp-caption-window-container")
    return caption_container

def getCaptionsLines(driver: webdriver.Chrome) -> WebElement:
    """
    Extract all caption lines
    """
    caption_lines = driver.find_elements(By.CLASS_NAME, "caption-visual-line")
    return caption_lines

# def getCaptionsLines(caption_container: WebElement) -> WebElement :
#     """
#     Extract all caption lines
#     """
#     caption_lines = caption_container.find_elements(By.CLASS_NAME, "caption-visual-line")
#     if len(caption_lines):
#         # Extract text from each a line
#         for line in caption_lines:
#             text = line.text
#             if text != last_text:
#                 print(text)
#                 last_text=text
#     return text