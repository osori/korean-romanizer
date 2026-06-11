from setuptools import setup

setup(
  name = 'korean_romanizer',
  packages = ['korean_romanizer'],
  use_scm_version=True,
  license='GPL-3.0-or-later',
  description = 'A Python library for Korean romanization',
  author = 'Ilkyu Ju',
  author_email = 'ju.ilkyu@gmail.com',
  url = 'https://github.com/osori/korean-romanizer',
  keywords = ['Korean', 'Romanization', 'Transliteration'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  entry_points={
    'console_scripts': [
      'kroman=korean_romanizer.cli:main',
    ],
  },
  extras_require={
    'dev': [
      'build>=1.2',
      'flake8>=7.0',
      'mypy>=1.10',
      'pytest>=8.0',
      'pytest-cov>=5.0',
      'ruff>=0.6',
    ],
  },
)
