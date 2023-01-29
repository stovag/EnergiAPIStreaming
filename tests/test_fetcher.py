"""Tests for the functions in the fetcher module
"""

import re
import os
import json

import pytest

from energy_den import generate_query_real_time, generate_query_from_range, fetch_data

DATETIME_PATTERN = "_\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}_\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}"

def test_generate_query_real_time():
    """Tests for generate_query_real_time function"""
    assert isinstance(generate_query_real_time("%Y-%m-%dT%H:%M"), tuple)
    assert isinstance(generate_query_real_time("%Y-%m-%dT%H:%M")[0], str)
    assert isinstance(generate_query_real_time("%Y-%m-%dT%H:%M")[1], str)
    assert (
        "https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime"
        in generate_query_real_time("%Y-%m-%dT%H:%M")[0]
    )
    assert re.search(DATETIME_PATTERN, generate_query_real_time("%Y-%m-%dT%H:%M")[1])

def test_generate_query_from_range():
    """Tests for the generate query_from_range functions"""

    # Happy Path
    assert generate_query_from_range(
        "2022-11-01", "2022-11-02", "%Y-%m-%d", "%Y-%m-%dT%H:%M"
    ) == (
        "https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime?offset=0&start=2022-11-01T00:00&end=2022-11-02T00:00&sort=Minutes5UTC%20DESC&timezone=dk",
        "_2022-11-01T00:00_2022-11-02T00:00",
    )

    assert generate_query_from_range(
        "2022-11-01T00:00", "2022-11-01T00:10", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M"
    ) == (
        "https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime?offset=0&start=2022-11-01T00:00&end=2022-11-01T00:10&sort=Minutes5UTC%20DESC&timezone=dk",
        "_2022-11-01T00:00_2022-11-01T00:10",
    )

    # Test date start < date end
    with pytest.raises(ValueError):
        generate_query_from_range("2022-11-02", "2022-11-01", "%Y-%m-%d", "%Y-%m-%dT%H:%M")

    with pytest.raises(TypeError):
        generate_query_from_range(5, "2020-11-01", "%Y-%m-%d", "%Y-%m-%dT%H:%M")

def test_fetch_data():
    """Tests for the fetch_data function. Also tests for data concistency
    """
    query, file_datetime = generate_query_from_range(
        "2022-11-01T00:00", "2022-11-01T00:10", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M"
    )
    filepath = fetch_data(query, file_datetime, "./tests/data/")
    print(filepath)
    assert isinstance(filepath, str)
    assert re.search(DATETIME_PATTERN, filepath)
    assert os.path.exists(filepath)
    assert ".json" in filepath
    assert os.stat(filepath).st_size > 0

    with open(filepath, "r", encoding="UTF-8") as file_object:
        json_data = json.load(file_object)

    assert "total" in json_data
    assert "sort" in json_data
    assert "dataset" in json_data
    assert "records" in json_data

    sample_record = json_data["records"][0]

    assert "Minutes5UTC" in sample_record
    assert "Minutes5DK" in sample_record
    assert "PriceArea" in sample_record
    assert "ProductionLt100MW" in sample_record
    assert "ProductionGe100MW" in sample_record
    assert "OffshoreWindPower" in sample_record
    assert "OnshoreWindPower" in sample_record
    assert "ExchangeGreatBelt" in sample_record
    assert "ExchangeGermany" in sample_record
    assert "ExchangeNetherlands" in sample_record
    assert "ExchangeNorway" in sample_record
    assert "ExchangeSweden" in sample_record
    assert "BornholmSE4" in sample_record
    assert "SolarPower" in sample_record
