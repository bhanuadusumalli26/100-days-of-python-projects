from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from .env file
load_dotenv()

ACCOUNT_EMAIL = os.getenv("Linkedln_Email")
ACCOUNT_PASSWORD = os.getenv("Linkedln_password")
PHONE = os.getenv("phone_number")


# Function to abort complex applications
def abort_application(driver):
    try:
        logging.info("Aborting application...")
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss"))
        )
        close_button.click()

        discard_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")
            )
        )
        discard_button.click()
    except TimeoutException:
        logging.warning("Failed to abort application due to timeout.")


# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")  # Start browser maximized

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open LinkedIn jobs page
    driver.get(
        "https://www.linkedin.com/jobs/search/?alertAction=viewjobs&currentJobId=4097270673&distance=25&f_AL=true&f_E=1&f_TPR=r86400&geoId=105214831&keywords=data%20analyst&location=Bengaluru%2C%20Karnataka%2C%20India&origin=JOB_SEARCH_PAGE_JOB_FILTER"
    )

    # Reject cookies
    try:
        reject_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[action-type="DENY"]'))
        )
        reject_button.click()
        logging.info("Cookies rejected.")
    except TimeoutException:
        logging.warning("No cookies popup found.")

    # Click sign-in button
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
    )
    sign_in_button.click()

    # Log in
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_field.send_keys(ACCOUNT_EMAIL)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(ACCOUNT_PASSWORD)
    password_field.send_keys(Keys.ENTER)

    # Wait for CAPTCHA to be solved manually
    input("Press Enter when you have solved the CAPTCHA")

    # Get all job listings
    all_listings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".job-card-container--clickable")
        )
    )

    for listing in all_listings:
        logging.info("Opening job listing...")
        listing.click()
        time.sleep(2)  # Allow page to load

        try:
            # Click apply button
            apply_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-s-apply button"))
            )
            apply_button.click()

            # Fill phone number if required
            time.sleep(2)  # Allow form to load
            try:
                phone = driver.find_element(By.CSS_SELECTOR, "input[id*=phoneNumber]")
                if phone.get_attribute("value").strip() == "":
                    phone.send_keys(PHONE)
            except NoSuchElementException:
                logging.info("Phone number field not found.")

            # Check the submit button
            submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")
            if submit_button.get_attribute("data-control-name") == "continue_unify":
                abort_application(driver)
                logging.info("Complex application, skipped.")
                continue
            else:
                logging.info("Submitting job application...")
                submit_button.click()

            # Close the modal after submission
            close_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "sign-in-button")
                )  # Adjust the selector
            )
            # until(
            #     EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss"))
            # )
            close_button.click()
        except NoSuchElementException:
            logging.warning("No apply button found, skipping listing.")
        except TimeoutException:
            logging.warning("Timed out while interacting with the application process.")

    logging.info("Job application process completed.")

finally:
    logging.info("Closing browser...")
    driver.quit()
