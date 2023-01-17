from distutils.core import setup

# read the contents of the README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'korean_romanizer',
  packages = ['korean_romanizer'],
  version = '0.25',
  license='GNU GPLv3',
  description = 'A Python library for Korean romanization',
  long_description=long_description,
  long_description_content_type='text/markdown'
  author = 'Ilkyu Ju',
  author_email = 'ju.ilkyu@gmail.com',
  url = 'https://github.com/osori/korean-romanizer',
  download_url = 'https://github.com/osori/korean-romanizer/archive/0.25.tar.gz',
  keywords = ['Korean', 'Romanization', 'Transliteration'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
