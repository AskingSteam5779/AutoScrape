import pandas as pd
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Function for random mouse movement
def random_mouse_movement(driver, element):
    action = ActionChains(driver)
    element_size = element.size
    element_location = element.location

    x_offset = random.randint(-50, 50)
    y_offset = random.randint(-50, 50)

    if 0 <= element_location["x"] + x_offset <= element_location["x"] - element_size["width"] and \
            0 <= element_location["y"] + y_offset <= element_location["y"] - element_size["height"]:
        action.move_to_element_with_offset(element, x_offset, y_offset).perform()
    else:

        pass


# Function for random scrolling
def random_scroll(driver):
    scroll_amount = random.randint(-300, 300)
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    time.sleep(random.uniform(0.5, 2))


# Launches browser and opens webpage
driver = webdriver.Chrome()
driver.get("https://www.careershift.com/Account/Login")

# Input sign in email
sign_in_email = driver.find_element(By.ID, "UserEmail")
input_email = input("Input your email: ")
sign_in_email.send_keys(input_email)

# Input sign in password
sign_in_password = driver.find_element(By.ID, "Password")
input_password = input("Input your password: ")
sign_in_password.send_keys(input_password)

# Sign in
sign_in_button = driver.find_element(By.XPATH, '//button[text()="Login"]')
sign_in_button.click()

# If "Try it Out!" button is there, it is clicked
try_it = '//a[@class="btn btn-link dismiss" and text()="Try it out!"]'
try:
    try_it = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, try_it)))

    try_it.click()
except NoSuchElementException:

    pass

# Creates list of companies to search
companies = []

# Asks for 5 companies to search
for i in range(5):
    company = input(f"Enter company {i + 1}: ")
    companies.append(company)

# Creates empty dataframe to store First Name, Last Name, and Company
all_data = pd.DataFrame(columns=["First Name", "Last Name", "Company"])

# Loops through companies
for company_input in companies:
    # Clicks Contact Dropdown
    wait = WebDriverWait(driver, 10)
    contacts_button = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                   '//span[@class="title" and text()="Contacts"]')))
    contacts_button.click()

    # Clicks Search
    search_link = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.LINK_TEXT, "Search")))
    search_link.click()

    # Inputs search term
    company_name = driver.find_element(By.ID, "CompanyName")
    company_name.clear()
    company_name.send_keys(company_input)
    
    # Random mouse movement and scrolling
    random_mouse_movement(driver, company_name)
    random_scroll(driver)

    # Clicks on Search button
    search_button = driver.find_element(By.CLASS_NAME, "search-button")
    search_button.click()
    
    # New Update on careershift breaks site when advanced searching with executives
    """
    advanced_switch = driver.find_element(By.XPATH, '//span[@title="Advanced Search"]')
    advanced_switch.click()
    # Random mouse movement and scrolling
    random_mouse_movement(driver, advanced_switch)
    random_scroll(driver)

    # Clicks on Executive Checkbox
    executive = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
        By.XPATH, '//label[@for="TitleSeniority-Executives"]')))
    executive.click()

    # Searches using advanced search
    advanced_search = driver.find_element(By.XPATH, '//button[@class="btn btn-primary btn-lg btn-block py-3 uppercase '
                                                    'search-button text-nowrap"]')
    advanced_search.click()
    """
    # Waits until contacts are there
    contacts = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   "[id^='contact-title-']")))

    # Makes it so it only grabs the first 5 names
    contacts = contacts[:5]

    # Creates empty list for names to be stripped and placed in list
    names = []
    
    # Loops through contacts and strips names
    for contact in contacts:
        name = contact.text.strip()
        first_name, last_name = name.split(" ", 1)
        names.append((first_name, last_name))
    # Creates dataframe for names and company
    
    data = {"First Name": [name[0] for name in names], "Last Name": [name[1] for name in names],
            "Company": [company_input] * len(names)}
    df = pd.DataFrame(data)
    all_data = pd.concat([all_data, df], ignore_index=True)

# Sorts data alphabetically by company
sorted_data = all_data.sort_values(by=["Company"])
sorted_data.reset_index(drop=True, inplace=True)
sorted_data.to_excel("output.xlsx", index=False)
