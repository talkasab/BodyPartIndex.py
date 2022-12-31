# pylint: disable=missing-module-docstring
import os
import json
import pytest

from body_part_index.body_part_index import BodyPartIndex

SAMPLE_BODYPARTS_FILENAME='sample_body_parts.json'

def get_filename_in_tests_dir(filename: str) -> str:
    """Returns the sample json data filename for the tests."""
    return os.path.join(os.path.dirname(__file__), filename)

@pytest.fixture
def sample_json_data_filename() -> str:
    """Returns the sample json data filename for the tests."""
    return get_filename_in_tests_dir(SAMPLE_BODYPARTS_FILENAME)

@pytest.fixture
def sample_json_data():
    """Returns the sample json data for the tests."""
    with open(get_filename_in_tests_dir(SAMPLE_BODYPARTS_FILENAME), encoding='utf-8') as json_file:
        return json.load(json_file)

@pytest.fixture
def sample_body_part_index():
    """Returns a sample BodyPartIndex for the tests."""
    if BodyPartIndex.is_initialized():
        return BodyPartIndex.get_instance()
    return BodyPartIndex(json_filename=get_filename_in_tests_dir(SAMPLE_BODYPARTS_FILENAME))
