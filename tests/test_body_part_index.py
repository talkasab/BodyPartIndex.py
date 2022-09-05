from body_part_index import __version__, BodyPartIndex, BodyPart, WHOLE_BODY_ID


def test_version():
    """Make sure we get the correct version number.
    """
    assert __version__ == '0.1.0'

def test_initialize_with_filename(sample_json_data_filename: str):
    """Make sure we can initialize the index with a filename.
    """
    if BodyPartIndex.is_initialized():
        BodyPartIndex.reset_instance()
    bpi: BodyPartIndex = BodyPartIndex(json_filename=sample_json_data_filename)
    assert len(bpi.get_all_body_parts()) == 6

def test_initialize_with_data(sample_json_data: dict):
    """Make sure we can initialize the index with JSON data.
    """
    if BodyPartIndex.is_initialized():
        BodyPartIndex.reset_instance()
    bpi: BodyPartIndex = BodyPartIndex(json_data=sample_json_data)
    assert len(bpi.get_all_body_parts()) == 6
    
def test_get_all_body_parts(sample_body_part_index: BodyPartIndex):
    """Make sure we get the correct BodyParts.
    """
    expected_body_parts: Set[str] = {'RID2507', 'RID294', 'RID294_RID5824', 'RID294_RID5825', 'RID39569', 'RID56'}
    actual_body_parts: Set[str] = {bp.radlex_id for bp in sample_body_part_index.get_all_body_parts()}
    assert actual_body_parts == expected_body_parts

def test_get_by_id(sample_body_part_index: BodyPartIndex):
    """Make sure we can get a BodyPart by ID.
    """
    body_part: BodyPart = sample_body_part_index.get_by_id(WHOLE_BODY_ID)
    assert isinstance(body_part, BodyPart)
    assert body_part.radlex_id == WHOLE_BODY_ID
    assert body_part.description == 'whole body'
