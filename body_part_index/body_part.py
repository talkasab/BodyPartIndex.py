class BodyPart:
    """"Body part object representing a node in the anatomic location hierarchy."""
    def __init__(self, id: str, description: str, contained_by_id: str, **kwargs) :
        self.radlex_id = id
        self.description = description
        self.contained_by_id = contained_by_id
        self.codes = []
        if "codes" in kwargs :
            # TODO: check that kwargs["codes"] has the right structure
            for code in kwargs["codes"] :
                self.codes.append((code["system"], code["code"]))
        if "synonyms" in kwargs :
            # TODO: check to see that kwargs["codes"] has the right structure
            self.synonyms = set(kwargs["synonyms"])
        else :
            self.synonyms = set()
        self.children = set()
