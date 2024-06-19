from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import time
import re
from datetime import datetime
from pushbullet import PushBullet
import streamlit as st

st.title('Refresher app')

API_KEY = "o.vYtRgQo87BXOQsZMZiNrWOn5WOKeiL2l"
pb = PushBullet(API_KEY)

with st.spinner("Launching Selenium..."):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if 'driver' not in st.session_state:
        st.session_state.driver = webdriver.Chrome(options=chrome_options)

if st.button('Start refreshing'):

    if st.button('Stop the machine'):
        st.session_state.driver.quit()

    with st.spinner("Getting information..."):

        # Navigate to the URL
        st.session_state.driver.get("https://appointment.bmeia.gv.at/")

        time.sleep(5)

        # Locate the select element by its ID
        select_element = st.session_state.driver.find_element_by_id("Office")

        # Create a Select object
        select = Select(select_element)

        # Select an option by visible text
        select.select_by_visible_text("ASTANA")

        time.sleep(5)

        # Find the button using CSS selector
        button = st.session_state.driver.find_element_by_css_selector("input[value='Next']")

        # Click the button (or perform any other action)
        button.click()

        time.sleep(5)

        # Locate the select element by its ID
        select_element1 = st.session_state.driver.find_element_by_id("CalendarId")

        # Create a Select object
        select1 = Select(select_element1)

        # Select an option by visible text
        select1.select_by_visible_text("Aufenthaltstitel/Вид на жительство")

        time.sleep(5)

        # Find the button using CSS selector
        button = st.session_state.driver.find_element_by_css_selector("input[value='Next']")

        # Click the button (or perform any other action)
        button.click()

        time.sleep(5)

        # Find the button using CSS selector
        button = st.session_state.driver.find_element_by_css_selector("input[value='Next']")

        # Click the button (or perform any other action)
        button.click()

        push = pb.push_note('Updater', 'Updater is active')

        time.sleep(5)

    good = False

    while not good:

        # Locate the first <td> in the specified table structure using XPath
        first_td = st.session_state.driver.find_element_by_xpath("(//table[@class='no-border'])[2]/tbody/tr[1]/td[1]")
        # Get the text of the first <td> element
        week = first_td.text

        match = re.search(r'\b(\d{1,2})/\d{1,2}/\d{4}\b', week)
        if match:
            month = int(match.group(1))
            st.write(f"Extracted month: {month}")

            # Check if the month is earlier than August (month 8)
            if month < 8:
                st.write("YESSSS")
                push = pb.push_note('Updater', 'REGISTER NOW!')
                good = True
            else:
                current_time = datetime.now()
                st.write(f"Not yet...{current_time}")
                time.sleep(300)
                st.session_state.driver.refresh()
                time.sleep(2)
                try:
                    alert = Alert(st.session_state.driver)
                    alert.accept()
                except:
                    pass
        else:
            st.write("No date found in the text.")

    time.sleep(1200)

    # Close the browser
    st.session_state.driver.quit()

