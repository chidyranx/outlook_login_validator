# 🚀 Outlook Account Validator

A high-performance, automated Selenium script designed to bulk-validate Microsoft Outlook/Hotmail email addresses. It identifies which accounts exist and which do not, handling slow network conditions and preventing duplicate entries automatically.
Due to account inactivity, microsoft might delete accounts that were inactive more than 2 years, this code will help you check which account is active or not account.
## 📖 Features

* **Accuracy:** Uses specific Microsoft DOM selectors (`usernameError` and `passwd`) to ensure 100% accurate validation.
* **Duplicate Protection:** Automatically scans existing result files to skip emails that have already been processed.
* **Slow Network Handling:** Implements dynamic waiting logic to allow the page to load on slower connections without crashing.
* **Local Driver Support:** Configured to run using a local `chromedriver.exe` for better control.
* **Auto-Logging:** Segregates results into `working.txt` and `notworking.txt` directly on your Desktop.

---

## 🛠️ Installation & Setup

### 1. Prerequisites

Ensure you have **Python 3.x** installed. You will also need the Selenium library:

```bash
pip install selenium

```

### 2. Driver Configuration

1. Download the **ChromeDriver** that matches your Chrome version.
2. Place `chromedriver.exe` in your `C:\` drive (or update the path in the script).

### 3. Prepare your Data

Create a file named `emails.txt` on your **Desktop** and paste your email list (one email per line).

---

## 🚀 How it Works

The validator follows a precise logic flow to ensure Microsoft doesn't flag the automation:

1. **Initialization:** Loads the browser and checks your Desktop for any previously saved results to avoid double-checking.
2. **Navigation:** Goes to the Microsoft Login portal.
3. **Input:** Types the email and simulates a human "Enter" key press.
4. **Wait & Detect:** * If the `passwd` field appears: The email is **Valid**.
* If the `usernameError` div appears: The email is **Invalid**.


5. **Output:** Instantly appends the email to the correct file on your Desktop.

---

## 📂 Project Structure

* `validator.py`: The main automation script.
* `emails.txt`: Your input list (Desktop).
* `working.txt`: Valid accounts (Auto-generated).
* `notworking.txt`: Non-existent accounts (Auto-generated).

---

## ⚠️ Disclaimer

This tool is for educational and authorized testing purposes only. Automated login attempts may violate Microsoft's Terms of Service. Use responsibly.

---
