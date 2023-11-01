# pylint: disable=missing-module-docstring
import pytest
from body_part_index import BodyPartIndex, BodyPart, WHOLE_BODY_ID
from body_part_index.body_part import BodyPartData, Code

# pylint: disable=no-name-in-module
from . import (
    ABDOMEN_ID,
    PELVIS_ID,
    UTERINE_ADNEXA_ID,
    LEFT_UTERINE_ADNEXA_ID,
    RIGHT_UTERINE_ADNEXA_ID,
    FEMALE_GENITAL_SYSTEM_ID,
    NIPPLE_OF_MALE_BREAST_ID,
    AREOLA_OF_MALE_BREAST_ID,
    OVARIAN_ARTERY_ID,
    RIGHT_OVARIAN_ARTERY_ID,
)

# pylint: enable=no-name-in-module


def test_make_body_part():
    """Make sure we can make a BodyPart."""
    body_part: BodyPartData = BodyPartData(PELVIS_ID, 'pelvis', contained_by_id=WHOLE_BODY_ID)
    assert isinstance(body_part, BodyPartData)
    assert body_part.radlex_id == PELVIS_ID
    assert body_part.description == 'pelvis'


def test_insufficient_arguments():
    """Make sure we get an error if we don't provide enough arguments."""
    with pytest.raises(TypeError):
        # pylint: disable=no-value-for-parameter
        _: BodyPartData = BodyPartData(PELVIS_ID, 'pelvis')
        # pylint: enable=no-value-for-parameter


def test_make_body_part_with_index(sample_body_part_index: BodyPartIndex):
    """Make sure we can make a BodyPart with an index."""
    body_part: BodyPart = BodyPart(sample_body_part_index, PELVIS_ID, 'pelvis', WHOLE_BODY_ID)
    assert isinstance(body_part, BodyPart)
    assert body_part.radlex_id == PELVIS_ID


@pytest.mark.parametrize(
    'radlex_id, description, contained_by_id',
    [
        (PELVIS_ID, 'pelvis', WHOLE_BODY_ID),
        (WHOLE_BODY_ID, 'whole body', WHOLE_BODY_ID),
        (ABDOMEN_ID, 'abdomen', WHOLE_BODY_ID),
        (UTERINE_ADNEXA_ID, 'uterine adnexa', PELVIS_ID),
    ],
)
def test_basic_properties(
    sample_body_part_index: BodyPartIndex, radlex_id: str, description: str, contained_by_id: str
):
    """Make sure we can get basic properties of BodyParts."""
    body_part = sample_body_part_index.get_by_id(radlex_id)
    actual = (body_part.radlex_id, body_part.description, body_part.contained_by_id)
    expected = (radlex_id, description, contained_by_id)
    assert actual == expected


def test_parents(sample_body_part_index: BodyPartIndex):
    """Make sure we can get the BodyPart that contains another BodyPart."""
    body_part = sample_body_part_index.get_by_id(PELVIS_ID)
    assert body_part.contained_by == sample_body_part_index.get_by_id(WHOLE_BODY_ID)
    body_part2 = sample_body_part_index.get_by_id(UTERINE_ADNEXA_ID)
    assert body_part2.part_of == sample_body_part_index.get_by_id(FEMALE_GENITAL_SYSTEM_ID)
    body_part3 = sample_body_part_index.get_by_id(PELVIS_ID)
    assert body_part3.part_of is None


def test_synonyms(sample_body_part_index: BodyPartIndex):
    """Make sure we can get synonyms for BodyParts."""
    body_part = sample_body_part_index.get_by_id(PELVIS_ID)
    assert body_part.synonyms == ['lesser pelvis', 'pelvis minor', 'true pelvis']


def test_codes(sample_body_part_index: BodyPartIndex):
    """Make sure we can get codes for BodyParts."""
    body_part = sample_body_part_index.get_by_id(PELVIS_ID)
    expected = [
        Code('FMA', '9578'),
        Code('SNOMED', '12921003'),
        Code('MESH', 'A01.923.600'),
        Code('UMLS', 'C0030797'),
    ]
    assert body_part.codes == expected


