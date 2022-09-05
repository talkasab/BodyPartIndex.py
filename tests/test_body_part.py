import pytest
from body_part_index import BodyPartIndex, BodyPart
from body_part_index.body_part import BodyPartData, Code

def test_make_body_part():
    """Make sure we can make a BodyPart.
    """
    body_part: BodyPartData = BodyPartData('RID2507', 'pelvis', contained_by_id='RID39569')
    assert isinstance(body_part, BodyPartData)
    assert body_part.radlex_id == 'RID2507'
    assert body_part.description == 'pelvis'

def test_insufficient_arguments():
    """Make sure we get an error if we don't provide enough arguments.
    """
    with pytest.raises(TypeError):
        _: BodyPartData = BodyPartData('RID2507', 'pelvis')

def test_make_body_part_with_index(sample_body_part_index: BodyPartIndex):
    """Make sure we can make a BodyPart with an index.
    """
    body_part: BodyPart = BodyPart(sample_body_part_index, 'RID2507', 'pelvis', 'RID39569')
    assert isinstance(body_part, BodyPart)
    assert body_part.radlex_id == 'RID2507'

@pytest.mark.parametrize('radlex_id, description, contained_by_id', 
                         [("RID2507", "pelvis", "RID39569"),
                          ("RID39569", "whole body", "RID39569"),
                          ("RID56", "abdomen", "RID39569"),
                          ("RID294", "uterine adnexa", "RID2507")])
def test_basic_properties(sample_body_part_index: BodyPartIndex, 
                                    radlex_id: str, description: str, contained_by_id: str):
    """Make sure we can get basic properties of BodyParts."""
    body_part = sample_body_part_index.get_by_id(radlex_id)
    actual = (body_part.radlex_id, body_part.description, body_part.contained_by_id)
    expected = (radlex_id, description, contained_by_id)
    assert actual == expected
    
def test_codes(sample_body_part_index: BodyPartIndex):
    """Make sure we can get codes for BodyParts."""
    body_part = sample_body_part_index.get_by_id('RID2507')
    actual = body_part.codes
    expected = [Code('FMA', '9578'), Code('SNOMED', '12921003'), Code('MESH', 'A01.923.600'), Code('UMLS', 'C0030797')]
    assert actual == expected