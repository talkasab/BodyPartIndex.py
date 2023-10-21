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

# Import data distributed with the package
index = BodyPartIndex()


# OR import data from the latest version on the web
if (r := requests.get(BODY_PART_INDEX_DATA_URL)).status_code == requests.codes.ok:
    index = BodyPartIndex(json_data=json.loads(r.text))

# OR Open a local data file
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

## How to get a particular body part by system/code?

```python
index = BodyPartIndex(json_filename='body_parts.json')
body_part: BodyPart = index.get_by_code(Code('SNOMED', '818983003'))
```

## How to search for body parts based on names or synonyms?

The `search` function will return all the BodyParts that match a specific search value.

```python
index = BodyPartIndex(json_filename='body_parts.json')
bodyPart = index.search('adnexa')
```

# `BodyPart` (Scenarios)

## What can you get from a `BodyPart`?

```python
index = BodyPartIndex(json_filename='body_parts.json')
bodyPart = index.get('RID294')
bodyPart.description    # "uterine adnexa"
bodyPart.sex_specific   # "Female"
bodyPart.synonyms       # ["adnexa"]
bodyPart.contained_by   # BodyPart(radlex_id='RID2507', description='pelvis', ...)
bodyPart.part_of        # BodyPart(radlex_id='RID270', description='female genital system', ...)
bodyPart.codes          # [ Code(system='SNOMED', 'code=''), Code(...), Code(...) ]
```

## How to deal with sided body parts?

For cases where the body part is sided, the index contains three versions: an unsided version, a left-sided version, 
and a right-sided version. All of these are aware of each other.

```python
index = BodyPartIndex(json_filename='body_parts.json')
bodyPart = index.get('RID294') # uterine adnexa (side not specified)
# From the unsided version, get the right- and left-sided versions
right = bodyPart.right     # BodyPart(radlex_id='RID294_RID5825', description='right uterine adnexa', ...)
left  = bodyPart.left      # BodyPart(radlex_id='RID294_RID5824', description='left uterine adnexa', ...)
# From either sided versions, can get back to the unsided or to the other side
right.unsided == body_part # True
left.right    == right     # True
```
## How to determine if one body part is contained by another?

To determine if a one body part is contained by another, use the `is_contained` function.

```python
index = BodyPartIndex(json_filename='body_parts.json')
bodyPart1 = index.get('RID294') # uterine adnexa (side not specified)
bodyPart2 = index.get('RID39569') # whole body
is_contained = bodyPart1.is_contained(bodyPart2)
```

## How to get the contained children of a body part?

## How to use the 'snomed_code' property?

The  `BodyPart` class provides a property called `snomed_code` that returns the most appropriate SNOMED code for the body part. Here's how you can use it:

```python
index = BodyPartIndex(json_filename='body_parts.json')
bodyPart = index.get('RID294_RID5824') # Left uterine adnexa
snomed_code = bodyPart.snomed_code
print(f"SNOMED Code for Left Uterine Adnexa: {snomed_code}")
```
In this example, the `snomed_code` property returns the SNOMED code for the left uterine adnexa.
If the code is not directly assigned, it looks for the code in the unsided version and then the immediate parent body part. If no code is found, it returns None.
