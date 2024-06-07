from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import pdb
import time
import sqlite3
import platform
from sql_utils import create_database_and_table, insert_table_info, update_location, fetch_undownloaded_url, update_table_name
from utils import get_newest_file, move_file


def get_os_specific_download_path():
    os_name = platform.system()
    if os_name == "Darwin": # Macos
        # return r"temp_download"
        return r'.'
    elif os_name == "Windows": 
        return r'C:\Users\chenq\Downloads'
    else:
        raise NotImplementedError
    

def selenium_fetch_download(conn, source_url, destination_dir):
    # Setup Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")

    # prefs = {
    #     "download.default_directory": './temp_download',  # Set download directory
    #     "download.prompt_for_download": False,       # Disable download prompt
    #     "download.directory_upgrade": True,          # Allow directory upgrade
    #     "safebrowsing.enabled": True                 # Enable safe browsing to avoid warning dialogs
    # }
    # chrome_options.add_experimental_option("prefs", prefs)

    # Set path to chromedriver as per your configuration
    # webdriver_service = Service("/opt/homebrew/bin/chromedriver") # Change this to your own chromedriver path
    webdriver_service = Service() 
    # Choose Chrome Browser
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Open the website
    driver.get(source_url)
    # pdb.set_trace()

    # Wait for the page to load (adjust the time as necessary)
    time.sleep(5) # You can use WebDriverWait for a more efficient wait

    # Scroll down to load more content until no more new content loads
    scroll_pause_time = 5
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(f"Height: {last_height}")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page
        time.sleep(scroll_pause_time)

        # Check if new content is loaded
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        print(f"New height: {new_height}")
        if new_height >= 50000:
            break

    # Find all elements that match the given selector and extract their href attributes
    elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="template-thumbnail-card-renderer-a"]')

    # Extract the href attributes
    urls = [element.get_attribute('href') for element in elements]
    
    for url in urls:
        insert_table_info(conn, 'undownloaded', url)
    
    # Iterate through each href and click the download button
    cur_url = fetch_undownloaded_url(conn)
    while cur_url:
        try:
            # Open the URL
            driver.get(cur_url)
            time.sleep(5)  # Wait for the page to load, adjust the sleep time as needed

            # Find and click the download button using the class attribute
            download_button = driver.find_element(By.XPATH, '//button[@data-testid="template-download-button"]')
            download_button.click()

            time.sleep(5)  # Wait for the download to start

            downloaded_file_path = get_newest_file(get_os_specific_download_path())
            if downloaded_file_path is None:
                print(f"[Error] Failed to download from {url}")
            else:
                downloaded_file_name = os.path.basename(downloaded_file_path)
                location = move_file(downloaded_file_path, destination_dir)     
                # Update the location in the database
                update_location(conn, cur_url, location) 
                update_table_name(conn, cur_url, downloaded_file_name)

        except Exception as e:
            pass

        cur_url = fetch_undownloaded_url(conn)

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    conn = sqlite3.connect('table.db')
    create_database_and_table(conn)

    source_url = """
    https://create.microsoft.com/en-us/search?query=Business%20budgets&filters=excel
    """
    name = "payroll".replace(" ", "_").lower()
    destination_dir = f"./storage/{name}"
    selenium_fetch_download(conn, source_url, destination_dir)


