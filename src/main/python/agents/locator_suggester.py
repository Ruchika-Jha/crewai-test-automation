import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

def suggest_locators(action_text, login_required=True):
    load_dotenv()
    url = os.getenv('TEST_WEBSITE_URL')
    username = os.getenv('TEST_USERNAME', 'standard_user')
    password = os.getenv('TEST_PASSWORD', 'secret_sauce')
    driver = webdriver.Chrome()
    driver.get(url)

    # Perform login if required (example for saucedemo.com)
    if login_required:
        try:
            driver.find_element(By.ID, 'user-name').send_keys(username)
            driver.find_element(By.ID, 'password').send_keys(password)
            driver.find_element(By.ID, 'login-button').click()
            print(f"Logged in as {username}")
        except Exception as e:
            print(f"Login step failed: {e}")

    print(f"Scanning {url} for action: '{action_text}'\n")

    # Try to find by exact button text
    try:
        button = driver.find_element(By.XPATH, f"//button[text()='{action_text}']")
        print(f"Suggested locator: By.XPATH, \"//button[text()='{action_text}']\"")
    except:
        print("No button found with exact text.")

    # Try to find by partial match
    buttons = driver.find_elements(By.XPATH, f"//button[contains(text(), '{action_text}')]")
    for btn in buttons:
        print(f"Suggested locator: By.XPATH, \"//button[contains(text(), '{action_text}')]\"")

    # Try to find by id
    elements = driver.find_elements(By.XPATH, f"//*[@id]")
    for el in elements:
        if action_text.lower() in el.get_attribute("id").lower():
            print(f"Suggested locator: By.ID, \"{el.get_attribute('id')}\"")

    driver.quit()

# Example usage:
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python locator_suggester.py <action_text> [no-login]")
    else:
        action_text = sys.argv[1]
        login_required = True
        if len(sys.argv) > 2 and sys.argv[2] == 'no-login':
            login_required = False
        suggest_locators(action_text, login_required)
