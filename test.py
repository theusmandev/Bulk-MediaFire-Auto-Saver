

import pandas as pd
import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. Paths Setup ---
current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = "upload - Copy.xlsx"
file_path = os.path.join(current_dir, file_name)
# Cookies save karne ke liye folder
user_data_dir = os.path.join(current_dir, "selenium_chrome_profile")

if not os.path.exists(file_path):
    print(f"ERROR: '{file_name}' nahi mili!")
    exit()

# Backup logic
backup_path = os.path.join(current_dir, "Backup_Sample_sheet.xlsx")
shutil.copy2(file_path, backup_path)

# --- 2. Chrome Options (Session Bachane ke liye) ---
options = webdriver.ChromeOptions()
# Yeh line aapka login session save rakhegi
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Default") 
# Automation detection ko kam karne ke liye
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def safe_save(dataframe, path):
    temp_path = path + ".tmp"
    try:
        dataframe.to_excel(temp_path, index=False)
        if os.path.exists(path): os.remove(path)
        os.rename(temp_path, path)
    except Exception as e:
        print(f"⚠️ Save Error (Excel band rakhen): {e}")

try:
    # --- 3. Persistent Login Check ---
    driver.get("https://www.mediafire.com/myfiles/")
    print("\n--- CHECKING LOGIN ---")
    print("Agar aap login hain, to files nazar ayengi. Agar nahi, to login karen.")
    input("Check karne ke baad ke Dashboard khula hai, ENTER dabayen...")

    df = pd.read_excel(file_path)
    if 'Status' not in df.columns: df['Status'] = ""

    # --- 4. Main Loop ---
    for index, row in df.iterrows():
        raw_links = str(row['Mediafire Links'])
        if str(row['Status']).lower() == "saved" or raw_links == 'nan':
            continue

        link_list = [l.strip() for l in raw_links.split(',')]
        row_success = True 

        print(f"Row {index + 1}: Processing {len(link_list)} links...")

        for url in link_list:
            if not url.startswith("http"): continue
            try:
                driver.get(url)
                # Check karen agar login wapas mang raha hai
                if "login" in driver.current_url:
                    print("⚠️ Login session out! Please login again in the browser.")
                    input("Login karne ke baad ENTER dabayen...")
                    driver.get(url) # Dobara link par jayen

                wait = WebDriverWait(driver, 15)
                plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
                    "//a[contains(@title, 'Save file')] | //button[contains(@title, 'Save file')] | "
                    "//*[@class='g-icon i-plus'] | //a[contains(@class, 'save')]")))
                
                plus_button.click()
                time.sleep(4) # Rate limit se bachne ke liye thora ziada time
            except Exception:
                row_success = False
                break 

        if row_success:
            df.at[index, 'Status'] = "Saved"
            safe_save(df, file_path)
            print(f"✅ Row {index + 1} Saved.")

    print("\nKaam Mukammal!")

finally:
    driver.quit()












# import pandas as pd
# import time
# import os
# import shutil # File backup ke liye
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# # --- 1. File Path & Backup Setup ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_name = "upload - Copy"
# file_path = os.path.join(current_dir, file_name)
# backup_path = os.path.join(current_dir, "Sample_sheet_BACKUP.xlsx")

# if not os.path.exists(file_path):
#     print(f"ERROR: '{file_name}' nahi mili!")
#     exit()

# # Script shuru hone se pehle ek backup copy bana len (Safety First!)
# shutil.copy2(file_path, backup_path)
# print(f"✅ Backup ban gaya hai: {backup_path}")

# try:
#     df = pd.read_excel(file_path)
# except Exception as e:
#     print(f"❌ File corrupt lag rahi hai! Backup use karen. Error: {e}")
#     exit()

# if 'Status' not in df.columns:
#     df['Status'] = ""

# # --- 2. Chrome Driver Setup ---
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# def safe_save(dataframe, path):
#     """File ko save karne ka mehfooz tareeqa"""
#     temp_path = path + ".tmp"
#     try:
#         dataframe.to_excel(temp_path, index=False)
#         if os.path.exists(path):
#             os.remove(path)
#         os.rename(temp_path, path)
#     except Exception as e:
#         print(f"⚠️ Save karne mein masla: {e}. Make sure Excel file band hai!")

