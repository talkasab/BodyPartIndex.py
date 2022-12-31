"""Contains the BodyPart class and associated types."""

from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, NamedTuple, Optional, Set, Iterable, Protocol, List, Tuple

WHOLE_BODY_ID = "RID39569"
SEXES = ("Female", "Male")
INDEX_FUNCTIONS = ('get_by_id', 'get_all_body_parts')


class Code(NamedTuple):
    """A Code is a tuple of (sysem, code)."""
    system: str
    code: str

    @staticmethod
    def from_dict(code_dict: Dict) -> "Code":
        """Generate a Code from a dict with "system" and "code" keys."""
        return Code(code_dict["system"], code_dict["code"])


@dataclass(frozen=True)
class BodyPartData:
    """A BodyPartData is a tuple of at least (radlex_id, description, contained_by_id) and optional
       codes, synonyms, sided IDs, part_of_id, and sex specificity.

    Args:
        radlex_id (str): Main identifier for the object
        description (str): Preferred term for the concept (from RadLe)
        contained_by_id (str): Parent object in the anatomic location hierarchy
        codes (Iterable[Dict[str, str]], optional): List of codes for the concept, where each
                element is a dict like {"system": "SNOMED", "code": "xxxxxx"}. Defaults to None.
        synonyms (Iterable[str], optional): List of synonyms for the concept. Defaults to None.
        unsided_id (str, optional): Identifier for the unsided version of the concept. Defaults to None.
        left_id (str, optional): Identifier for the left-sided version of the concept. Defaults to None.
        right_id (str, optional): Identifier for the right-sided version of the concept. Defaults to None.
        part_of_id (str, optional): Identifier for the part-of version of the concept. Defaults to None.
        sex_specific (str, optional): Indicates whether the concept is associated with a sex phenotype.

    """
    radlex_id: str
    description: str = field(hash=False, compare=False)
    contained_by_id: str = field(hash=False, compare=False)
    codes: Optional[Iterable[Code]] = field(default=None, hash=False, compare=False)
    synonyms: Optional[Iterable[str]] = field(default=None, hash=False, compare=False)
    unsided_id: Optional[str] = field(default=None, hash=False, compare=False)
    left_id: Optional[str] = field(default=None, hash=False, compare=False)
    right_id: Optional[str] = field(default=None, hash=False, compare=False)
    part_of_id: Optional[str] = field(default=None, hash=False, compare=False)
    sex_specific: Optional[str] = field(default=None, hash=False, compare=False)

    def __str__(self) -> str:
        return f"{self.radlex_id}: {self.description}"

    @staticmethod
    def params_from_json_dict(body_part_dict: Dict) -> Tuple[List[str], Dict[str, any]]:
        """Generate arguments for BodyPartData constructor from a JSON dict.

            Args:
                body_part_dict (Dict): JSON dict with keys "radlex_id", "description", "contained_by_id",
                    "codes", "synonyms", "unsided_id", "left_id", "right_id", "part_of_id", and "sex_specific".

            Returns:
                (args, kwargs) (tupel of List and Dict): arguments and keyword-arguments for the BodyPartData
                    constructor.
        """
        args: List = (body_part_dict["radlexId"], body_part_dict["description"], body_part_dict["containedById"])
        kwargs: Dict[str, any] = {}
        code_dicts = body_part_dict.get("codes", None)
        if code_dicts is not None:
            kwargs["codes"] = [Code(**code_dict) for code_dict in code_dicts]
        synonyms = body_part_dict.get("synonyms", None)
        if synonyms is not None and len(synonyms) > 0:
            kwargs["synonyms"] = synonyms
        if "unsidedId" in body_part_dict:
            kwargs["unsided_id"] = body_part_dict["unsidedId"]
        if "leftId" in body_part_dict:
            kwargs["left_id"] = body_part_dict["leftId"]
        if "rightId" in body_part_dict:
            kwargs["right_id"] = body_part_dict["rightId"]
        if "partOfId" in body_part_dict:
            kwargs["part_of_id"] = body_part_dict["partOfId"]
        if "sexSpecific" in body_part_dict:
            kwargs["sex_specific"] = body_part_dict["sexSpecific"]
        return (args, kwargs)

class Index(Protocol):
    """Signature of an object that can be used by BodyPart to find its related objects."""
    def get_by_id(self, radlex_id: str) -> 'BodyPart': ... # pylint: disable=missing-function-docstring

    def get_all_body_parts(self) -> Iterable['BodyPart']: ...# pylint: disable=missing-function-docstring

