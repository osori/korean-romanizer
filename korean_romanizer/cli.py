import argparse
from korean_romanizer.romanizer import Romanizer

def main():
    parser = argparse.ArgumentParser(description='Romanize Korean text.')
    parser.add_argument('text', nargs='+', help='The Korean text to be romanized.')
    args = parser.parse_args()
    
    text_to_romanize = " ".join(args.text)
    
    r = Romanizer(text_to_romanize)
    result = r.romanize()
    print(result)

if __name__ == '__main__':
    main()
