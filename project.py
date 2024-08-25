import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

st.subheader('Doctor finder for Indian people')   # this is the title for the app
# Input box for entering location
location = st.text_input('Enter your city:') 

# Dropdown box for specialization, the empty list is selected as first element so that if a user begans to scrape without entering specialization it doesnt return anything

specializations = [''] + ['Cardiologist', 'Dermatologist', 'Neurologist', 'Pediatrician', 'General Physician', 'Dentist', 'Homoeopath', 'Ayurveda', 'General surgeon']
specialization = st.selectbox('Select the specialization you are looking for:', specializations)

if specialization == '':
    st.warning("Please select a valid option from the dropdown!")
else:
    st.success(f"You selected: {specialization}")

# Button to start scraping

if st.button('Scrape'):
    # Encode the specialization for the URL

    encoded_specialization = quote(specialization)  # this trims down spaces between different parts of a specialization

    url = f'https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22{encoded_specialization}%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city={location}'

    # Headers to mimic a browser request so that we can appear a genuine connection

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Send the request to fetch the data from the URL
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser') 

             # Find information pertaining to tthe names of doctors
            doct_names = soup.find_all('div', class_="u-color--primary uv2-spacer--xs-bottom")

            # Check if there are any doctor profiles available so that we can count them
            doctor_profile_count = soup.find_all('div', class_='u-d-flex flex-ai-center u-spacer--top-md')   
            if len(doctor_profile_count) > 1: # this means doctor profile isnt an empty list
                number_of_available_doctors = doctor_profile_count[0].text
                st.markdown(f'##### {number_of_available_doctors}')    # The number of Hashes  is used to adjust the density of markdown 

            else:
                st.markdown(f"##### {len(doct_names)} doctors available as practising {specialization}s in the city of {location}" if len(doct_names) >0 else f'##### No data found for {specialization}s in {location}.')

            if len(doct_names) > 0:

                st.markdown('##### The doctors who make it to the top of the page in this specialization are:')
                for doct in doct_names:
                    st.write(doct.text)               # this displays the names of the doctors
        else:
            st.error(f"Failed to retrieve data. Status code: {response.status_code}")            
    except requests.exceptions.RequestException as e:
        st.markdown(f'##### An error occurred: {e}')

