"""Basic Functionalities for fetching data from the ElectricityProdex5MinRealtime API

    Raises:
        AttributeError: _description_
"""
import json
from datetime import datetime, timedelta

import requests


def generate_query_real_time(datetime_format):
    """Function to generate the query and filepath for the data generated
    in the last 5 minutes from the ElectricityProdex5MinRealtime API.

    Args:
        datetime_format (str, optional): Format of the datetime used
                                         in the API query. Defaults to "%Y-%m-%dT%H:%M:%S".

    Returns:
        tuple (query, file_datetime):
            WHERE:
            query (str): The query to be used to call the API
            file_datetime (str): Datetime range from the data, used for logging"""

    # Get time in Danish TimeZone
    end_datetime = datetime.now() - timedelta(hours=1)
    start_datetime = end_datetime - timedelta(minutes=5)
    start_datetime_query = start_datetime.strftime(datetime_format)
    end_datetime_query = end_datetime.strftime(datetime_format)
    base_api_url = (
        "https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime"
    )
    query_parameters = (
        f"?offset=0&start={start_datetime_query}&end={end_datetime_query}"
    )
    standard_parameters = "&sort=Minutes5UTC%20DESC&timezone=dk"
    query = base_api_url + query_parameters + standard_parameters
    file_datetime = f"_{start_datetime_query}_{end_datetime_query}"

    return query, file_datetime


def generate_query_from_range(
    start_date_str,
    end_date_str,
    date_format="%Y-%m-%d",
    datetime_format="%Y-%m-%dT%H:%M",
):
    """Function to generate the query and filepath for the data generated
    in the given datetime range from the ElectricityProdex5MinRealtime API.

    Args:
        start_date_str (str, optional): First datetime to collect data for. Defaults to None.
        end_date_str (str, optional): Last datetime to collect data for. Defaults to None.
        date_format (str, optional): Format of the datetime inputs. Defaults to "%Y-%m-%d".
        datetime_format (str, optional): Format of the datetime used
                                         in the API query. Defaults to "%Y-%m-%dT%H:%M".

    Returns:
        tuple (query, file_datetime):
            WHERE:
            query (str): The query to be used to call the API
            file_datetime (str): Datetime range from the data, used for logging"""

    if not isinstance(start_date_str, str) or not isinstance(end_date_str, str):
        raise TypeError

    start_datetime = datetime.strptime(start_date_str, date_format)
    end_datetime = datetime.strptime(end_date_str, date_format)

    if start_datetime > end_datetime:
        raise ValueError("Starting date can not be later than end date")

    start_datetime_query = start_datetime.strftime(datetime_format)
    end_datetime_query = end_datetime.strftime(datetime_format)
    base_api_url = (
        "https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime"
    )
    query_parameters = (
        f"?offset=0&start={start_datetime_query}&end={end_datetime_query}"
    )
    standard_parameters = "&sort=Minutes5UTC%20DESC&timezone=dk"
    query = base_api_url + query_parameters + standard_parameters
    file_datetime = f"_{start_datetime_query}_{end_datetime_query}"

    return query, file_datetime


def generate_query_from_interval(
    start_date_str,
    num_intevals=5,
    interval="minutes",
    date_format="%Y-%m-%d",
    datetime_format="%Y-%m-%dT%H:%M",
):
    """Function to generate the query and filepath for the data generated
     given a starting date and intervals from the ElectricityProdex5MinRealtime API.


    Args:
        start_date_str (str, required): First datetime to collect data for.
        num_intevals (int, optional): Number of intervals to collect data for. Defaults to 5.
        interval (str, optional): Type of interval, can be: "minutes", "hours", "days", or "months".
                                  Defaults to "minutes".
        date_format (str, optional): Format of the datetime inputs. Defaults to "%Y-%m-%d".
        datetime_format (str, optional): Format of the datetime used
                                         in the API query. Defaults to "%Y-%m-%dT%H:%M:%S".

    Returns:
        tuple (query, file_datetime):
            WHERE:
            query (str): The query to be used to call the API
            file_datetime (str): Datetime range from the data, used for logging
    """

    start_datetime = datetime.strptime(start_date_str, date_format)
    if interval == "minutes":
        end_datetime = start_datetime + timedelta(minutes=num_intevals)
    if interval == "hours":
        end_datetime = start_datetime + timedelta(hours=num_intevals)
    if interval == "days":
        end_datetime = start_datetime + timedelta(days=num_intevals)
    if interval == "months":
        end_datetime = start_datetime + timedelta(months=num_intevals)

    start_datetime_query = start_datetime.strftime(datetime_format)
    end_datetime_query = end_datetime.strftime(datetime_format)
    base_api_url = (
        "https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime"
    )
    query_parameters = (
        f"?offset=0&start={start_datetime_query}&end={end_datetime_query}"
    )
    standard_parameters = "&sort=Minutes5UTC%20DESC&timezone=dk"
    query = base_api_url + query_parameters + standard_parameters
    file_datetime = f"_{start_datetime_query}_{end_datetime_query}"

    return query, file_datetime


def fetch_data(query, file_datetime, directory):
    """Fetch data from the query and save them in the file spacified by the date ranges

    Args:
        query (str): API query generated from the other functions in the package
        file_datetime (str): Datetime specifing the range the data is from
        directory (str, optional): The directory data will be stored in.
                                   Defaults to "./data/productionapi/"
    """
    response = requests.get(query, timeout=10)
    filepath = directory + f"ElectricityProdex5MinRealtime_{file_datetime}.json"
    with open(filepath, "w+", encoding="UTF-8") as file_object:
        json.dump(response.json(), file_object, ensure_ascii=False)
    return filepath
