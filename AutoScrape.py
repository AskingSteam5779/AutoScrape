import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
company_input = input("Enter the company name: ")
company_name.send_keys(company_input)

# Clicks on Search button
search_button = driver.find_element(By.CLASS_NAME, "search-button")
search_button.click()

# Clicks on Advanced Switch
advanced_switch = driver.find_element(By.XPATH, '//span[@title="Advanced Search"]')
advanced_switch.click()

# Clicks on Executive Checkbox
executive = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,
                                                                       '//label[@for="TitleSeniority-Executives"]')))
executive.click()

# Searches using advanced search
advanced_search = driver.find_element(By.XPATH, '//button[@class="btn btn-primary btn-lg btn-block py-3 uppercase '
                                                'search-button text-nowrap"]')
advanced_search.click()

# Waits until contacts are there
contacts = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                               "[id^='contact-title-']")))

# Makes it so it only grabs the first 5 names
contacts = contacts[:5]

# Creates empty list for names to be stripped and placed in list
names = []

for contact in contacts:
    name = contact.text.strip()
    first_name, last_name = name.split(" ", 1)
    names.append((first_name, last_name))

names.sort(key=lambda x: x[0])

data = {"First Name": [name[0] for name in names], "Last Name": [name[1] for name in names]}
df = pd.DataFrame(data)

df.to_excel("output.xlsx", index=False)
