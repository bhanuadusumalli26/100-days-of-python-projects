from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)
from time import sleep
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
FB_EMAIL = os.getenv("facebook")
FB_PASSWORD = os.getenv("password")

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# Uncomment the following line to run in headless mode
# chrome_options.add_argument("--headless")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("http://www.tinder.com")

    # Wait for the login button and click it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[text()="Log in"]'))
    ).click()

    # Wait for Facebook login button and click it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button',
            )
        )
    ).click()

    # Switch to Facebook login window
    base_window = driver.window_handles[0]
    fb_login_window = driver.window_handles[1]
    driver.switch_to.window(fb_login_window)

    # Log in with Facebook credentials
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    ).send_keys(FB_EMAIL)

    driver.find_element(By.ID, "pass").send_keys(FB_PASSWORD)
    driver.find_element(By.ID, "pass").send_keys(Keys.ENTER)

    # Switch back to Tinder window
    driver.switch_to.window(base_window)

    # Handle location and notification pop-ups
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        )
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
        )
    ).click()

    # Handle cookies pop-up
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[1]/button')
        )
    ).click()

    # Perform 100 Likes
    for n in range(100):
        sleep(1)  # Add a short delay between actions
        try:
            like_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button',
                    )
                )
            )
            like_button.click()

        except ElementClickInterceptedException:
            try:
                # Handle "It's a Match!" pop-up
                match_popup = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".itsAMatch a"))
                )
                match_popup.click()
            except NoSuchElementException:
                print("Match pop-up not found; retrying...")
                sleep(2)

        except NoSuchElementException:
            print("Like button not found; retrying...")

finally:
    driver.quit()
