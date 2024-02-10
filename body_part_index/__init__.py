"""Body Part Index"""

__version__ = "0.1.0"
from .body_part import WHOLE_BODY_ID, BodyPart, Code  # noqa: F401
from .body_part_index import BodyPartIndex  # noqa: F401

BODY_PART_INDEX_DATA_URL = "https://raw.githubusercontent.com/talkasab/anatomiclocations.org/main/data/body_parts.json"
