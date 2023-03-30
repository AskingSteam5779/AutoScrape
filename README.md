# AutoScrape.py Version 1.1
Necessary dependencies:
Python 3.10, Selenium, pandas, ChromeDriver
Download Python 3.10: https://www.python.org/downloads/
Selenium from command prompt: pip --install selenium
Pandas from command prompt: pip --install pandas
Install ChromeDriver the same as your Chrome version: https://chromedriver.chromium.org/downloads

How to use:
Start the program and enter credentials to CareerShift.com
Program will initialize and ask for 5 companies, input 5 companies, the program will search all 5 companies, grab 5 contacts' (first and last names) and put them on an output.xlsx file sorted by company name

Temporary changes:
Removed the search by executives function due to CareerShift changes that breaks the site
