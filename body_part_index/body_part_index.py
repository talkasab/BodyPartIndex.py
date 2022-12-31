"""Routines to pull in the information/hierarchy of BodyPart objects from the standard library."""
import gc
import json
from typing import List, Dict, Set, Iterable, Optional

from .body_part import BodyPartData
from . import BodyPart, Code

class BodyPartIndex:
    """Index of BodyPart objects, keyed by RadLex ID.

    Raises:
        Exception: If a second instance of this class is created (use get_instance() instead)
    """
    __the_instance: Optional['BodyPartIndex'] = None

    # TODO: Add ability to add local codes and synonyms
    def __init__(self, json_data: Optional[Dict] = None, json_filename: Optional[str] = None) -> None:
        if BodyPartIndex.__the_instance is not None:
            raise Exception("Singleton already initialized.  Use BodyPartIndex.get_instance() instead.")
        if json_data is None:
            if json_filename is None:
                raise Exception("Must provide either json_filename or json_data")
            json_data = self._get_json_data_from_file(json_filename)
        self._initialize(json_data)
        BodyPartIndex.__the_instance = self

    @staticmethod
    def get_instance() -> 'BodyPartIndex':
        """Get singleton instance of BodyPartIndex.

        Returns:
            BodyPartIndex: The singleton instance of BodyPartIndex
        """
        if BodyPartIndex.__the_instance is None:
            raise Exception("Singleton not initialized.  Use BodyPartIndex() instead.")
        return BodyPartIndex.__the_instance

    @staticmethod
    def reset_instance() -> None:
        """Reset the singleton instance of BodyPartIndex.
        """
        BodyPartIndex.__the_instance = None
        gc.collect()

    @staticmethod
    def is_initialized() -> bool:
        """Check if the singleton instance of BodyPartIndex has been initialized.
        """
        return BodyPartIndex.__the_instance is not None

    def _get_json_data_from_file(self, json_filename: str) -> Dict:
        with open(json_filename, encoding='utf-8') as json_file:
            return json.load(json_file)

    def _add_to_indices(self, body_part: BodyPart) -> None:
        def add_to_text_index(text: str, body_part: BodyPart) -> None:
            if text not in self.__text_index:
                self.__text_index[text] = []
            self.__text_index[text].append(body_part)
        # Harvest codes for code indices
        for code in body_part.codes:
            if code in self.__code_index:
                raise Exception(f"Duplicate BodyPart with code {code}")
            self.__code_index[code] = body_part
            if code.code in self.__code_text_index:
                raise Exception(f"Duplicate BodyPart with code text {code.code}")
            self.__code_text_index[code.code] = body_part
        # Harvest text for text indices
        add_to_text_index(body_part.radlex_id, body_part)
        add_to_text_index(body_part.description, body_part)
        if body_part.synonyms and len(body_part.synonyms) > 0:
            for synonym in body_part.synonyms:
                add_to_text_index(synonym, body_part)
        for code in body_part.codes:
            add_to_text_index(code.code, body_part)


    def _initialize(self, json_data: Dict) -> None:
        self.__index: Dict[str, BodyPart] = {}
        self.__code_index: Dict[Code, BodyPart] = {}
        self.__code_text_index: Dict[str, BodyPart] = {}
        self.__text_index: Dict[str, List[BodyPart]] = {}
        for body_part_dict in json_data["bodyParts"]:
            (args, kwargs) = BodyPartData.params_from_json_dict(body_part_dict)
            body_part: BodyPart = BodyPart(self, *args, **kwargs)
            if id in self.__index:
                raise Exception(f"Duplicate BodyPart with ID {id}")
            self.__index[body_part.radlex_id] = body_part
            self._add_to_indices(body_part)
        # TODO: Sanity check for all references
        # TODO: Sanity check that all body parts have a parent leading to WHOLE_BODY_ID

    def get_all_body_parts(self) -> Iterable[BodyPart]:
        """Get all BodyParts in the index.

        Returns:
            Iterable[BodyPart]: All BodyParts in the index
        """
        return list(self.__index.values())

    def get_by_id(self, radlex_id: str) -> BodyPart:
        """Get BodyPart object by RadLex ID.

        Args:
            id (str): RadLex ID of the BodyPart to retrieve

        Raises:
            Exception: If no BodyPart with the given ID is found

        Returns:
            BodyPart: BodyPart object with the given RadLex ID
        """
        if radlex_id not in self.__index:
            raise Exception(f"No BodyPart with ID {radlex_id}")
        return self.__index[radlex_id]

    def get_by_code(self, code: Code) -> Optional[BodyPart]:
        """Get BodyPart object by code.

        Args:
            code (str): Code of the BodyPart to retrieve

        Returns:
            BodyPart: BodyPart object with the given code (or None if not found)
        """
        if code in self.__code_index:
            return self.__code_index[code]
        return None

    def get(self, code_text_or_id: str) -> Optional[BodyPart]:
        """Get BodyPart object by code or ID.

        Args:
            code_or_id (str): Code (without system) or ID of the BodyPart to retrieve

        Returns:
            BodyPart: BodyPart object with the given code or ID
        """
        if code_text_or_id in self.__index:
            return self.__index[code_text_or_id]
        if code_text_or_id in self.__code_text_index:
            return self.__code_text_index[code_text_or_id]
        return None

    def search(self, query: str) -> Iterable[BodyPart]:
        """Search for BodyParts by query.

        Args:
            query (str): Query to search for BodyParts in description, synonyms, and codes

        Returns:
            Iterable[BodyPart]: BodyParts matching the query
        """
        # Look for partial matches
        results: Set[BodyPart] = set()
        for text, body_parts in self.__text_index.items():
            if query in text:
                results.update(body_parts)
        return results
