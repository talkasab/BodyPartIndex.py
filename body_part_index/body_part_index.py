"""Routines to pull in the information/hierarchy of BodyPart objects from the standard library."""
import gc
import json
from typing import Dict, Iterable, Optional

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

    def _initialize(self, json_data: Dict) -> None:
        self.__index: Dict[str, BodyPart] = {}
        for body_part_dict in json_data["bodyParts"]:
            (args, kwargs) = BodyPartData.params_from_json_dict(body_part_dict)
            body_part: BodyPart = BodyPart(self, *args, **kwargs)
            if id in self.__index:
                raise Exception(f"Duplicate BodyPart with ID {id}")
            self.__index[body_part.radlex_id] = body_part
            # TODO: Harvest codes for code index
            # TODO: harvest strings from description, synonyms, and codes for search
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

    def get_by_code(self, code: Code) -> BodyPart:
        """Get BodyPart object by code.

        Args:
            code (str): Code of the BodyPart to retrieve

        Raises:
            Exception: If no BodyPart with the given code is found

        Returns:
            BodyPart: BodyPart object with the given code
        """
        pass

    def get(self, code_or_id: str) -> Optional[BodyPart]:
        """Get BodyPart object by code or ID.

        Args:
            code_or_id (str): Code (without system) or ID of the BodyPart to retrieve

        Returns:
            BodyPart: BodyPart object with the given code or ID
        """
        pass

    def search(self, query: str) -> Iterable[BodyPart]:
        """Search for BodyParts by query.

        Args:
            query (str): Query to search for BodyParts in description, synonyms, and codes

        Returns:
            Iterable[BodyPart]: BodyParts matching the query
        """
        pass
