from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import speedtest
import os
from dotenv import load_dotenv

load_dotenv()

# Constants
CHROME_DRIVER_PATH = (
    r"C:\path\to\chromedriver.exe"  # Update with your chromedriver path
)
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
UPLOAD_THRESHOLD = 10  # Mbps
DOWNLOAD_THRESHOLD = 20  # Mbps


class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.down_speed = 0
        self.up_speed = 0

    def get_internet_speed(self):
        print("Checking internet speed...")
        st = speedtest.Speedtest()
        st.get_best_server()
        self.down_speed = round(st.download() / 1_000_000, 2)  # Convert to Mbps
        self.up_speed = round(st.upload() / 1_000_000, 2)  # Convert to Mbps
        print(f"Download speed: {self.down_speed} Mbps")
        print(f"Upload speed: {self.up_speed} Mbps")

    def tweet_at_provider(self, message):
        print("Logging into Twitter...")
        self.driver.get("https://twitter.com/login")
        time.sleep(3)

        email_field = self.driver.find_element(By.NAME, "session[username_or_email]")
        password_field = self.driver.find_element(By.NAME, "session[password]")

        email_field.send_keys(TWITTER_EMAIL)
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.ENTER)
        time.sleep(5)

        print("Tweeting the message...")
        tweet_box = self.driver.find_element(
            By.XPATH, "//div[@aria-label='Tweet text']"
        )
        tweet_box.send_keys(message)

        tweet_button = self.driver.find_element(
            By.XPATH, "//div[@data-testid='tweetButtonInline']"
        )
        tweet_button.click()
        time.sleep(2)
        print("Tweet posted successfully!")

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    # Initialize bot
    bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)

    try:
        # Get internet speed
        bot.get_internet_speed()

        # Check if speed is below thresholds
        if bot.down_speed < DOWNLOAD_THRESHOLD or bot.up_speed < UPLOAD_THRESHOLD:
            tweet = (
                f"Dear ISP, why is my internet speed so low? "
                f"I'm getting {bot.down_speed} Mbps download and {bot.up_speed} Mbps upload, "
                f"but I was promised much higher speeds. #InternetSpeed #India"
            )
            bot.tweet_at_provider(tweet)
        else:
            print("Internet speed is fine, no tweet required.")
    finally:
        # Close the driver
        bot.close_driver()
