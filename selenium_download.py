import os
import glob
import pdb
import time
import shutil
import argparse
import sqlite3
import pandas as pd
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from sql_utils import create_database_and_table, insert_table_info, update_location, fetch_undownloaded_url, update_table_name


download_dir = r'C:\Users\chenq\Downloads'

def get_newest_file(directory):
    # Get list of all files in the directory
    list_of_files = glob.glob(os.path.join(directory, '*'))
    
    # Filter out directories, keep only files
    list_of_files = [f for f in list_of_files if os.path.isfile(f)]
    
    if not list_of_files:
        return None
    
    # Find the newest file
    newest_file = max(list_of_files, key=os.path.getmtime)
    
    # return os.path.basename(newest_file)
    return newest_file



def load_urls(file_name, file_dir='./output'):
    file_path = os.path.join(file_dir, file_name)
    urls = pd.read_json(file_path)['url'].tolist()
    return urls


def selenium_download(conn, destination_dir):
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Iterate over each URL
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
            # urls_process_status[cur_url] = 'success'

            file_path = get_newest_file(download_dir)
            file_name = os.path.basename(file_path)
            new_file_path = move_file(file_path, destination_dir)
            # Update the location in the database
            update_location(conn, cur_url, new_file_path) 
            update_table_name(conn, cur_url, file_name)

        except Exception as e:
            print(f"Failed to download from {cur_url}: {e}")
            # urls_process_status[cur_url] = 'failed'

        cur_url = fetch_undownloaded_url(conn)
    

    # Close the browser
    driver.quit()


def move_file(src_path, dest_dir):
    # Create the destination directory if it does not exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Construct full file path
    file_name = os.path.basename(src_path)
    flatten_file_name = file_name.lower().replace(' ', '_')
    dest_file = os.path.join(dest_dir, flatten_file_name)
    
    # Move the file
    shutil.move(src_path, dest_file)
    print(f'Moved: {src_path} -> {dest_file}')
    return dest_file


if __name__ == "__main__":

    conn = sqlite3.connect('database.db')

    create_database_and_table(conn)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Download files using Selenium")
    parser.add_argument("--name", help="List of URLs to download files from", required=True)
    args = parser.parse_args()

    urls = load_urls(args.name)
    for url in urls:
        insert_table_info(conn, 'undownloaded', url)

    conn.commit()
    flattened_name = args.name.lower().replace(' ', '_')[:-5]
    selenium_download(conn, destination_dir=f'./storage/{flattened_name}')
    conn.commit()
    



