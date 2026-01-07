from dagster import Definitions, asset

@asset
def raw_data():
    """
    This asset represents raw data.
    In a real scenario, this might fetch data from SFTP.
    """
    return [1, 2, 3, 4, 5]

@asset
def processed_data(raw_data):
    """
    This asset depends on raw_data.
    It simulates a transformation step.
    """
    return [x * 10 for x in raw_data]

defs = Definitions(
    assets=[raw_data, processed_data],
)
