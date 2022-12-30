# BodyPartIndex.py
Python wrapper library for standard set of body parts for tagging artifacts in medical imaging informatics (see https://www.anatomiclocations.org).

## Installation 

> Pending

Will soon be possible to install from PyPI:

```console
pip install body_part_index
```

# `BodyPartIndex` (Scenarios)

## How to open the library?

To open the library, you first need to import it into your project. Then, you can use the `BodyPartIndex` object.

```python
import requests, json
from body_part_index import BodyPartIndex, BodyPart, BODY_PART_INDEX_DATA_URL

# Import data from the standard URL
if (r := requests.get(BODY_PART_INDEX_DATA_URL)).status_code == reqeusts.codes.ok:
    index = BodyPartIndex(json_data=json.loads(r.text))

# Open a local data file
index = BodyPartIndex(json_filename='body_parts.json')
```

## How to use a local JSON file of body parts?

> pending

## How to get a particular body part by RadLex ID, SNOMED, or another code?

```python
index = BodyPartIndex(json_filename='body_parts.json')
bodyPart = index.get('RID294')
bodyPart2 = index.get('265256') # FMA code
# TODO: bodyPart3 = index.get('THX1138') # Local code
```

The function returns a `BodyPart` object.

## How to search for body parts based on names or synonyms?

The `search` function will return all the BodyParts that match a specific search value.

```python
index = BodyPartIndex(json_filename='body_parts.json')
bodyPart = index.search('adnexa')
```