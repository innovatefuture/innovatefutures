import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Load the data from CSV/Excel file
data = pd.read_excel('Merged_Resources Final.xlsx')


# Iterate through each row in the data
for index, row in data.iterrows():
    # Set up the driver for each iteration
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    try:
        # Navigate to the site
        driver.get("https://innovatefutures.net/admin/resources/howto/create/")

        # Log in
        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        #add your superuser email and password
        email=''
        password=''
        username.send_keys(email)
        password.send_keys(password)
        password.send_keys(Keys.RETURN)


        time.sleep(1)  # Wait for login to complete

        # Fill in the title
        title = driver.find_element(By.NAME, 'title')
        title.clear()
        title.send_keys(row['Resource name'])

        # Fill in the summary (using 'Services Provided' as an example)
        summary = driver.find_element(By.NAME, 'summary')
        summary.clear()
        summary_text = str(row['description']) if pd.notna(row['description']) else 'No summary found'
        summary.send_keys(summary_text)

        # Fill in the link (website)
        link = driver.find_element(By.NAME, 'link')
        link.clear()
        link_text = str(row['website']) if pd.notna(row['website']) else ''
        link.send_keys(link_text)

        # Locate and add tags (if needed, use 'Intersectional Issues')
        tag_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.tagit li.tagit-new input'))
        )

        columns_to_process = ['Assets', 'Services Provided', 'Intersectional Issues', 'Population Groups']
        tags_list = []

        for col in columns_to_process:
            if pd.notna(row[col]):
                tags_list.extend(str(row[col]).split(', '))

        # Remove duplicates by converting to a set, then back to a list
        unique_tags_list = list(set(tags_list))


        for tag in unique_tags_list:
            print(tag,end='\n')
            tag_input.send_keys(tag)
            tag_input.send_keys(Keys.RETURN)

        # Fill in the location (latitude and longitude)
        location_input = driver.find_element(By.ID, 'id_location_latlng')
        location_text = f"{row['lat']},{row['lng']}" if pd.notna(row['lat']) and pd.notna(row['lng']) else ''
        location_input.send_keys(location_text)
        location_input.clear()
        location_input.send_keys(location_text)
        location_input.send_keys(Keys.DELETE)

        # Click the save button
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button.action-save'))
        )
        save_button.click()

        time.sleep(2)  # Wait for the save operation to complete

    finally:
        # Close the browser after each iteration
        driver.quit()

    time.sleep(1)  # Wait for save operation to complete