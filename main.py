import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. File Path Setup (Portable Logic) ---
# Script ki apni location hasil karen
current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = "Sample_sheet.xlsx"  # GitHub repo mein majood file ka naam
file_path = os.path.join(current_dir, file_name)

# Check karen ke file waqai majood hai ya nahi
if not os.path.exists(file_path):
    print(f"ERROR: '{file_name}' nahi mili! Baraye meharbani file ko script ke sath wale folder mein rakhen.")
    exit()

# Excel file load karen
df = pd.read_excel(file_path)
if 'Mediafire Links' not in df.columns:
    print("ERROR: Excel file mein 'Mediafire Links' naam ka column nahi mila!")
    exit()

links = df['Mediafire Links'].tolist()

# --- 2. Chrome Driver Setup ---
options = webdriver.ChromeOptions()
# options.add_argument("--headless") # Agar aap browser window nahi dekhna chahte to ise uncomment karen
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # --- 3. Login Phase ---
    driver.get("https://www.mediafire.com/login/")
    print("\n--- LOGIN PROCESS ---")
    print("1. Khulne wali browser window mein apna MediaFire account login karen.")
    print("2. Login karne ke baad, wapis yahan terminal mein aayen aur ENTER dabayen...")
    input("Press Enter to start saving links...")

    count = 0
    success_count = 0
    failed_links = []

    # --- 4. Automation Loop ---
    for url in links:
        # Khali links ko skip karne ke liye
        if pd.isna(url) or not str(url).startswith("http"):
            continue
            
        try:
            driver.get(url)
            count += 1
            print(f"Processing ({count}/{len(links)}): {url}")

            # "Save to My Files" button ka intezar karen
            # MediaFire different UI show kar sakta hai, isliye multiple XPATHs use kiye hain
            wait = WebDriverWait(driver, 10)
            plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
                "//a[contains(@title, 'Save file')] | "
                "//button[contains(@title, 'Save file')] | "
                "//*[@class='g-icon i-plus'] | "
                "//a[contains(@class, 'save')]")))
            
            plus_button.click()
            print("✅ Successfully saved!")
            success_count += 1

            # Rate limiting se bachne ke liye delay
            time.sleep(3) 

        except Exception as e:
            print(f"❌ Is link par masla aya: {url}")
            failed_links.append(url)
            continue

    print("\n" + "="*30)
    print(f"Kaam Tamam! Total: {len(links)} | Saved: {success_count} | Failed: {len(failed_links)}")
    print("="*30)

finally:
    driver.quit()