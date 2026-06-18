import argparse

from korean_romanizer import romanize

def main():
    """Run the kroman command-line interface."""
    parser = argparse.ArgumentParser(description='Romanize Korean text.')
    parser.add_argument('text', nargs='+', help='The Korean text to be romanized.')
    args = parser.parse_args()
    
    text_to_romanize = " ".join(args.text)
    
    result = romanize(text_to_romanize)
    print(result)

if __name__ == '__main__':
    main()
