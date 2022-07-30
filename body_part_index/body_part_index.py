"""Routines to pull in the information/hierarchy of BodyPart objects from the standard library."""
import json
from .body_part import BodyPart

__index = {}
WHOLE_BODY_ID = "RID39569"
WHOLE_BODY = BodyPart(WHOLE_BODY_ID, "whole body", WHOLE_BODY_ID, codes=[
                      {"system": "SNOMED", "code": "COO17421"}])


def initialize(config={}) -> None:
    __index[WHOLE_BODY_ID] = WHOLE_BODY
    __index["RID56"] = BodyPart("RID56", "abdomen", WHOLE_BODY_ID,
                                codes=[{"system": "SNOMED", "code": "818983003"},
                                       {"system": "MESH", "code": "A01.923.047"}],
                                synonyms=["abdominopelvis",
                                          "abdominopelvic region"]
                                )
    for part in __index.values():
        contained_by = __index[part.contained_by_id]
        part.contained_by = contained_by
        contained_by.children.add(part)
        # Also need to get the partOf hierarchy
