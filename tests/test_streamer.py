from energy_den import deserialize_json, serialize_json


def test_deserialize_json():
    """Tests for the deserialize_json function"""
    json_data = deserialize_json(
        "tests/data/ElectricityProdex5MinRealtime__2022-11-01T00:00_2022-11-01T00:10.json"
    )
    assert isinstance(json_data, dict)
    assert json_data["dataset"] == "ElectricityProdex5MinRealtime"
    assert json_data["total"] == 4
    assert json_data["sort"] == "Minutes5UTC DESC"


def test_serializa_json():
    """Tests for the serialize_json function"""
    json_data = deserialize_json(
        "tests/data/ElectricityProdex5MinRealtime__2022-11-01T00:00_2022-11-01T00:10.json"
    )
    json_string = serialize_json(json_data)
    assert isinstance(json_string, bytes)