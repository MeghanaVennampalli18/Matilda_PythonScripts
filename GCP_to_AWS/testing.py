from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# This will automatically download and use the correct ChromeDriver version
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://aws.amazon.com/cloudwatch/pricing/")



# driver.find_element_by_class_name("lb-txt-none lb-txt-16 lb-txt").click()

title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".text_module_text__16d6jzf.text_module_one__16d6jzf.text_module_heading__16d6jzf.text_module_block__16d6jzf"))
    )

if title.text == "Amazon CloudWatch Pricing":
    print("Title is correct")
else:
    print("Title is incorrect")
    print("Actual title:", title.text)


# driver.find_element(By.ID, "aws-element-85c136e5-6fef-451a-a630-6eee3b8049db-tab-1").click() 

# Wait for any overlay/dialog to disappear
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.dialog_module_backdrop__16xx0uw"))
)

# Find and click the specific dropdown button
dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.awsui_button-trigger_18eso_20dwt_97.awsui_has-caret_18eso_20dwt_137"))
)
dropdown_button.click()

# Wait a moment for the dropdown to appear
time.sleep(2)

# Wait for dropdown options and select Canada using role and text
canada_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//li[@role='option']//span[text()='Canada (Central)']"))
)
canada_option.click()

time.sleep(3600) 



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time


# def fetch_cloudwatch_logs_price():
#     # Set up the WebDriver (ensure chromedriver is in your PATH or provide the executable path)
#     driver_path = "path/to/chromedriver"  # Replace with your ChromeDriver path
#     driver = webdriver.Chrome(executable_path=driver_path)

#     try:
#         # Navigate to the AWS Pricing Calculator page for CloudWatch Logs
#         aws_pricing_url = "https://aws.amazon.com/cloudwatch/pricing/"
#         driver.get(aws_pricing_url)

#         # Wait for the page to load and the relevant content to appear
#         wait = WebDriverWait(driver, 10)  # Timeout after 10 seconds
#         price_element = wait.until(
#             EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Logs-Standard Storage')]/following-sibling::td"))
#         )

#         # Extract the price text
#         price_text = price_element.text
#         price = float(price_text.strip('$'))  # Convert to float if necessary
#         print(f"CloudWatch Logs - Standard Storage Price: ${price:.4f} per GB")

#     except Exception as e:
#         print(f"An error occurred: {e}")

#     finally:
#         # Close the browser
#         driver.quit() 

# # Run the function
# fetch_cloudwatch_logs_price()