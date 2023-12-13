
from datetime import datetime, timedelta
import os
import csv
import pytz
import requests
from dotenv import load_dotenv
from airflow import DAG
from airflow.operators.python import PythonOperator


load_dotenv()

api_key = os.getenv('API_KEY')

locations = ['Quilpué', 'Vitacura']


default_args = {
    'owner': 'ggoni',
    'retry': 5,
    'retry_delay': timedelta(minutes=10)
}


def call_api(api_url, params=None, headers=None, method='GET', data=None):
    """
    Make an API call using the requests library.

    Parameters:
    - api_url (str): The URL of the API.
    - params (dict): Query parameters to include in the request.
    - headers (dict): HTTP headers to include in the request.
    - method (str): HTTP method to use (e.g., 'GET', 'POST', 'PUT', 'DELETE').
    - data: Data to include in the request body for methods like POST and PUT.

    Returns:
    - requests.Response: The response object returned by the API.
    """
    try:
        response = requests.request(
            method, api_url, params=params, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None


def unix_time_to_datetime(unix_time, timezone='Etc/GMT+3'):
    """
    Convert Unix time to datetime object in a specific timezone.

    Parameters:
    - unix_time (int): Unix timestamp.
    - timezone (str): Timezone (default is 'GMT-3').

    Returns:
    - datetime.datetime: Datetime object in the specified timezone.
    """
    tz = pytz.timezone(timezone)
    return datetime.fromtimestamp(unix_time, tz)


def get_data(location):
    url = 'http://api.weatherapi.com/v1/current.json?key=' + \
        api_key + '&q=' + str(location)
    loc_json = call_api(url)
    loc_date, loc_temp = unix_time_to_datetime(
        loc_json['current']['last_updated_epoch']), loc_json['current']['temp_c']
    return loc_date, loc_temp


def log_data(file_path, new_line):

    with open(file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(new_line)


def fill():
    for location in locations:
        my_tuple = get_data(location)
        newline = [location, str(my_tuple[0]), str(my_tuple[1])]
        log_data('/opt/airflow/data/mediciones.csv', newline)


with DAG(
    default_args=default_args,
    dag_id="dag_with_python_weather_v01",
    start_date=datetime(2023, 12, 13, 17),
    schedule_interval='@hourly'
) as dag:
    task1 = PythonOperator(
        task_id='fill',
        python_callable=fill
    )

    task1
