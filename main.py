"""

This script uses the 'Nutrionix' API to obtain workout information
and the 'Sheety' API to post the information to a google spreadsheet
to keep track of workouts.

This script requires that 'requests', 'python_dotenv' be installed within the Python
environment you are running this script in.

"""

import requests
import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")
EXCERCISE_POST_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'
EXCERCISE_POST_HEADER = {
    'x-app-key': API_KEY,
    'x-app-id': API_ID,
    'x-remote-user-id': '0'
}

query = input('What exercises did you do today? (Eg ran 3 miles)')

EXCERCISE_POST_PARAMS = {
    'query': query,
    'gender': 'male',
    'weight_kg': 61.7,
    'height_cm': 170.2,
    'age': 27
}

response = requests.post(url=EXCERCISE_POST_ENDPOINT, headers=EXCERCISE_POST_HEADER, json=EXCERCISE_POST_PARAMS)
response.raise_for_status()
data = response.json()
print(data)
# Start of STEP 4 SOLUTION
SHEETY_GET_ENDPOINT = os.getenv("SHEETY_GET_ENDPOINT")
SHEETY_POST_ENDPOINT = os.getenv("SHEETY_POST_ENDPOINT")
# Added this part for STEP 5
encoded_username_password = os.getenv("encoded_username_password")
SHEETY_HEADER = {
    'Authorization': encoded_username_password
}
for row in data['exercises']:
    date = dt.datetime.now().strftime('%d/%m/%Y')
    time = dt.datetime.now().strftime('%H:%M:%S')
    exercise = row['name'].title()
    duration = row['duration_min']
    calories = row['nf_calories']
    record = {
        'workout': {
            'date': date,
            'time': time,
            'exercise': exercise,
            'duration': duration,
            'calories': calories
        }
    }
    print(record)
    response = requests.post(url=SHEETY_POST_ENDPOINT, json=record, headers=SHEETY_HEADER)
    response.raise_for_status()
    print(response.text)
