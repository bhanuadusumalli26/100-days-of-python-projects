from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(
    "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
)

# Wait for the price elements to appear on the page
try:
    price_dollar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole"))
    )
    price_cents = driver.find_element(By.CLASS_NAME, "a-price-fraction")

    print(price_dollar.text)
    print(price_cents.text)
except Exception as e:
    print("Error: ", e)

driver.quit()
