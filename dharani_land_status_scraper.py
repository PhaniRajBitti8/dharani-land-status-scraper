# Script for scraping land status data from the Dharani portal of Telangana.

import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Defining the website URL
website = 'https://dharani.telangana.gov.in/knowLandStatus'

# Setting the path to chromedriver
path = 'C:/chromedriver-win64/chromedriver.exe'

# Initialising the webdriver service
service = Service(executable_path=path)

# Launching the webdriver service
driver = webdriver.Chrome(service=service)
driver.get(website)


# Function to get all the options from the dropdown
def get_dropdown_options(dropdown_element):
    return [option.text for option in dropdown_element.find_elements(By.TAG_NAME, 'option')]


# Function to select an option from a dropdown
def select_dropdown_option(dropdown_element, option):
    select = Select(dropdown_element)
    select.select_by_visible_text(option)


# Wait for dropdowns to load
time.sleep(2)

# Getting the elements from dropdown
district_dropdown = driver.find_element(By.ID, 'districtID')
mandal_dropdown = driver.find_element(By.ID, 'mandalID')
village_dropdown = driver.find_element(By.ID, 'villageId')
survey_no_dropdown = driver.find_element(By.ID, 'surveyIdselect')

data = []

# First get the options for the district dropdown
district_options = get_dropdown_options(district_dropdown)

# Looping through each district
for district in district_options:
    select_dropdown_option(district_dropdown, district)
    time.sleep(2)  # Wait for mandal dropdown to update

    # Now get the mandal options
    mandal_options = get_dropdown_options(mandal_dropdown)

    # Looping through each mandal dropdown
    for mandal in mandal_options:
        select_dropdown_option(mandal_dropdown, mandal)
        time.sleep(2) # Wait for village dropdown to update

        # Now get the options for village
        village_options = get_dropdown_options(village_dropdown)

        # Looping through each village
        for village in village_options:
            select_dropdown_option(village_dropdown, village)
            time.sleep(2) # Wait for survey nno to update

            # Get options for the survey number dropdown
            survey_no_options = get_dropdown_options(survey_no_dropdown)

            # Looping through survey numbers after removing Please Select from dropdown
            for survey_no in survey_no_options:
                if district != "Please Select" and mandal != "Please Select" and village != "Please Select" and survey_no != "Please select":
                    data.append({'District': district, 'Mandal': mandal, 'Village': village, 'Survey No': survey_no})

# Creating DataFrame from the collected data
df = pd.DataFrame(data)

# Saving the above DataFrame to CSV file
df.to_csv('dharani_land_status_telangana.csv', index=False)

# Finally Closing the driver
driver.quit()