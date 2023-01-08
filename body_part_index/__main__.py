"""Command line interface for body_part_index package."""
import argparse
import logging
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

def body_part_summary(body_part: BodyPart) -> str:
    """Generate summary of BodyPart object."""
    descendants_count = len(body_part.descendants)
    return f'{body_part} [{descendants_count} children]'


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
    print(body_part_summary(body_part))
    for child in body_part.children:
        print(f'  {body_part_summary(child)}')

if __name__ == '__main__':
    main()
