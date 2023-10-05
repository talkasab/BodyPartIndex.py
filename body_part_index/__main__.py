"""Command line interface for body_part_index package."""
import argparse
import json
import logging
from typing import Dict, List, Optional
import requests
from body_part_index import BodyPartIndex, BodyPart, BODY_PART_INDEX_DATA_URL, WHOLE_BODY_ID


def setup_argparse() -> argparse.ArgumentParser:
    """Setup argparse for body_part_index CLI."""
    parser = argparse.ArgumentParser(
        description='Command line interface for body_part_index package.'
    )
    parser.add_argument(
        '-i', '-c', '--id_or_code',
        type=str,
        default=WHOLE_BODY_ID,
        required=False,
        help='ID or code (without system) of the BodyPart to retrieve',
    )
    parser.add_argument(
        '-u',
        '--from-url',
        type=str,
        const=BODY_PART_INDEX_DATA_URL,
        nargs='?',
        help='URL of the body part index data file',
    )
    parser.add_argument(
        '-f',
        '--from-file',
        type=str,
        help='Filename of the body part index data file',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '-t',
        '--tree',
        action='store_true',
        help='Enable JSON tree for tree view'
    )
    parser.add_argument(
        '-s',
        '--snomed',
        action='store_true',
        help='Enable report on SNOMED status report'
    )
    return parser


def setup_index(args) -> BodyPartIndex:
    """Generate BodyPartIndex object from command line arguments."""
    logger = logging.getLogger(__name__)
    if args.from_file is not None:
        logger.warning("Using body part index data from %s", args.from_file)
        return BodyPartIndex(json_filename=args.from_file)
    if args.from_url is not None:
        if (response := requests.get(args.from_url, timeout=3)).ok:
            logger.warning("Using body part index data from %s", args.from_url)
            return BodyPartIndex(json_data=response.json())
        raise Exception(f'Failed to retrieve body part index data from {args.from_url}')
    logger.warning("Using default body part index data")
    return BodyPartIndex()


def get_snomed_code(body_part: BodyPart)->Optional[str]:
    """Pull the SNOMED code out of a BodyPart object."""
    snomed_code = None
    for code in body_part.codes:
        if code.system == 'SNOMED':
            snomed_code = code.code
            break
    return snomed_code


def body_part_summary(body_part: BodyPart) -> str:
    """Generate summary of BodyPart object."""
    summary = str(body_part)
    if (snomed_code := get_snomed_code(body_part)) is not None:
        summary += f' (SNOMED: {snomed_code})'
    if (descendants_count := len(body_part.descendants)) > 0:
        summary += f' [{descendants_count} descendants]'
    return summary


def print_tree(body_part: BodyPart, indent: int = 2):
    """Print tree of BodyPart object."""
    print(body_part_summary(body_part))
    for child in body_part.children:
        lead = ' ' * indent
        print(f'{lead}{body_part_summary(child)}')


def body_part_to_dict(body_part: BodyPart) -> dict:
    """Convert BodyPart object to dict."""
    sorted_children = sorted(body_part.children, key=lambda bp: len(bp.descendants), reverse=True)
    return {
        'name': body_part_summary(body_part),
        'children': [body_part_to_dict(child) for child in sorted_children],
    }


def print_json_tree(body_part: BodyPart):
    """Print JSON tree of BodyPart object."""
    body_part_tree = body_part_to_dict(body_part)
    body_part_tree['expanded'] = True
    print('var tree = ' + json.dumps([body_part_tree], indent=2) + ';')


def find_snomed_statuses(body_part: BodyPart)->Dict[str, List[BodyPart]]:
    """Find SNOMED statuses for BodyPart object and descendants."""
    no_snomed = []
    unsided_snomed = []
    container_snomed = []
    
    for bp in [body_part] + body_part.descendants:
        if get_snomed_code(bp) is not None:
            continue
        if (bp.unsided is not None and get_snomed_code(bp.unsided) is not None):
            unsided_snomed.append(bp)
            unsided_snomed.append(body_part)
        elif get_snomed_code(bp.parent) is not None:
            container_snomed.append(bp)
        else:
            no_snomed.append(bp)
    
    return {'none': no_snomed, 'unsided': unsided_snomed, 'container': container_snomed}


def print_snomed_report(body_part: BodyPart)->None:
    """Print SNOMED status report for BodyPart object."""
    snomed_statuses = find_snomed_statuses(body_part)
    print(f'No SNOMED: {len(snomed_statuses["none"])}')


def main():
    """Main function for body_part_index CLI."""
    parser = setup_argparse()
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('body_part_index').setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger('body_part_index').setLevel(logging.ERROR)
    logging.getLogger(__name__).warning("Starting body_part_index CLI: %s", args)
    index: BodyPartIndex = setup_index(args)
    body_part: BodyPart = index.get(args.id_or_code)
    if body_part is None:
        raise Exception(f'No BodyPart with ID or code {args.id_or_code}')
    if args.tree:
        print_json_tree(body_part)
    if args.snomed:
        print_snomed_report(body_part)
    else:
        print_tree(body_part)

if __name__ == '__main__':
    main()
