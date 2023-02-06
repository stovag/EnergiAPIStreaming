"""Module to send json data to kafka
"""

import json

from kafka import KafkaProducer


def deserialize_json(json_file):
    """Method to deserialize a json file into a dict

    Args:
        json_file (str): path to the json file

    Returns:
        dict: deserialized dict from json
    """
    with open(json_file, "r", encoding="UTF-8") as file_object:
        json_data = json.load(file_object)
        return json_data


def serialize_json(json_data):
    """Method to get the needed data from the json and
        serialize it into a string

    Args:
        json_data (dict): Deserialized dictionary with data from the json object

    Returns:
        str: Json string with the needed data
    """
    json_data_records = json_data["records"]
    json_data_bitstring = json.dumps(json_data_records).encode("utf-8")
    return json_data_bitstring


def send_data_to_kafka(bootstrap_server, topic, json_data_string):
    """Method to stream data to a kafka topic

    Args:
        bootstrap_server (str): Configuration for the kafka bootstrap server
        topic (str): kafka topic Data will be streamed to
        json_data_string (str): String of json data
    """
    producer = KafkaProducer(bootstrap_servers=[bootstrap_server])
    producer.send(topic, json_data_string)
    producer.flush()
    producer.close()