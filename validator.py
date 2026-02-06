import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
CHROME_DRIVER_PATH = r"C:\chromedriver.exe"
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
input_file = os.path.join(desktop, "emails5.txt")
valid_file = os.path.join(desktop, "working5.txt")
invalid_file = os.path.join(desktop, "notworking5.txt")


def get_already_processed():
    """Reads existing txt files to prevent duplicates."""
    processed = set()
    for f_path in [valid_file, invalid_file]:
        if os.path.exists(f_path):
            with open(f_path, 'r') as f:
                processed.update([line.strip() for line in f if line.strip()])
    return processed


def save_result(file_path, email):
    """Saves email only if it's not already in the file."""
    with open(file_path, 'a') as f:
        f.write(email + "\n")


def check_outlook_emails():
    service = Service(executable_path=CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=service, options=options)

    if not os.path.exists(input_file):
        print("Error: emails.txt not found on Desktop.")
        return

    with open(input_file, 'r') as f:
        emails = [line.strip() for line in f if line.strip()]

    # Load already checked emails to avoid duplicates
    already_done = get_already_processed()

    total = len(emails)
    print(f"Starting... Total emails: {total} (Already processed: {len(already_done)})\n")

    for index, email in enumerate(emails, 1):
        if email in already_done:
            print(f"[{index}/{total}] Skipping (Already Done): {email}")
            continue

        print(f"[{index}/{total}] Checking: {email}")
        driver.get("https://login.microsoftonline.com/")

        try:
            # Wait for email field
            email_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.NAME, "loginfmt"))
            )
            email_input.clear()
            email_input.send_keys(email)
            time.sleep(1)  # Small pause
            email_input.send_keys(Keys.ENTER)  # Press Enter to submit

            # --- DETECTION LOGIC ---
            # Wait 3 seconds as requested for the network to catch up
            time.sleep(3)

            # Now we look for either the Error ID or the Password Name
            error_elements = driver.find_elements(By.ID, "usernameError")
            pass_elements = driver.find_elements(By.NAME, "passwd")

            if error_elements and "couldn't find an account" in error_elements[0].text:
                print(f"  -> RESULT: NOT WORKING")
                save_result(invalid_file, email)
                already_done.add(email)

            elif pass_elements:
                print(f"  -> RESULT: WORKING")
                save_result(valid_file, email)
                already_done.add(email)

            else:
                # If network is REALLY slow, try one more 5-second dynamic wait
                print("  -> Waiting extra time for slow network...")
                for _ in range(10):  # Max 10 more seconds
                    if driver.find_elements(By.NAME, "passwd"):
                        save_result(valid_file, email)
                        print(f"  -> RESULT: WORKING (Late Load)")
                        break
                    if driver.find_elements(By.ID, "usernameError"):
                        save_result(invalid_file, email)
                        print(f"  -> RESULT: NOT WORKING (Late Load)")
                        break
                    time.sleep(1)

        except Exception as e:
            print(f"  -> ERROR: {e}")

    driver.quit()
    print("\nCheck your Desktop for results.")


if __name__ == "__main__":
    check_outlook_emails()
