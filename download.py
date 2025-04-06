import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

download_dir = "./download"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Chrome options configuration
def get_chrome_options(download_dir):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {
        "download.default_directory": os.path.abspath(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return chrome_options

def download_file(url, download_dir):
    driver = None
    try:
        chrome_options = get_chrome_options(download_dir)
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        time.sleep(4)
        
        download_button = driver.find_element(By.XPATH, "//a[contains(@class, 'link-button') and contains(text(), 'Download')]")
        
        actions = ActionChains(driver)
        for _ in range(1):
            actions.double_click(download_button).perform()
            time.sleep(1)
        
    except Exception as e:
        print(f"Error while processing {url}: {e}")
    finally:
        if driver:
            driver.quit()

# Hàm xóa tất cả file trong thư mục
def clear_download_directory(directory):
    try:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"Cleared all files in {directory}")
    except Exception as e:
        print(f"Error while clearing directory {directory}: {e}")

# Process links from multiple environment variables
i = 0
file_count = 0  # Đếm số lượng file đã tải
MAX_FILES_BEFORE_CLEAR = 50  # Giới hạn số file trước khi xóa

while True:
    links_key = f"LINKS{i:02d}" if i > 0 else "LINKS"
    links_str = os.getenv(links_key, None)
    
    if links_str is None:
        if i == 0:
            print("No LINKS environment variables found.")
            break
        else:
            break
    
    links = links_str.splitlines()
    
    for link in links:
        if link.strip().startswith("#"):
            continue
        download_file(link, download_dir)
        file_count += 1
        
        # Kiểm tra nếu đã tải đủ số file tối đa thì xóa thư mục
        if file_count >= MAX_FILES_BEFORE_CLEAR:
            clear_download_directory(download_dir)
            file_count = 0  # Reset bộ đếm
    
    i += 1

# Xóa lần cuối sau khi hoàn tất
time.sleep(3)
clear_download_directory(download_dir)
