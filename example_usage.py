"""Example usage of the witsidedev python module
"""

import toml

import energy_den as ed

config = toml.load("config.toml")

query, file_datetime = ed.generate_query_real_time(
    config["energy_api"]["datetime_format"]
)
ed.fetch_data(query, file_datetime, config["energy_api"]["directory"])