def test_sidedness(sample_body_part_index: BodyPartIndex):
    """Make sure we can get unsided, left, and right versions of BodyParts."""
    unsided = sample_body_part_index.get_by_id(UTERINE_ADNEXA_ID)
    left = sample_body_part_index.get_by_id(LEFT_UTERINE_ADNEXA_ID)
    right = sample_body_part_index.get_by_id(RIGHT_UTERINE_ADNEXA_ID)
    assert unsided.left == left
    assert unsided.right == right
    assert unsided.unsided is None
    assert left.left is None
    assert left.right == right
    assert left.unsided == unsided
    assert right.left == left
    assert right.right is None
    assert right.unsided == unsided


def test_children(sample_body_part_index: BodyPartIndex):
    """Make sure we can get the BodyParts that are contained by another BodyPart."""
    body_part = sample_body_part_index.get_by_id(WHOLE_BODY_ID)
    expected = {
        sample_body_part_index.get_by_id(ABDOMEN_ID),
        sample_body_part_index.get_by_id(PELVIS_ID),
    }
    assert body_part.children == expected


def test_descendants(sample_body_part_index: BodyPartIndex):
    """Make sure we can get the all the BodyParts that are contained by another BodyPart."""
    body_part = sample_body_part_index.get_by_id(WHOLE_BODY_ID)
    expected = {
        sample_body_part_index.get_by_id(ABDOMEN_ID),
        sample_body_part_index.get_by_id(PELVIS_ID),
        sample_body_part_index.get_by_id(UTERINE_ADNEXA_ID),
        sample_body_part_index.get_by_id(LEFT_UTERINE_ADNEXA_ID),
        sample_body_part_index.get_by_id(RIGHT_UTERINE_ADNEXA_ID),
        sample_body_part_index.get_by_id(FEMALE_GENITAL_SYSTEM_ID),
        sample_body_part_index.get_by_id(OVARIAN_ARTERY_ID),
        sample_body_part_index.get_by_id(RIGHT_OVARIAN_ARTERY_ID)
    }
    assert body_part.descendants == expected

def test_is_contained(sample_body_part_index: BodyPartIndex):
    """Ensure True when other BodyPart is in this BodyPart's ancestry.
        Ensure False when other BodyPart is not contained in this BodyPart's ancestry.
    """ 
    body_part1 = sample_body_part_index.get_by_id(ABDOMEN_ID)
    body_part2 = sample_body_part_index.get_by_id(WHOLE_BODY_ID)
    body_part3 = sample_body_part_index.get_by_id(RIGHT_UTERINE_ADNEXA_ID)

    assert body_part1.is_contained(body_part2) == True
    assert body_part1.is_contained(body_part3) == False

def test_snomed_code_direct_assignment(sample_body_part_index: BodyPartIndex):
    """Test snomed_code property when SNOMED code is directly assigned."""
    body_part = sample_body_part_index.get_by_id(RIGHT_UTERINE_ADNEXA_ID)
    assert body_part.snomed_code == '110634007'

def test_snomed_code_unsided_version(sample_body_part_index: BodyPartIndex):
    """Test snomed_code property when SNOMED code is obtained from the unsided version."""
    body_part = sample_body_part_index.get_by_id(RIGHT_OVARIAN_ARTERY_ID)  
    assert body_part.snomed_code == '12052000'

def test_snomed_code_immediate_parent(sample_body_part_index: BodyPartIndex):
    """Test snomed_code property when SNOMED code is obtained from the immediate parent."""
    body_part = sample_body_part_index.get_by_id(AREOLA_OF_MALE_BREAST_ID)  
    assert body_part.snomed_code == '67770001'

def test_no_snomed_code(sample_body_part_index: BodyPartIndex):
    """Test snomed_code property when no SNOMED code is available."""
    body_part = sample_body_part_index.get_by_id(NIPPLE_OF_MALE_BREAST_ID)
    assert body_part.snomed_code is None
