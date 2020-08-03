from distutils.core import setup
setup(
  name = 'korean_romanizer',
  packages = ['korean_romanizer'],
  version = '0.11',
  license='GNU GPLv3',
  description = 'A python library for Korean romanization',
  author = 'Ilkyu Ju',
  author_email = 'ju.ilkyu@gmail.com',
  url = 'https://github.com/osori/korean-romanizer',
  download_url = 'https://github.com/osori/korean-romanizer/archive/0.11.tar.gz',
  keywords = ['Korean', 'Romanization', 'Transliteration'],
  install_requires=[
      ],
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
