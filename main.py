import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Excel file load karen
file_path = r"E:\My-Workstation\Coding\Python\Projects\mediafire file saver to myaccount by links\allurdupdfnovel.blogspot.com.xlsx" # Aap ki file ka naam
df = pd.read_excel(file_path)
links = df['Mediafire Links'].tolist()

# 2. Chrome Driver setup
options = webdriver.ChromeOptions()
# options.add_argument("--user-data-dir=C:/Users/YourUser/AppData/Local/Google/Chrome/User Data") # Optional: Session save karne ke liye
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 3. Pehle MediaFire open karen taake aap login kar saken
    driver.get("https://www.mediafire.com/login/")
    print("LOG IN KAREN: Browser mein login karne ke baad terminal mein ENTER press karen...")
    input() # Jab aap login kar len, tab yahan enter dabayen

    count = 0
    for url in links:
        try:
            driver.get(url)
            count += 1
            print(f"Processing ({count}/{len(links)}): {url}")

            # 4. "+" (Save to My Files) button ka intezar karen aur click karen
            # Mediafire par is button ka title aksar 'Save to My Files' hota ha
            wait = WebDriverWait(driver, 10)
            plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@title, 'Save file')] | //button[contains(@title, 'Save file')] | //*[@class='g-icon i-plus']")))
            
            plus_button.click()
            print("Successfully saved!")

            # Har link ke baad thora gap den taake account block na ho
            time.sleep(3) 

        except Exception as e:
            print(f"Is link par masla aya: {url}")
            continue

    print("--- Tamam links process ho gaye hain! ---")

finally:
    driver.quit()