# try:
#     # --- 3. Login Phase ---
#     driver.get("https://www.mediafire.com/login/")
#     print("\n--- LOGIN PROCESS ---")
#     input("Login kar ke ENTER dabayen...")

#     # --- 4. Loop ---
#     for index, row in df.iterrows():
#         raw_links = str(row['Mediafire Links'])
#         status = str(row['Status'])

#         if status.lower() == "saved":
#             continue

#         if raw_links == 'nan' or not raw_links.strip():
#             continue

#         link_list = [l.strip() for l in raw_links.split(',')]
#         row_success = True 

#         print(f"\nProcessing Row {index + 1}: {len(link_list)} links")

#         for url in link_list:
#             if not url.startswith("http"): continue
#             try:
#                 driver.get(url)
#                 wait = WebDriverWait(driver, 10)
#                 plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
#                     "//a[contains(@title, 'Save file')] | //button[contains(@title, 'Save file')] | "
#                     "//*[@class='g-icon i-plus'] | //a[contains(@class, 'save')]")))
#                 plus_button.click()
#                 print(f"-> Saved: {url}")
#                 time.sleep(2)
#             except Exception:
#                 row_success = False
#                 print(f"❌ Link fail: {url}")
#                 break 

#         if row_success:
#             df.at[index, 'Status'] = "Saved"
#             # Har row ke baad safe save karein
#             safe_save(df, file_path)

#     print("\n" + "="*30 + "\nKaam Khatam!\n" + "="*30)

# finally:
#     driver.quit()










# import pandas as pd
# import time
# import os
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# # --- 1. File Path Setup ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_name = "upload.xlsx"
# file_path = os.path.join(current_dir, file_name)

# if not os.path.exists(file_path):
#     print(f"ERROR: '{file_name}' nahi mili!")
#     exit()

# df = pd.read_excel(file_path)

# if 'Status' not in df.columns:
#     df['Status'] = ""

# # --- 2. Chrome Driver Setup ---
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# try:
#     # --- 3. Login Phase ---
#     driver.get("https://www.mediafire.com/login/")
#     print("\n--- LOGIN PROCESS ---")
#     input("Login karne ke baad ENTER dabayen...")

#     # --- 4. Automation Loop ---
#     for index, row in df.iterrows():
#         raw_links = str(row['Mediafire Links'])
#         status = str(row['Status'])

#         if status.lower() == "saved":
#             print(f"Skipping Row {index + 1}: Already Saved.")
#             continue

#         if raw_links == 'nan' or not raw_links.strip():
#             continue

#         # Comma se links ko alag alag karein (Split logic)
#         link_list = [l.strip() for l in raw_links.split(',')]
#         row_success = True 

#         print(f"\nProcessing Row {index + 1}: Found {len(link_list)} link(s)")

#         for url in link_list:
#             if not url.startswith("http"):
#                 continue
                
#             try:
#                 driver.get(url)
#                 print(f"-> Saving: {url}")

#                 wait = WebDriverWait(driver, 10)
#                 plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
#                     "//a[contains(@title, 'Save file')] | "
#                     "//button[contains(@title, 'Save file')] | "
#                     "//*[@class='g-icon i-plus'] | "
#                     "//a[contains(@class, 'save')]")))
                
#                 plus_button.click()
#                 time.sleep(2) # Chota delay browser action ke liye

#             except Exception as e:
#                 print(f"❌ Masla aya is link par: {url}")
#                 row_success = False # Agar aik bhi link fail hua to row saved mark nahi hogi
#                 break # Agle row par chale jao ya handle karo

#         # Agar row ke saare links save ho gaye
#         if row_success:
#             df.at[index, 'Status'] = "Saved"
#             print(f"✅ Row {index + 1} ki saari files save ho gayin!")
#         else:
#             df.at[index, 'Status'] = "Failed/Partial"

#         # Save progress after each row
#         df.to_excel(file_path, index=False)

#     print("\n" + "="*30)
#     print("Mubarak ho! Saara kaam khatam.")
#     print("="*30)

# finally:
#     driver.quit()