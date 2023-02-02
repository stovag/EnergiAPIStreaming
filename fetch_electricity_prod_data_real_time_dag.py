"""_summary_
"""

from datetime import datetime, timedelta

import toml
import energy_den as ed
import logging

from airflow import DAG
from airflow.models.variable import Variable
from airflow.operators.python_operator import PythonOperator

with DAG(
    "get_electricity_production_data_real_time",
    description="DAG for fetching data from the Energy Production API",
    schedule_interval="*/5 * * * *",
    start_date=datetime(2022, 10, 26),
    catchup=False,
) as dag:

    # Get Denmark Time
    datetime_now = datetime.now()
    datetime_den = datetime_now - timedelta(hours=1) 
    time = datetime_den.strftime("%Y-%m-%d_%H_%M_%S")
    config = toml.load("/home/stovag/big_data/module/config.toml")

    def get_data():
        """Function to get data from the ElectricityProdex5MinRealtime API using
        Witside's internal module
        """
        query, file_datetime = ed.generate_query_real_time(
            config["energy_api"]["datetime_format"]
        )
        json_filepath = ed.fetch_data(
            query, file_datetime, config["energy_api"]["directory"]
        )
        Variable.set("file_created", json_filepath)
        logging.info(query)

    save_data_to_file = PythonOperator(
        task_id="get_electricity_production_data_real_time",
        python_callable=get_data,
        dag=dag,
    )

    def stream_to_kafka():

        bootstrap_server = config["kafka"]["bootstrap_server"]
        topic = config["kafka"]["topic"]

        json_filepath = Variable.get("file_created")
        json_data = ed.deserialize_json(json_filepath)
        json_data_string = ed.serialize_json(json_data)
        ed.send_data_to_kafka(bootstrap_server, topic, json_data_string)

    stream_data_to_kafka = PythonOperator(
        task_id="stream_energy_data_to_kafka",
        python_callable=stream_to_kafka,
        dag=dag,
    )

    save_data_to_file >> stream_data_to_kafka
