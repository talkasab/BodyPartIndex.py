# pylint: disable=missing-module-docstring
from typing import Set
from body_part_index import __version__, BodyPartIndex, BodyPart, WHOLE_BODY_ID
from . import ABDOMEN_ID, PELVIS_ID, UTERINE_ADNEXA_ID, LEFT_UTERINE_ADNEXA_ID, RIGHT_UTERINE_ADNEXA_ID, \
    FEMALE_GENITAL_SYSTEM_ID # pylint: disable=no-name-in-module


def test_version():
    """Make sure we get the correct version number."""
    assert __version__ == '0.1.0'


def test_initialize_with_filename(sample_json_data_filename: str):
    """Make sure we can initialize the index with a filename."""
    if BodyPartIndex.is_initialized():
        BodyPartIndex.reset_instance()
    bpi: BodyPartIndex = BodyPartIndex(json_filename=sample_json_data_filename)
    assert len(bpi.get_all_body_parts()) == 7


def test_initialize_with_data(sample_json_data: dict):
    """Make sure we can initialize the index with JSON data."""
    if BodyPartIndex.is_initialized():
        BodyPartIndex.reset_instance()
    bpi: BodyPartIndex = BodyPartIndex(json_data=sample_json_data)
    assert len(bpi.get_all_body_parts()) == 7


def test_get_all_body_parts(sample_body_part_index: BodyPartIndex):
    """Make sure we get the correct BodyParts."""
    expected_body_parts: Set[str] = {
        PELVIS_ID,
        UTERINE_ADNEXA_ID,
        LEFT_UTERINE_ADNEXA_ID,
        RIGHT_UTERINE_ADNEXA_ID,
        WHOLE_BODY_ID,
        ABDOMEN_ID,
        FEMALE_GENITAL_SYSTEM_ID,
    }
    actual_body_parts: Set[str] = {
        bp.radlex_id for bp in sample_body_part_index.get_all_body_parts()
    }
    assert actual_body_parts == expected_body_parts


def test_get_by_id(sample_body_part_index: BodyPartIndex):
    """Make sure we can get a BodyPart by ID."""
    body_part: BodyPart = sample_body_part_index.get_by_id(WHOLE_BODY_ID)
    assert isinstance(body_part, BodyPart)
    assert body_part.radlex_id == WHOLE_BODY_ID
    assert body_part.description == 'whole body'


# Test the BodyPartIndex get() method that looks across all the IDs and code values
def test_get(sample_body_part_index: BodyPartIndex):
    """Make sure we get BodyParts by ID or code value."""
    body_part: BodyPart = sample_body_part_index.get(PELVIS_ID)
    assert isinstance(body_part, BodyPart)
    assert body_part.radlex_id == PELVIS_ID
    assert body_part.description == 'pelvis'

    body_part = sample_body_part_index.get('818983003')
    assert isinstance(body_part, BodyPart)
    assert body_part.radlex_id == ABDOMEN_ID
    assert any(c.code == '818983003' for c in body_part.codes)


# Test the BodyPartIndex search() method that looks at the description and synonyms
def test_search(sample_body_part_index: BodyPartIndex):
    """Make sure we can search for BodyParts by description or synonym."""
    # Search for a description
    search_results = sample_body_part_index.search('abdomen')
    assert {r.radlex_id for r in search_results} == {ABDOMEN_ID}
    # Search for a synonym
    search_results2 = list(sample_body_part_index.search('true pelvis'))
    assert {r.radlex_id for r in search_results2} == {PELVIS_ID}
    # Search for a partial
    search_results3 = sample_body_part_index.search('adnexa')
    assert len(search_results3) == 3
    expected = {UTERINE_ADNEXA_ID, LEFT_UTERINE_ADNEXA_ID, RIGHT_UTERINE_ADNEXA_ID}
    assert {r.radlex_id for r in search_results3} == expected