class BodyPart(BodyPartData):
    """ "Body part object representing a node in the anatomic location hierarchy."""

    def __init__(self, index: Index, radlex_id: str, description: str, contained_by_id: str, /,
                 codes: Optional[Iterable[Code]] = None, synonyms: Optional[Iterable[str]] = None,
                 unsided_id: Optional[str] = None, left_id: Optional[str] = None, right_id: Optional[str] = None,
                 part_of_id: Optional[str]=None, sex_specific: str = None) -> None:
        """Initialize a BodyPart object, representing an anatomic location, with associated information.

        Args:
            radlex_id (str): Main identifier for the object
            description (str): Preferred term for the concept (from RadLe)
            contained_by_id (str): Parent object in the anatomic location hierarchy
            index (BodyPartIndex-like): Typically a BodyPartIndex, but can be anything that offers "get_by_id" and
                   "get_all_body_parts" methods.
            codes (Iterable[Code], optional): List of codes for the concept, where each
                   element is a dict like {"system": "SNOMED", "code": "xxxxxx"}. Defaults to None.
            synonyms (Iterable[str], optional): List of synonyms for the concept. Defaults to None.
            unsided_id (str, optional): Identifier for the unsided version of the concept. Defaults to None.
            left_id (str, optional): Identifier for the left-sided version of the concept. Defaults to None.
            right_id (str, optional): Identifier for the right-sided version of the concept. Defaults to None.
            part_of_id (str, optional): Identifier for the part-of version of the concept. Defaults to None.
            sex_specific (str, optional): Indicates whether the concept is associated with a sex phenotype.

        Raises:
            Exception: When one of the arguments is inappropriate
        """
        # Mandatory arguments
        super().__init__(radlex_id=radlex_id, description=description, contained_by_id=contained_by_id, codes=codes,
                         synonyms=synonyms, unsided_id=unsided_id, left_id=left_id, right_id=right_id,
                         part_of_id=part_of_id, sex_specific=sex_specific)
        for method in INDEX_FUNCTIONS:
            if not callable(getattr(index, method, None)):
                raise ValueError(f"index must be a BodyPartIndex or at least implement {method}() (got {index})")
        self._index: Index = index

    @cached_property
    def contained_by(self) -> 'BodyPart':
        """BodyPart: Parent object in the anatomic location (contained by) hierarchy"""
        return self._index.get_by_id(self.contained_by_id)

    @cached_property
    def part_of(self) -> Optional['BodyPart']:
        """BodyPart: Parent object in the part of hierarchy"""
        return self._index.get_by_id(self.part_of_id) if self.part_of_id is not None else None

    @cached_property
    def left(self) -> Optional['BodyPart']:
        """BodyPart: Left-sided version of the concept"""
        return self._index.get_by_id(self.left_id) if self.left_id is not None else None

    @cached_property
    def right(self) -> Optional['BodyPart']:
        """BodyPart: Right-sided version of the concept"""
        return self._index.get_by_id(self.right_id) if self.right_id is not None else None

    @cached_property
    def unsided(self) -> Optional['BodyPart']:
        """BodyPart: Unisided version of the concept"""
        return self._index.get_by_id(self.unsided_id) if self.unsided_id is not None else None

    @cached_property
    def children(self) -> Set['BodyPart']:
        """Returns the set of children of this BodyPart."""
        return set(filter(self.is_child, self._index.get_all_body_parts()))

    @cached_property
    def descendants(self) -> Set['BodyPart']:
        """Returns the set of descendants of this BodyPart."""
        descendants: Set['BodyPart'] = set(self.children)
        for child in self.children:
            descendants.update(child.descendants)
        return descendants

    @cached_property
    def ancestors(self) -> List['BodyPart']:
        """Returns the set of ancestors of this BodyPart."""
        if self.radlex_id == WHOLE_BODY_ID:
            return []
        return [self.contained_by] + self.contained_by.ancestors

    def is_child(self, other: 'BodyPart') -> bool:
        """Check if the other BodyPart is a child of this one.

        Args:
            other (BodyPart): BodyPart to check against

        Returns:
            bool: True if other is a parent of this one, False otherwise
        """
        return other.contained_by_id == self.radlex_id  # pylint: disable=protected-access
