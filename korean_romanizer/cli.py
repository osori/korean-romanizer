import argparse
from importlib import metadata

from korean_romanizer import romanize


_DISTRIBUTION_NAME = "korean_romanizer"


class _VersionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(f"kroman {metadata.version(_DISTRIBUTION_NAME)}")
        parser.exit()


def main():
    """Run the kroman command-line interface."""
    parser = argparse.ArgumentParser(description='Romanize Korean text.')
    parser.add_argument(
        '--version',
        action=_VersionAction,
        nargs=0,
        help="show program's version number and exit",
    )
    parser.add_argument('text', nargs='+', help='The Korean text to be romanized.')
    args = parser.parse_args()

    text_to_romanize = " ".join(args.text)

    result = romanize(text_to_romanize)
    print(result)

if __name__ == '__main__':
    main()
